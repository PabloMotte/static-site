import re

from textnode import TextNode, TextType, text_type_characters


def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    node: TextNode = TextNode(text, TextType.TEXT) 
    new_nodes = split_nodes_delimiter([node], TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def split_nodes_delimiter(old_nodes: list[TextNode], text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = [] 
    delimiter: str = text_type_characters[text_type]
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            # Clear double delimiters and replace by a single delimeter
            node_text = old_node.text.replace(delimiter+delimiter, delimiter)
            splits = node_text.count(delimiter)
            if splits % 2 == 1:
                raise ValueError("invalid Markdown syntax")
            else:
                # If we split by the delimiter, each list item will alternate between formatted and unformatted
                split_list = node_text.split(delimiter)
                formatted_elem: bool = False
                for splitting in range(len(split_list)):
                    if formatted_elem:
                        # first list item is in bold
                        new_node = TextNode(split_list[splitting], text_type)
                    else:
                        new_node = TextNode(split_list[splitting], TextType.TEXT)
                    if new_node.text != "":
                        new_nodes.append(new_node)
                    formatted_elem = not formatted_elem
        else:
            # no text? no bother!
            new_nodes.append(old_node)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            # no text? no bother!
            new_nodes.append(old_node)
            continue
        node_text = old_node.text
        images = extract_markdown_images(node_text)
        if len(images) == 0:
            # no images? no bother!
            new_nodes.append(old_node)
            continue
        for image in images:
            # split on the entire matched tuple from extract_markdown_images
            sections = node_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = [] 
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            # no text? no bother!
            new_nodes.append(old_node)
            continue
        node_text = old_node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            # no links? no bother!
            new_nodes.append(old_node)
            continue
        for link in links:
            # split on the entire matched tuple from extract_markdown_links
            sections = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # e.g. text = "This is text with a " 
    #   + "![rick roll](https://i.imgur.com/aKaOqIh.gif) and " 
    #   + "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # using this function gives:
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
    #  ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    ret_val: list[tuple[str, str]] \
     = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return ret_val

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    ret_val: list[tuple[str, str]] \
     = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return ret_val
