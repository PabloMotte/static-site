from enum import Enum


class TextType(Enum):
    # inline text
    PLAIN_TEXT = 0 # text, or <p></p> text
    BOLD_TEXT = 1 # **Bold** text, or <b>Bold</b> text
    ITALIC_TEXT = 2 # _Italic_ text, or <i>Italic</i> text
    CODE_TEXT = 3 # `Code` text
    LINKS = 4 # [anchor text](url)
    IMAGES = 5 # ![alt text](url)

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.PLAIN_TEXT, url: str | None = None) -> None:
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
