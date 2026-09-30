#!/usr/bin/env python3

from textnode import TextNode, TextType


def main():
    textnode: TextNode = TextNode("This is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(textnode)

if __name__ == "__main__":
    main()
