import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "text in here")
        node2 = HTMLNode("p", "text in here")
        self.assertEqual(node.__repr__(), node2.__repr__())

    def test_ne(self):
        node = HTMLNode("p", "text in here")
        node2 = HTMLNode("a", "description in here", None, {"href":"https://boot.dev"})
        self.assertNotEqual(node.__repr__(), node2.__repr__())

    def test_has_children(self):
        node = HTMLNode("p", "text in here")
        node2 = HTMLNode("a", "description in here", [node], {"href":"https://boot.dev"})
        self.assertNotEqual(node2.__repr__(), None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Google it!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google it!</a>')

    def test_leaf_value_error(self):
        node = LeafNode("a", "")
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_children(self):
        node = ParentNode(
                "",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
        self.assertRaises(ValueError, node.to_html)
        node.tag = "p"
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children2(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
