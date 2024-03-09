import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello this is a paragraph Text.",props={"href": "https://www.google.com"})
        self.assertEqual("HTMLNode(p, Hello this is a paragraph Text., None, {'href': 'https://www.google.com'})", repr(node))

    def test_props_to_html_all_None(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())
    
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(" href=https://boot.dev", node.props_to_html())

    def test_to_html(self):
        node = LeafNode("p","This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>",node.to_html())
    
    def test_value_not_passed(self):
        node = LeafNode("a", None, {"href": "https://boot.dev"})
        self.assertRaises(ValueError, node.to_html)
    
    def test_no_tag(self):
        node = LeafNode(None, "This is pure text.")
        self.assertEqual(node.to_html(), "This is pure text.")
    
    def test_parentnode_no_tag(self):
        node = ParentNode(None,[LeafNode("p","text"), LeafNode("a", "Click me!", {"href": "https://boots.dev"}), LeafNode("p", "text2")], None )
        self.assertRaises(ValueError, node.to_html)
    
    def test_parentnode_no_children(self):
        node = ParentNode("p", None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_parentnode_nested_no_tag(self):
        node = ParentNode("p", [ParentNode(None , [LeafNode("b", "bold text", None)])], None)
        self.assertRaises(ValueError, node.to_html)

    def test_nested_nodes_level1(self):
        node = ParentNode("div", [LeafNode("p","text"), LeafNode("a", "Click me!", {"href": "https://boots.dev"}), LeafNode("p", "text2")])
        self.assertEqual("<div><p>text</p><a href=https://boots.dev>Click me!</a><p>text2</p></div>", node.to_html())
    
    def test_nested_nodes_level2(self):
        node = ParentNode("div",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "Normal Text", None),
                                LeafNode("b", "bold text", None),
                                LeafNode(None, "Normal Text", None)
                            ]
                        )
                    ],
                    None
                )
        self.assertEqual("<div><p>Normal Text<b>bold text</b>Normal Text</p></div>", node.to_html())
    
    def test_nested_nodes_level3(self):
        node = ParentNode(
                    "div",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "Normal Text", None),
                                LeafNode("b", "bold text", None),
                                LeafNode(None, "Normal Text", None)
                            ]
                        ),
                        ParentNode(
                            "ul",
                            [
                                LeafNode("li", "Item1"),
                                LeafNode("li", "Item2")
                            ]
                        ),
                        LeafNode("p", "Pure Text", None)
                    ],
                    None
                )
        self.assertEqual("<div><p>Normal Text<b>bold text</b>Normal Text</p><ul><li>Item1</li><li>Item2</li></ul><p>Pure Text</p></div>", node.to_html())

if __name__ == "__main__":
    unittest.main()