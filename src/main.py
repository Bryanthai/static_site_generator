from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

def main():
    new_node = TextNode("BOILER TEXT", TextType.LINK, "cockandballstorture.net")
    print(repr(new_node))

main()