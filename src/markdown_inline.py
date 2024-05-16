import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code
)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        new_nodes.extend(recursive_split(node.text))

    return new_nodes
    
def recursive_split(text: str, start: int = 0, nesting_level: int = 0, parent_type: str = text_type_text):
    nodes = []
    i = start

    while i < len(text):
        next_delimiter_pos, next_delimiter, next_delimiter_type = find_next_delimiter(text, i)  

        if not next_delimiter:
            nesting_level -= 1
            nodes.append(TextNode(text[i:], parent_type))
            break

        if i < next_delimiter_pos:
            nodes.append(TextNode(text[i:next_delimiter_pos], parent_type))
        
        i = next_delimiter_pos + len(next_delimiter)
        nesting_level += 1
        end_delimiter_pos = find_matching_delimiter(text, i, next_delimiter, nesting_level)

        if end_delimiter_pos == -1:
            raise ValueError(f"Invalid Markdown Syntax: Missing ending delimiter {next_delimiter}.")

        nested_nodes = recursive_split(text[i:end_delimiter_pos], 0, nesting_level, next_delimiter_type)
        nodes.extend(nested_nodes)
        
        nesting_level -= 1
        i = end_delimiter_pos + len(next_delimiter)

    return nodes

def find_next_delimiter(text: str, start: int):
    for i in range(start, len(text)):
        if text[i] == "*" and text[i+1] == "*":
            return i, "**", text_type_bold
        elif text[i] == "*":
            return i, "*", text_type_italic
        elif text[i] == "`":
            return i, "`", text_type_code
    return None, None, None

def find_matching_delimiter(text: str, start: int, delimiter: str, nesting_level: int = 0):
    if nesting_level < 2:
        return text.rfind(delimiter, start, len(text))
    else:
        return text.find(delimiter, start, len(text))
        
def extract_markdown_images(text: str) -> list[tuple[str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str]]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        if old_node.text == "":
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        old_text = old_node.text
        for image_tup in images:
            splits = old_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            split_nodes = []
            if splits[0] != "":
                split_nodes.append(TextNode(splits[0], text_type_text))
            
            split_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
            old_text = splits[1]

            new_nodes.extend(split_nodes)
        if old_text != "":
            new_nodes.append(TextNode(old_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != text_type_text:
                new_nodes.append(old_node)
                continue
            if old_node.text == "":
                continue
            links = extract_markdown_links(old_node.text)
            if len(links) == 0:
                new_nodes.append(old_node)
                continue
            old_text = old_node.text
            for link_tup in links:
                splits = old_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                split_nodes = []
                if splits[0] != "":
                    split_nodes.append(TextNode(splits[0], text_type_text))
                
                split_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
                old_text = splits[1]

                new_nodes.extend(split_nodes)
            if old_text != "":
                new_nodes.append(TextNode(old_text, text_type_text))
        return new_nodes

def text_to_textnode(text: str) -> list[TextNode]:
    nodes = []
    text_node = [TextNode(text, text_type_text, None)]

    nodes = split_nodes_image(text_node)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)

    return nodes