#!/usr/bin/env python3
"""Create a non-overwriting docs/tests session from bundled templates."""

import argparse
import datetime as dt
import re
import shutil
import tempfile
from pathlib import Path


TEMPLATE_NAMES = (
    "test-charter.md",
    "risk-register.md",
    "rtm.md",
    "test-plan.md",
    "test-cases.md",
    "defect-log.md",
    "evidence-index.md",
    "test-summary.md",
)


def scope_slug(scope: str) -> str:
    if not scope.strip() or "/" in scope or "\\" in scope or ".." in scope:
        raise ValueError("scope must be non-empty text, not a path")
    slug = re.sub(r"[\W_]+", "-", scope.strip().lower(), flags=re.UNICODE).strip("-")
    if not slug:
        raise ValueError("scope must contain letters or digits")
    return slug


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Target project root")
    parser.add_argument("--scope", required=True, help="Feature, flow, release, or product")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Session date")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        slug = scope_slug(args.scope)
        session_date = dt.date.fromisoformat(args.date).isoformat()
    except ValueError as error:
        raise SystemExit(str(error)) from error

    templates = Path(__file__).resolve().parent.parent / "assets/templates"
    missing = [name for name in TEMPLATE_NAMES if not (templates / name).is_file()]
    if missing:
        raise SystemExit(f"missing bundled templates: {', '.join(missing)}")

    target = args.root.resolve() / "docs/tests" / f"{session_date}-{slug}"
    if target.exists():
        raise SystemExit(f"test session already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)

    replacements = {
        "{{SESSION_DATE}}": session_date,
        "{{SCOPE}}": args.scope.strip(),
        "{{SCOPE_SLUG}}": slug,
    }
    temporary = Path(tempfile.mkdtemp(prefix=f".{target.name}.", dir=target.parent))
    try:
        for name in TEMPLATE_NAMES:
            source = templates / name
            content = source.read_text(encoding="utf-8")
            for token, value in replacements.items():
                content = content.replace(token, value)
            destination = temporary / name
            destination.write_text(content, encoding="utf-8")
            shutil.copymode(source, destination)
        temporary.replace(target)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
