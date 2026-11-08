#!/usr/bin/env ruby
# frozen_string_literal: true

require 'date'
require 'yaml'

ROOT = File.expand_path('..', __dir__)
BLOG_ROOT = File.join(ROOT, 'content', 'blog')
DATA_ROOT = File.join(ROOT, 'data', 'blog')

def fail!(message)
  warn message
  exit 1
end

def front_matter(path)
  text = File.read(path)
  parts = text.split(/^---\s*$\n?/, 3)
  fail!("invalid front matter: #{path}") unless parts.length == 3

  YAML.safe_load(parts[1], permitted_classes: [Date, Time], aliases: true) || {}
end

editorial = YAML.safe_load(File.read(File.join(DATA_ROOT, 'editorial.yaml')), aliases: true)
taxonomy = YAML.safe_load(File.read(File.join(DATA_ROOT, 'taxonomy.yaml')), aliases: true)
articles = editorial.fetch('articles')
categories = taxonomy.fetch('categories')
tags = taxonomy.fetch('tags')

bundle_slugs = Dir.children(BLOG_ROOT).select do |entry|
  File.directory?(File.join(BLOG_ROOT, entry))
end.sort
fail!('editorial article coverage differs from content/blog bundles') unless bundle_slugs == articles.keys.sort

category_counts = Hash.new(0)
english = 0
articles.each do |slug, record|
  category = record.fetch('category')
  article_tags = record.fetch('tags')
  fail!("unknown category for #{slug}: #{category}") unless categories.key?(category)
  fail!("#{slug}: expected 4-8 tags") unless (4..8).cover?(article_tags.length)
  fail!("#{slug}: duplicate tags") unless article_tags.uniq == article_tags
  unknown = article_tags.reject { |tag| tags.key?(tag) }
  fail!("#{slug}: unknown tags #{unknown.join(', ')}") unless unknown.empty?
  fail!("#{slug}: missing primary form") unless article_tags.any? { |tag| tag.start_with?('form-') && tag != 'form-translation' }
  fail!("#{slug}: too many tone tags") if article_tags.count { |tag| tag.start_with?('tone-') } > 1
  fail!("#{slug}: too many entity tags") if article_tags.count { |tag| tag.start_with?('vendor-', 'org-', 'person-') } > 3
  resource_topics = article_tags.count { |tag| tag.start_with?('resource-', 'service-', 'tech-', 'product-', 'topic-') }
  fail!("#{slug}: expected 1-3 resource/topic tags") unless (1..3).cover?(resource_topics)

  pages = Dir.glob(File.join(BLOG_ROOT, slug, 'index*.md')).sort
  pages.each do |path|
    metadata = front_matter(path)
    fail!("#{path}: category mismatch") unless metadata['categories'] == [category]
    fail!("#{path}: tag mismatch") unless metadata['tags'] == article_tags
  end
  english += 1 if File.file?(File.join(BLOG_ROOT, slug, 'index.md'))
  category_counts[category] += 1
end

fail!("expected 158 articles, got #{articles.length}") unless articles.length == 158
fail!("expected 81 English articles, got #{english}") unless english == 81
fail!('expected 8 populated categories') unless category_counts.length == 8 && category_counts.values.sum == 158

%w[categories tags].each do |plural|
  terms = taxonomy.fetch(plural)
  terms.each_key do |term|
    %w[_index.md _index.zh.md].each do |name|
      path = File.join(ROOT, 'content', plural, term, name)
      fail!("missing localized taxonomy term page: #{path}") unless File.file?(path)
    end
  end
end

puts "blog editorial taxonomy OK: #{articles.length} articles, #{categories.length} columns, #{tags.length} tags"
