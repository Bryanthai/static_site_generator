import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href":f"{text_node.url["href"]}"})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value=text_node.text, props={"src":f"{text_node.url["src"]}", "alt":f"{text_node.url["alt"]}"})
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    split_list = []
    total_hit = 0
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT or delimiter == "":
            new_nodes.append(node)
            continue
        total_hit = node.text.count(delimiter)
        if total_hit % 2 != 0:
            raise Exception("Invalid Markdown syntax")
        total_hit = 0
        split_list = node.text.split(delimiter)
        for index in range(len(split_list)):
            if split_list[index] == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(split_list[index], node.text_type))
            else:
                new_nodes.append(TextNode(split_list[index], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_link(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    pass