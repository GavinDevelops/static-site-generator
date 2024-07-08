from htmlnode import ParentNode
from inline_markdown import text_node_to_html_node, text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    blocks = []
    for block in split_blocks:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks


def block_to_block_type(block):
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    split_block = block.split("\n")
    quote_count, unordered_count, ordered_count = 0, 0, 0
    for line in split_block:
        if line.startswith(">"):
            quote_count += 1
        elif line.startswith("* ") or line.startswith("- "):
            unordered_count += 1
        elif line.startswith(f"{ordered_count + 1}. "):
            ordered_count += 1
    if quote_count == len(split_block):
        return block_type_quote
    elif unordered_count == len(split_block):
        return block_type_unordered_list
    elif ordered_count == len(split_block):
        return block_type_ordered_list
    return block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        nodes.append(html_node)
    return ParentNode("div", nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return block_paragraph_to_html_node(block)
    if block_type == block_type_ordered_list:
        return block_ordered_list_to_html_node(block)
    if block_type == block_type_unordered_list:
        return block_unordered_list_to_html_node(block)
    if block_type == block_type_code:
        return block_code_to_html_node(block)
    if block_type == block_type_quote:
        return block_quote_to_html_node(block)
    if block_type == block_type_heading:
        return block_heading_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def block_heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def block_paragraph_to_html_node(block):
    lines = block.split("\n")
    parapraph = " ".join(lines)
    children = text_to_children(parapraph)
    return ParentNode("p", children)


def block_code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def block_quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def block_unordered_list_to_html_node(block):
    split = block.split("\n")
    html_items = []
    for item in split:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def block_ordered_list_to_html_node(block):
    split = block.split("\n")
    html_items = []
    for item in split:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def main():
    block_heading_to_html_node("#### testing")


if __name__ == "__main__":
    main()
