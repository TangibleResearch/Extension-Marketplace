from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


SLUG_PATTERN = re.compile(r"[^a-z0-9-]+")


@dataclass
class ExtensionSpec:
    name: str
    publisher: str = "TangibleResearch"
    description: str = "A Tangible Studio extension."
    version: str = "0.1.0"
    language: str = "typescript"
    categories: list[str] = field(default_factory=lambda: ["Other"])
    permissions: list[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        value = SLUG_PATTERN.sub("-", self.name.strip().lower()).strip("-")
        return value or "tangible-extension"


def create_extension(spec: ExtensionSpec, root: str | Path = ".") -> Path:
    target = Path(root).expanduser().resolve() / spec.slug
    src = target / "src"
    src.mkdir(parents=True, exist_ok=True)

    manifest = {
        "name": spec.slug,
        "displayName": spec.name,
        "publisher": spec.publisher,
        "description": spec.description,
        "version": spec.version,
        "engines": {"tangibleStudio": "^0.1.0"},
        "categories": spec.categories,
        "permissions": spec.permissions,
        "activationEvents": ["onCommand:tangible.helloWorld"],
        "contributes": {
            "commands": [
                {
                    "command": "tangible.helloWorld",
                    "title": "Hello Tangible Extension",
                }
            ]
        },
        "main": "./src/extension.ts" if spec.language == "typescript" else "./src/extension.py",
    }

    (target / "tangible-extension.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (target / "README.md").write_text(f"# {spec.name}\n\n{spec.description}\n")

    if spec.language == "python":
        (src / "extension.py").write_text(
            "def activate(context):\n"
            "    context.commands.register('tangible.helloWorld', lambda: context.window.info('Hello from Tangible.'))\n\n"
            "def deactivate():\n"
            "    pass\n"
        )
    else:
        (src / "extension.ts").write_text(
            "export function activate(context) {\n"
            "  context.commands.register('tangible.helloWorld', () => {\n"
            "    context.window.info('Hello from Tangible.');\n"
            "  });\n"
            "}\n\n"
            "export function deactivate() {}\n"
        )

    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Tangible Studio extension project.")
    parser.add_argument("name")
    parser.add_argument("--root", default=".")
    parser.add_argument("--publisher", default="TangibleResearch")
    parser.add_argument("--description", default="A Tangible Studio extension.")
    parser.add_argument("--language", choices=["typescript", "python"], default="typescript")
    args = parser.parse_args()

    path = create_extension(
        ExtensionSpec(
            name=args.name,
            publisher=args.publisher,
            description=args.description,
            language=args.language,
        ),
        args.root,
    )
    print(path)


if __name__ == "__main__":
    main()
