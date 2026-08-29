#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'

root = File.expand_path('..', __dir__)
en = YAML.safe_load(File.read(File.join(root, 'data/home/en.yaml')), aliases: true)
zh = YAML.safe_load(File.read(File.join(root, 'data/home/zh.yaml')), aliases: true)

def shape(value)
  case value
  when Hash
    value.keys.sort.to_h { |key| [key, shape(value[key])] }
  when Array
    value.map { |item| shape(item) }
  else
    :scalar
  end
end

unless shape(en) == shape(zh)
  warn 'home data parity failed: en.yaml and zh.yaml differ in structure'
  exit 1
end

puts 'home data parity OK'

