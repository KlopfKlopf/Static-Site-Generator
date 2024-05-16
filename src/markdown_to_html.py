from markdown_block import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list
)
from textnode import text_node_to_html_node
from markdown_inline import text_to_textnode
from htmlnode import ParentNode

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def convert_blockquote_to_htmlnode(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children =text_to_children(content)
    return ParentNode("blockquote", children)


def convert_ul_to_htmlnode(block):
    lines = block.split("\n")
    child_nodes = []
    for i in range(len(lines)):
        text = lines[i].lstrip("-*").strip()
        children = text_to_children(text)
        child_nodes.append(ParentNode("li",children))
    return ParentNode("ul", child_nodes)

def convert_ol_to_htmlnode(block):
    lines = block.split("\n")
    child_nodes = []
    for line in lines:
        if line.strip():
            text = line.split(".", 1)[-1].strip()
            children = text_to_children(text)
            child_nodes.append(ParentNode("li",children))
    return ParentNode("ol", child_nodes)

def convert_code_to_htmlnode(block):
    text = block.strip("```")
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def convert_heading_to_htmlnode(block):
    heading_split = block.split(" ", 1)
    header_num = len(heading_split[0])
    text = heading_split[1].strip()
    children = text_to_children(text)

    return ParentNode(f"h{header_num}", children)

def convert_paragraph_to_htmlnode(block):
    lines = block.split("\n")
    content = " ".join(lines)
    children = text_to_children(content)
    return ParentNode("p", children)

def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_quote:
            html_nodes.append(convert_blockquote_to_htmlnode(block))
        elif block_type == block_type_unordered_list:
            html_nodes.append(convert_ul_to_htmlnode(block))
        elif block_type == block_type_ordered_list:
            html_nodes.append(convert_ol_to_htmlnode(block))
        elif block_type == block_type_code:
            html_nodes.append(convert_code_to_htmlnode(block))
        elif block_type == block_type_heading:
            html_nodes.append(convert_heading_to_htmlnode(block))
        elif block_type == block_type_paragraph:
            html_nodes.append(convert_paragraph_to_htmlnode(block))
    
    return ParentNode("div", html_nodes)

    
