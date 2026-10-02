import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode


class BlockType(Enum):
    # block text
    PARAGRAPH = 0 # paragraph text, or <p>...</p> text
    HEADING = 1 # # Heading text, or <h1>...</h1> text (or h2, h3, ...)
    CODE = 2 # ```, or <code>...</code>
    QUOTE = 3 # > Quote text, or <blockquote>...</blockquote>
    UNORDERED_LIST = 4 # - Item text, or <ul><li>...</li>...</ul>
    ORDERED_LIST = 5 # 1. ... text, 2. ..., ..., or <ol><li>...</li>...</ol>

block_type_characters: dict[BlockType, str] = {
    BlockType.PARAGRAPH: "",
    BlockType.HEADING: "^(#{1,6}) ",
    BlockType.CODE: r"^```\n",
    BlockType.QUOTE: r"^\> ?",
    BlockType.UNORDERED_LIST: "^- ",
    BlockType.ORDERED_LIST: r"^(\d+). ",
}


class BlockNode:
    def __init__(self, text: str, block_type: BlockType = BlockType.PARAGRAPH, \
                 url: str | None = None) -> None:
        self.text: str = text
        self.block_type: BlockType = block_type
        self.url: str | None = url

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.text == value.text \
                and self.block_type == value.block_type \
                and self.url == value.url
        return False

    def __repr__(self) -> str:
        return f"BlockNode({self.text}, {self.block_type.name}, {self.url})"

def block_to_block_type(block: str) -> BlockType:
    ret_val: BlockType = BlockType.PARAGRAPH
    if re.search(block_type_characters[BlockType.HEADING], block) is not None:
        ret_val = BlockType.HEADING
    elif re.search(block_type_characters[BlockType.CODE], block) is not None:
        ret_val = BlockType.CODE
    elif re.search(block_type_characters[BlockType.QUOTE], block) is not None:
        ret_val = BlockType.QUOTE
    elif re.search(block_type_characters[BlockType.UNORDERED_LIST], block) is not None:
        ret_val = BlockType.UNORDERED_LIST
    elif re.search(block_type_characters[BlockType.ORDERED_LIST], block) is not None:
        ret_val = BlockType.ORDERED_LIST
    return ret_val

def block_node_to_html_node(block_node: BlockNode) -> HTMLNode:
    match block_node.block_type:
        case BlockType.PARAGRAPH:
            return LeafNode("p", block_node.text)
        case BlockType.QUOTE:
            block_text: str = ""
            regex: str = block_type_characters[BlockType.QUOTE] + r"\s*?(.*?)\s*?$"
            list_items = re.findall(regex, block_node.text)
            for list_item in list_items:
                block_text += (list_item + "\n")
            return LeafNode("blockquote", block_text)
        case BlockType.HEADING:
            count: int = 1
            regex: str = block_type_characters[BlockType.HEADING] + r"\s*?(.*?)\s*?$"
            line_items = re.findall(regex, block_node.text)
            count = len(line_items[0][0])
            return LeafNode(f"h{count}", line_items[0][1])
        case BlockType.CODE:
            block_text: str = ""
            regex: str = block_type_characters[BlockType.CODE] + r"(.*?\n)+" + block_type_characters[BlockType.CODE]
            line_items = re.findall(regex, block_node.text)
            for line_item in line_items:
                block_text += line_item
            leaf = LeafNode("code", block_text)
            return ParentNode("pre", [leaf])
        case BlockType.ORDERED_LIST:
            leaves: list[HTMLNode] = []
            list_items: list[tuple[int, str]] = []
            regex: str = block_type_characters[BlockType.ORDERED_LIST] + r"\s*?(.*?)\s*?$"
            list_items = re.findall(regex, block_node.text)
            for list_item in sorted(list_items, key=lambda item: item[0]):
                leaves.append(LeafNode("li", list_item[1]))
            return ParentNode("ol", leaves)
        case BlockType.UNORDERED_LIST:
            leaves: list[HTMLNode] = []
            list_items: list[tuple[int, str]] = []
            regex: str = block_type_characters[BlockType.UNORDERED_LIST] + r"\s*?(.*?)\s*?$"
            list_items = re.findall(regex, block_node.text)
            for list_item in list_items:
                leaves.append(LeafNode("li", list_item[1]))
            return ParentNode("ul", leaves)

