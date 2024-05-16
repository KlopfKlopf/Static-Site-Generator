block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    
    splits = markdown.split("\n")
    block_text = ""
    for split in splits:
        if split != "":
            block_text += split + "\n"
            continue
        
        if block_text != "":
            blocks.append(block_text.strip())
            block_text = ""
    
    if block_text != "":
        blocks.append(block_text.strip())
    return blocks

def block_to_block_type(block):
    if (block.startswith("#")
        or block.startswith("##")
        or block.startswith("###")
        or block.startswith("####")
        or block.startswith("#####")
        or block.startswith("######")
        ):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif block.startswith(">"):
        if pattern_at_each_line(block, ">"):
            return block_type_quote    
    elif block.startswith("*"):
        if pattern_at_each_line(block, "*"):
            return block_type_unordered_list
    elif block.startswith("-"):
        if pattern_at_each_line(block, "-"):
            return block_type_unordered_list
    elif block.startswith("1."):
        if pattern_at_each_line(block, "1."):
            return block_type_ordered_list
    
    return block_type_paragraph


def pattern_at_each_line(block, pattern):
    i = 1
    for line in block.splitlines():
        if pattern != "1.":
            if not line.startswith(pattern):
                return False
        else:
            if not line.startswith(f"{i}."):
                return False
            i+=1
    return True