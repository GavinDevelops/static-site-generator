from htmlnode import LeafNode
from textnode import TextNode
import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode(
                "img", "", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception(
                f"Error converting TextNode of type {text_node.text_type} to HTMLNode: Invalid type"
            )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            print(f"text type: {text_type}")
            print(sections)
            raise Exception("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], "text", None))
            else:
                split_nodes.append(TextNode(sections[i], text_type, None))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        og_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for alt_text, url in images:
            sections = og_text.split(f"![{alt_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], "text", None))
            new_nodes.append(TextNode(alt_text, "image", url))
            og_text = sections[1]
        if og_text != "":
            new_nodes.append(TextNode(og_text, "text", None))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        og_text = node.text
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link, url in links:
            sections = og_text.split(f"[{link}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], "text", None))
            new_nodes.append(TextNode(link, "link", url))
            og_text = sections[1]
        if og_text != "":
            new_nodes.append(TextNode(og_text, "text", None))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, "text", None)]
    text_types = {"bold": "**", "italic": "*", "code": "`"}
    for text_type in text_types:
        nodes = split_nodes_delimiter(nodes, text_types[text_type], text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def main():
    test = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(test)
    print("[")
    for node in nodes:
        print(f"    {node}")
    print("]")


if __name__ == "__main__":
    main()
