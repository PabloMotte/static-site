from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    # inline text
    TEXT = 0 # text, or <p></p> text
    BOLD = 1 # **Bold** text, or <b>Bold</b> text
    ITALIC = 2 # _Italic_ text, or <i>Italic</i> text
    CODE = 3 # `Code` text
    LINK = 4 # [anchor text](url)
    IMAGE = 5 # ![alt text](url)

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.TEXT, \
                 url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.text == value.text \
                and self.text_type == value.text_type \
                and self.url == value.url
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
