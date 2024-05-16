import unittest

from markdown_block import (
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
    markdown_to_blocks,
    block_to_block_type
)

class TestMarkdownBlock(unittest.TestCase):

    def test_markdown_to_block1(self):
        text = "\nThis is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n\n\n\n\n* This is a list\n* with items\n\n"
        self.assertEqual(["This is **bolded** paragraph", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", "* This is a list\n* with items"], markdown_to_blocks(text))

    def test_markdown_to_block2(self):
        text = "This is a paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n\n"
        self.assertEqual(["This is a paragraph", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", "* This is a list\n* with items"], markdown_to_blocks(text))
    
    def test_block_to_blocktype1(self):
        block_header = "# This is header 1"
        self.assertEqual(block_type_heading, block_to_block_type(block_header))

    def test_block_to_blocktype2(self):
        block_code = "```py def this_is_a_function()```"
        self.assertEqual(block_type_code, block_to_block_type(block_code))
    
    def test_block_to_blocktype3(self):
        block_quote = ">This is a quote"
        self.assertEqual(block_type_quote, block_to_block_type(block_quote))
    
    def test_block_to_blocktype4(self):
        block_ol = "1. This is ordered list item 1\n2. This is ordered list item2."
        self.assertEqual(block_type_ordered_list, block_to_block_type(block_ol))
    
    def test_block_to_blocktype5(self):
        block_ul = "-This is unordered list item 1\n-This is unordered list item2."
        self.assertEqual(block_type_unordered_list, block_to_block_type(block_ul))

    def test_block_to_blocktype6(self):
        block_ul = "*This is unordered list item 1\n*This is unordered list item2."
        self.assertEqual(block_type_unordered_list, block_to_block_type(block_ul))
    
    def test_block_to_blocktype7(self):
        block_paragraph = "This is normal text"
        self.assertEqual(block_type_paragraph, block_to_block_type(block_paragraph))
    
    def test_block_to_blocktype8(self):
        block_false_ol = "2. This ordered list starts wrong.\n3. This ordered list started wrong and is rendered as paragraph"
        self.assertEqual(block_type_paragraph, block_to_block_type(block_false_ol))