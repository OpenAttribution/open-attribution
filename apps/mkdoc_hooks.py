# type: ignore
"""Make override changes to mkdocs via hooks."""

import re


def on_post_page(output: str, **kwargs) -> str:
    # ruff: noqa
    """Override the mkdocs post_page function."""
    # replace the static directory where mkdocs builds to with the SvelteKit route
    # output = re.sub(r"../../assets", r"/documentation/assets", output)
    # here we want to set the base url for all relative links, does not work still
    # output = re.sub(
    #     r"(</head>)",
    #     r'\t<base href="/docs/" target="_top">\n\1',
    #     output,
    #     flags=re.IGNORECASE,
    # )
    # Add target="_top" to change URL outside of iFrame
    # output = re.sub(r'href="([^"]+)"', r'href="\1" target="_top"', output)
    return output
