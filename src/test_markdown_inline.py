import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link
)
from markdown_inline import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnode
)

class TestMarkdownInline(unittest.TestCase):
    def test_text_type_bold(self):
        node = TextNode("The end of the movie is **good**.", "text")
        self.assertEqual([TextNode("The end of the movie is ", "text"), TextNode("good", "bold"), TextNode(".", "text")], split_nodes_delimiter([node], "**", "bold"))

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual([("link", "https://www.example.com"), ("another", "https://www.example.com/another")], extract_markdown_links(text))
    
    def test_extract_images(self):
        text = "This is a text with a ![image](https://i.imgur.com/zqwoijd.png) and ![one more](https://i.imgur.com/ijqoiwjd.png)"
        self.assertEqual([("image","https://i.imgur.com/zqwoijd.png"), ("one more", "https://i.imgur.com/ijqoiwjd.png")], extract_markdown_images(text))

    def test_split_image_nodes(self):
        nodes = [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with more Text behind.",
                    text_type_text,
                    ),
                TextNode("", 
                        text_type_text
                        ),
                TextNode(
                    "This is a second text with an ![third image](https://i.imgur.com/zjjcJKZ.png) and another ![fourth image](https://i.imgur.com/3elNhQu.png)",
                    text_type_text,
                    )
                ]
    
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            [
                TextNode("This is text with an ", text_type_text, None),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text, None),
                TextNode("second image", text_type_image, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with more Text behind.", text_type_text, None),
                TextNode("This is a second text with an ", text_type_text, None),
                TextNode("third image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text, None),
                TextNode("fourth image", text_type_image, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
            )
    
    def test_split_link_nodes(self):
        nodes = [
                TextNode(
                    "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) with more Text behind.",
                    text_type_text,
                    ),
                TextNode("", 
                        text_type_text
                        ),
                TextNode(
                    "Second text with [third link](https://i.imgur.com/zjjcJKZ.png) and another [fourth link](https://i.imgur.com/3elNhQu.png) with more Text behind.",
                    text_type_text,
                    )
                ]
    
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            [
                TextNode("This is text with an ", text_type_text, None),
                TextNode("link", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text, None),
                TextNode("second link", text_type_link, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with more Text behind.", text_type_text, None),
                TextNode("Second text with ", text_type_text, None),
                TextNode("third link", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text, None),
                TextNode("fourth link", text_type_link, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with more Text behind.", text_type_text)
            ],
            new_nodes
            )
    
    def test_split_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        text_nodes = text_to_textnode(text)

        self.assertEqual(
            [
                TextNode("This is ", "text", None),
                TextNode("text", "bold", None),
                TextNode(" with an ", "text", None),
                TextNode("italic", "italic", None),
                TextNode(" word and a ", "text", None),
                TextNode("code block", "code", None),
                TextNode(" and an ", "text", None),
                TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", "text", None), TextNode("link", "link", "https://boot.dev")
            ],
            text_nodes
        )

if __name__ == "__main__":
    unittest.main()