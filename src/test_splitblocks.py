import unittest

from blocknode import BlockType, block_to_block_type
from splitblocks import markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_block_identification(self):
        md = """
This is **bolded** paragraph

1. This is another paragraph with _italic_ text and `code` here
2. This is the same paragraph on a new line

# This is a heading

> This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "1. This is another paragraph with _italic_ text and `code` here\n2. This is the same paragraph on a new line",
                "# This is a heading",
                "> This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(blocks[0]))
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(blocks[1]))
        self.assertEqual(BlockType.HEADING, block_to_block_type(blocks[2]))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(blocks[3]))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(blocks[4]))

if __name__ == "__main__":
    unittest.main()
