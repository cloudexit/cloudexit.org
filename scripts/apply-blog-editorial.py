#!/usr/bin/env python3
"""Apply the reviewed blog category/tag overlay and generate localized terms."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
BLOG_ROOT = ROOT / "content" / "blog"
DATA_ROOT = ROOT / "data" / "blog"

CATEGORY_DETAILS = {
    "cloud-exit-economics": {
        "weight": 10,
        "icon": "fa-solid fa-arrow-right-from-bracket",
        "description_en": "Exit cases, TCO models, resource prices, FinOps, and the economics of leaving cloud services.",
        "description_zh": "下云案例、TCO 模型、资源价格、FinOps，以及离开云服务的经济账。",
    },
    "failures-postmortems": {
        "weight": 20,
        "icon": "fa-solid fa-triangle-exclamation",
        "description_en": "Service incidents, technical causes, timelines, accountability, and lessons from failure.",
        "description_zh": "云服务事故、技术原因、事件时间线、责任边界与故障教训。",
    },
    "security-control-risks": {
        "weight": 30,
        "icon": "fa-solid fa-shield-halved",
        "description_en": "Security, privacy, billing, data-loss, and control-plane risks when someone else holds the keys.",
        "description_zh": "当控制权掌握在他人手中时，安全、隐私、账单、数据丢失与控制面风险。",
    },
    "cloud-business": {
        "weight": 40,
        "icon": "fa-solid fa-chart-line",
        "description_en": "Cloud vendors, market structure, pricing strategy, sales, public relations, and industry commentary.",
        "description_zh": "云厂商、市场结构、定价策略、销售、公关与产业评论。",
    },
    "cloud-databases": {
        "weight": 50,
        "icon": "fa-solid fa-database",
        "description_en": "RDS economics, operational boundaries, database capability, and the changing role of DBAs.",
        "description_zh": "RDS 经济账、托管边界、数据库能力，以及 DBA 角色的变化。",
    },
    "self-hosting": {
        "weight": 60,
        "icon": "fa-solid fa-screwdriver-wrench",
        "description_en": "Practical playbooks, deployment guides, product choices, and operating experience for self-hosting.",
        "description_zh": "自建部署的实操手册、产品选型、迁移方法与运行经验。",
    },
    "sovereignty-open-ecosystems": {
        "weight": 70,
        "icon": "fa-solid fa-key",
        "description_en": "Data sovereignty, exit rights, local-first software, open source, licensing, and community governance.",
        "description_zh": "数据主权、退出权、本地优先、开源软件、许可证与共同体治理。",
    },
    "infrastructure-engineering": {
        "weight": 80,
        "icon": "fa-solid fa-gears",
        "description_en": "Architecture, APIs, hardware, SRE, platform teams, and durable infrastructure capability.",
        "description_zh": "架构、API、硬件、SRE、平台团队与可持续的基础设施能力。",
    },
}


def load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text())


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def expected_frontmatter(frontmatter: str, category: str, tags: list[str]) -> str:
    lines = frontmatter.splitlines()
    filtered: list[str] = []
    skip_list = False
    inserted = False
    for line in lines:
        if re.match(r"^(categories|tags):", line):
            if not inserted and line.startswith("tags:"):
                filtered.append(f"categories: [{category}]")
                filtered.append("tags:")
                filtered.extend(f"  - {tag}" for tag in tags)
                inserted = True
            skip_list = True
            continue
        if skip_list and re.match(r"^\s+-\s+", line):
            continue
        skip_list = False
        filtered.append(line)
    if not inserted:
        filtered.append(f"categories: [{category}]")
        filtered.append("tags:")
        filtered.extend(f"  - {tag}" for tag in tags)
    return "\n".join(filtered)


def apply_page(path: Path, category: str, tags: list[str], write: bool) -> bool:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML front matter: {path}")
    _, frontmatter, body = text.split("---", 2)
    current = frontmatter.strip("\n")
    expected = expected_frontmatter(current, category, tags)
    updated = f"---\n{expected}\n---{body}"
    if updated == text:
        return False
    if write:
        path.write_text(updated)
    return True


def term_page(
    title: str,
    description: str | None = None,
    icon: str | None = None,
    weight: int | None = None,
) -> str:
    fields = ["---", f"title: {yaml_quote(title)}", f"linkTitle: {yaml_quote(title)}"]
    if description:
        fields.append(f"description: {yaml_quote(description)}")
    if icon:
        fields.append(f"icon: {icon}")
    if weight is not None:
        fields.append(f"weight: {weight}")
    fields.extend(["type: blog", "toc_taxonomies: false", "---", ""])
    return "\n".join(fields)


def generate_terms(taxonomy: dict[str, object], write: bool) -> int:
    changed = 0
    roots = {
        "categories": ("Columns", "栏目"),
        "tags": ("Tags", "标签"),
    }
    for plural, (en_title, zh_title) in roots.items():
        root = ROOT / "content" / plural
        pages = {
            root / "_index.md": term_page(en_title),
            root / "_index.zh.md": term_page(zh_title),
        }
        for term_id, term in taxonomy[plural].items():
            details = CATEGORY_DETAILS.get(term_id, {})
            term_root = root / term_id
            pages[term_root / "_index.md"] = term_page(
                term["en"],
                details.get("description_en"),
                details.get("icon"),
                details.get("weight"),
            )
            pages[term_root / "_index.zh.md"] = term_page(
                term["zh"],
                details.get("description_zh"),
                details.get("icon"),
                details.get("weight"),
            )
        for path, content in pages.items():
            if path.is_file() and path.read_text() == content:
                continue
            changed += 1
            if write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="apply changes")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    editorial = load_yaml(DATA_ROOT / "editorial.yaml")
    taxonomy = load_yaml(DATA_ROOT / "taxonomy.yaml")
    article_dirs = {path.name for path in BLOG_ROOT.iterdir() if path.is_dir()}
    configured = set(editorial["articles"])
    if article_dirs != configured:
        missing = sorted(article_dirs - configured)
        extra = sorted(configured - article_dirs)
        raise SystemExit(f"editorial coverage mismatch; missing={missing}, extra={extra}")

    changed_pages = 0
    for slug, record in editorial["articles"].items():
        for path in sorted((BLOG_ROOT / slug).glob("index*.md")):
            changed_pages += apply_page(path, record["category"], record["tags"], args.write)
    changed_terms = generate_terms(taxonomy, args.write)
    action = "updated" if args.write else "would update"
    print(f"{action} {changed_pages} article pages and {changed_terms} taxonomy pages")
    return 0 if args.write or (changed_pages == 0 and changed_terms == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
