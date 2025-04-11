import re
from enum import Enum
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
    new_nodes = []
    for node in old_nodes:
        str = node.text
        link_list = extract_markdown_images(node.text)
        for image in link_list:
            temp_list = str.split(f"![{image[0]}]({image[1]})")
            new_nodes.append(TextNode(temp_list[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            str = temp_list[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        str = node.text
        link_list = extract_markdown_link(node.text)
        for link in link_list:
            temp_list = str.split(f"[{link[0]}]({link[1]})")
            new_nodes.append(TextNode(temp_list[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            str = temp_list[1]
    return new_nodes

def text_to_textnodes(text):
    new_node = TextNode(text, TextType.NORMAL_TEXT)
    new_nodes = split_nodes_link(new_node)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE_TEXT)
    return new_nodes

def markdown_to_block(markdown):
    block_list = []
    new_list = markdown.split("\n\n")
    for block in new_list:
        block.strip()
        if block != "":
            block_list.append(block)
    return block_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def checkheader(text):
    if re.findall(r"^\#{1,6} ", text) == []:
        return False
    return True

def check_list_num(text):
    list = re.findall(r"\d+. ", text)
    if list == []:
        return False
    for i in range (1, len(list)+1):
        if f"{i}. " != list[i-1]:
            return False
    return True

def checkforlinequote(text):
    list = text.split("\n")
    for str in list:
        if str.startswith(">") == False:
            return False
    return True

def checkforlineul(text):
    list = text.split("\n")
    for str in list:
        if str.startswith("- ") == False:
            return False
    return True


def block_to_block_type(block):
    if checkforlinequote(block):
        return BlockType.QUOTE
    if checkforlineul(block):
        return BlockType.UNORDERED_LIST
    if block.startswith("\"\"\"") and block.endswith("\"\"\""):
        return BlockType.UNORDERED_LIST
    if checkheader(block):
        return BlockType.HEADING
    if check_list_num(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH