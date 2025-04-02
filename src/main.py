from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

def main():
    new_node = TextNode("BOILER TEXT", TextType.LINK, "cockandballstorture.net")
    print(repr(new_node))

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
    pass

main()