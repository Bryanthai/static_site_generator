import re
import textwrap
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
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value=text_node.text, props={"src":text_node.url})
    
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
        if link_list == []:
            new_nodes.append(node)
        for image in link_list:
            temp_list = str.split(f"![{image[0]}]({image[1]})")
            new_nodes.append(TextNode(temp_list[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode("", TextType.IMAGE, image[1]))
            str = temp_list[1]
    return new_nodes

def split_nodes_link(node):
    new_nodes = []
    str = node.text
    link_list = extract_markdown_link(node.text)
    if link_list == []:
        new_nodes.append(node)
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
    new_nodes = split_nodes_delimiter(new_nodes, "```", TextType.CODE_TEXT)
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
        if str == "":
            continue
        if str.startswith(">") == False:
            return False
    return True

def checkforlineul(text):
    list = text.split("\n")
    for str in list:
        str = str.strip()
        if str == "":
            continue
        if str.startswith("- ") == False:
            return False
    return True


def block_to_block_type(block):
    if checkforlinequote(block):
        return BlockType.QUOTE
    if checkforlineul(block):
        return BlockType.UNORDERED_LIST
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if checkheader(block):
        return BlockType.HEADING
    if check_list_num(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def strip_ordered_list_left(text):
    return re.sub(r"\d+. ", "", text, 1)

def text_to_children(text, block_type):
    if block_type == BlockType.CODE:
        parent_node = ParentNode("pre", [])
        if text.endswith("````"):
            raise Exception("Invalid markdown syntax")
        text = text.strip("`")
        text = text.lstrip()
        tnode = TextNode(text, TextType.CODE_TEXT)
        hnode = text_node_to_html_node(tnode)
        parent_node.children.append(hnode)
        return parent_node
    elif block_type == BlockType.ORDERED_LIST:
        text_list = text.split("\n")
        if text_list[-1] == "":
            text_list.pop()
        parent_node = ParentNode("ol", [])
        for text in text_list:
            if text == "":
                continue
            text = strip_ordered_list_left(text)
            text = re.sub("\n", " ", text)
            tnodes_list = text_to_textnodes(text)
            hnode_list = []
            for tnode in tnodes_list:
                hnode_list.append(text_node_to_html_node(tnode))
            new_pnode = ParentNode("li", hnode_list)
            parent_node.children.append(new_pnode)
        return parent_node
    elif block_type == BlockType.UNORDERED_LIST:
        text_list = text.split("\n")
        if text_list[-1] == "":
            text_list.pop()
        parent_node = ParentNode("ul", [])
        for text in text_list:
            text = text.lstrip("- ")
            text = re.sub("\n", " ", text)
            tnodes_list = text_to_textnodes(text)
            hnode_list = []
            for tnode in tnodes_list:
                hnode_list.append(text_node_to_html_node(tnode))
            new_pnode = ParentNode("li", hnode_list)
            parent_node.children.append(new_pnode)
        return parent_node
    elif block_type == BlockType.QUOTE:
        text_list = text.split("\n")
        parent_node = ParentNode("blockquote", [])
        for text in text_list:
            text = text.lstrip("> ")
            text = re.sub("\n", " ", text)
            if text == "":
                parent_node.children.append(LeafNode(" "))
                continue
            tnodes_list = text_to_textnodes(text)
            for tnode in tnodes_list:
                parent_node.children.append(text_node_to_html_node(tnode))
        return parent_node
    elif block_type == BlockType.HEADING:
        text = text.lstrip("# ")
        text = re.sub("\n", " ", text)
        tnodes_list = text_to_textnodes(text)
        parent_node = ParentNode("h1", [])
        for tnode in tnodes_list:
            parent_node.children.append(text_node_to_html_node(tnode))
        return parent_node
    elif block_type == BlockType.PARAGRAPH:
        text = re.sub("\n", " ", text)
        tnodes_list = text_to_textnodes(text)
        parent_node = ParentNode("p", [])
        for tnode in tnodes_list:
            parent_node.children.append(text_node_to_html_node(tnode))
        return parent_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    new_list = []
    root_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        pnode = text_to_children(block, block_type)
        new_list.append(pnode)
    root_node.children = new_list
    return root_node

def extract_title(markdown):
    block_list = markdown_to_block(markdown)
    for block in block_list:
        if block.startswith("# "):
            return block.lstrip("# ")
    raise Exception("Header required in markdown file")