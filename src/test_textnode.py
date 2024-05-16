import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node2", "italic")
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", "italic", "https://test.dev")
        node2 = TextNode("This is a text node", "italic", "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", "italic")
        self.assertEqual(node.url, None)
    
    def test_repr(self):
        node = TextNode("This is a text node", "italic", "https://boot.dev")
        self.assertEqual("TextNode(This is a text node, italic, https://boot.dev)", repr(node))

if __name__ == "__main__":
    unittest.main()