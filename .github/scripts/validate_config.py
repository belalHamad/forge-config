#!/usr/bin/env python3
"""Checks remote_config.json before the Forge app ever sees it.

The app silently ignores a file it can't read (it keeps the last good
version), so a typo would otherwise go unnoticed. This mirrors the app's
`RemoteConfig` model: which fields exist and what type each one must be.
Errors fail the check (red X on the commit); warnings only annotate it.
"""
import difflib
import json
import sys

# Field -> allowed JSON types. Mirrors Forge's RemoteConfig.swift.
# `featuredPackID` also exists in the app's model but isn't used by any
# screen yet, so it's deliberately not accepted here (it would do nothing).
FIELDS = {
    "paywallHeadline": (str, type(None)),
    "paywallSubheadline": (str, type(None)),
    "bannerVisible": (bool,),
    "bannerText": (str, type(None)),
    "anchorPriceText": (str, type(None)),
}
REQUIRED = {"bannerVisible"}  # the app rejects the whole file without it
TYPE_NAMES = {str: "text in quotes", type(None): "null", bool: "true or false"}


def main(path: str) -> int:
    errors, warnings = [], []

    def no_duplicates(pairs):
        seen = {}
        for key, value in pairs:
            if key in seen:
                errors.append(f'"{key}" appears twice — keep only one.')
            seen[key] = value
        return seen

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f, object_pairs_hook=no_duplicates)
    except json.JSONDecodeError as e:
        print(f"::error file={path},line={e.lineno},col={e.colno}::Not valid JSON: {e.msg} "
              "(check for a missing comma, a missing quote, or a comma after the last line).")
        return 1

    if not isinstance(data, dict):
        errors.append("The file must be one { ... } block.")
        data = {}

    for key in data:
        if key not in FIELDS:
            hint = difflib.get_close_matches(key, FIELDS, n=1)
            if key == "featuredPackID":
                errors.append('"featuredPackID" isn\'t used by the app yet — remove it.')
            else:
                errors.append(f'Unknown field "{key}"' + (f' — did you mean "{hint[0]}"?' if hint else "."))

    for key in sorted(REQUIRED - data.keys()):
        errors.append(f'"{key}" is missing — it must be there (true or false).')

    for key, value in data.items():
        allowed = FIELDS.get(key)
        if allowed and not isinstance(value, allowed):
            expected = " or ".join(TYPE_NAMES[t] for t in allowed)
            errors.append(f'"{key}" must be {expected}.')
        if isinstance(value, str) and not value.strip():
            errors.append(f'"{key}" is empty text — use null instead of "".')

    if data.get("bannerVisible") is True and not (isinstance(data.get("bannerText"), str) and data["bannerText"].strip()):
        errors.append('"bannerVisible" is true but "bannerText" is empty — the banner would not show.')

    for key in ("paywallHeadline", "paywallSubheadline", "bannerText", "anchorPriceText"):
        value = data.get(key)
        if isinstance(value, str) and any(c in value for c in "$€£¥₺"):
            warnings.append(f'"{key}" mentions a price. Apple requires price claims to be true; '
                            "real prices always come from the App Store.")

    for message in warnings:
        print(f"::warning file={path}::{message}")
    for message in errors:
        print(f"::error file={path}::{message}")
    if errors:
        return 1
    print(f"{path} looks good.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "remote_config.json"))
