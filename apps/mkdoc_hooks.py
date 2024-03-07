# type: ignore
"""Make override changes to mkdocs via hooks."""

import re


def on_post_page(output: str, **kwargs) -> str:
    # ruff: noqa
    """Override the mkdocs post_page function."""
    # Add target="_top" to change URL outside of iFrame
    output = re.sub(r'href="([^"]+)"', r'href="\1" target="_top"', output)
    return output
