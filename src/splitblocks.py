import re

from textnode import TextNode, TextType, text_type_characters


def markdown_to_blocks(markdown: str) -> list[str]:
    ret_val: list[str] = []
    for block in markdown.split("\n\n"):
        if block.strip() != "":
            ret_val.append(block.strip())
    return ret_val
