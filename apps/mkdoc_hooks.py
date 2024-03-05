# type: ignore
# ruff: noqa
"""Make changes to mkdocs via hooks."""

import re


def on_post_page(output: str, **kwargs) -> str:
    """Override the mkdocs post_page function."""
    return re.sub(r'href="([^"]+)"', r'href="\1" target="_top"', output)
