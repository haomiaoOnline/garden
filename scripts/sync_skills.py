#!/usr/bin/env python3
import json
import os
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

DEFAULT_CATALOG_URL = "https://raw.githubusercontent.com/haomiaoOnline/skills/main/skills.json"
OUTPUT_PATH = Path("content/技能库/index.md")


def load_catalog():
    local_file = os.environ.get("SKILLS_CATALOG_FILE")
    if local_file:
        return json.loads(Path(local_file).read_text(encoding="utf-8"))

    url = os.environ.get("SKILLS_CATALOG_URL", DEFAULT_CATALOG_URL)
    request = Request(url, headers={"User-Agent": "haomiaoOnline-garden-skill-sync"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"failed to fetch Skill catalog: HTTP {response.status}")
        return json.loads(response.read().decode("utf-8"))


def validate_catalog(catalog):
    if catalog.get("schema_version") != 1:
        raise ValueError("unsupported skills.json schema_version")

    repository = catalog.get("repository")
    if not isinstance(repository, str) or not repository:
        raise ValueError("skills.json repository is required")

    skills = catalog.get("skills")
    if not isinstance(skills, list):
        raise ValueError("skills.json skills must be an array")

    required = {"id", "name", "path", "summary", "kind", "status", "tags"}
    ids = set()
    paths = set()

    for skill in skills:
        missing = required - skill.keys()
        if missing:
            raise ValueError(
                f"Skill {skill.get('id', '<unknown>')} missing {sorted(missing)}"
            )
        if skill["id"] in ids:
            raise ValueError(f"duplicate Skill id: {skill['id']}")
        if skill["path"] in paths:
            raise ValueError(f"duplicate Skill path: {skill['path']}")
        if not isinstance(skill["tags"], list):
            raise ValueError(f"Skill {skill['id']} tags must be an array")
        ids.add(skill["id"])
        paths.add(skill["path"])


def encode_repo_path(value):
    return "/".join(quote(part, safe="") for part in value.split("/"))


def md_text(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render(catalog):
    repository = catalog["repository"].rstrip("/")
    source_url = f"{repository}/blob/main/skills.json"
    skills = catalog["skills"]

    lines = [
        "---",
        "title: 我的 Skills",
        "tags:",
        "  - 🧰 Skill",
        "description: 从个人 Skills 仓库自动生成的 Skill 列表",
        "---",
        "",
        "这里收录我自己维护和使用的 Skill。",
        "",
        f"本页由数字花园构建流程从 [skills.json]({source_url}) 自动生成。Skill 列表不在 Garden 中手工维护。",
        "",
        f"当前共 **{len(skills)}** 个 Skill。",
        "",
    ]

    for skill in skills:
        skill_url = f"{repository}/tree/main/{encode_repo_path(skill['path'])}"
        lines.extend(
            [
                f"## [{md_text(skill['name'])}]({skill_url})",
                "",
                md_text(skill["summary"]),
                "",
                f"- 类型：{md_text(skill['kind'])} · 状态：{md_text(skill['status'])}",
            ]
        )
        if skill["tags"]:
            lines.append("- 标签：" + "、".join(md_text(tag) for tag in skill["tags"]))
        if skill.get("entrypoint"):
            entry_url = (
                f"{repository}/blob/main/{encode_repo_path(skill['entrypoint'])}"
            )
            lines.append(f"- [查看入口文件]({entry_url})")
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    catalog = load_catalog()
    validate_catalog(catalog)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render(catalog), encoding="utf-8")
    print(f"generated {OUTPUT_PATH} from {len(catalog['skills'])} Skills")


if __name__ == "__main__":
    main()
