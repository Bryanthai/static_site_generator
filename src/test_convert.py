import unittest

from convert import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_link
from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_2(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        test_list = [TextNode("This is text with a ", TextType.NORMAL_TEXT),
                     TextNode("code block", TextType.CODE_TEXT),
                     TextNode(" word", TextType.NORMAL_TEXT),
                    ]
        self.assertEqual(new_nodes, test_list)

    def test_split_2(self):
        node = TextNode("**bold****italic**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        test_list = [TextNode("bold", TextType.BOLD_TEXT),
                     TextNode("italic", TextType.BOLD_TEXT),
                    ]
        self.assertEqual(new_nodes, test_list)
    
    def test_split_3(self):
        node = TextNode("", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        test_list = []
        self.assertEqual(new_nodes, test_list)
    
    def test_split_4(self):
        node = TextNode("**bold****italic**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.BOLD_TEXT)
        test_list = [TextNode("**bold****italic**", TextType.NORMAL_TEXT)]
        self.assertEqual(new_nodes, test_list)

    def test_split_5(self):
        node = TextNode("**'bold'****_italic_**", TextType.NORMAL_TEXT)
        node1 = TextNode("this is _italic_", TextType.NORMAL_TEXT)
        node2 = TextNode("**bolded**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([node, node1, node2], "_", TextType.ITALIC_TEXT)
        test_list = [TextNode("**'bold'****", TextType.NORMAL_TEXT),
                     TextNode("italic", TextType.ITALIC_TEXT),
                     TextNode("**", TextType.NORMAL_TEXT),
                     TextNode("this is ", TextType.NORMAL_TEXT),
                     TextNode("italic", TextType.ITALIC_TEXT),
                     TextNode("**bolded**", TextType.BOLD_TEXT),
                    ]
        self.assertEqual(new_nodes, test_list)
    
    def test_split_6(self):
        node = TextNode("****", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        test_list = []
        self.assertEqual(new_nodes, test_list)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_link(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_link(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)