
from typing import Any


class HTMLNode:
    def __init__(self, tag: str | None = None, 
                value: str | None = None, 
                children: list["HTMLNode"] | None = None, 
                props: dict[str, Any] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None or len(self.props) < 1:
            return "" 
        else:
            ret_val: str = ""
            for prop in self.props:
                ret_val += f' {prop}="{self.props[prop]}"'
            return ret_val

    def __repr__(self) -> str:
        return f'HTMLNode("{self.tag}", "{self.value}", [{self.children}], [{self.props_to_html()}])'

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, Any] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.: " + self.__repr__())
        if self.tag is None or len(self.tag) < 1:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f'LeafNode("{self.tag}", "{self.value}", [{self.props_to_html()}])'

class ParentNode(HTMLNode):
    def __init__(self, tag: str, 
                children: list["HTMLNode"], 
                props: dict[str, Any] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("invalid HTML: no tag: " + self.__repr__())
        if self.children is None:
            raise ValueError("invalid HTML: no children: " + self.__repr__())
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f'ParentNode("{self.tag}", [{self.children}], [{self.props_to_html()}])'


