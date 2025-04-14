import unittest
import textwrap
from convert import *
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

    def test_extract_markdown_link_2(self):
        matches = extract_markdown_link(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

    def test_split_images_2(self):
        node = TextNode(
            "This is text with an ![text](cockballs) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.IMAGE, "cockballs"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [text](cock) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.LINK, "cock"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

    def test_split_link_2(self):
        node = TextNode(
            "This is text with an ![text](cock) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link(node)
        self.assertListEqual([TextNode("This is text with an ![text](cock) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL_TEXT)], new_nodes)

    def text_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        check_list = [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
        output_list = text_to_textnodes(text)
        self.assertEqual(check_list, output_list)

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and ```code``` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and ```code``` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_check_ordered_list(self):
        test = """1. lmao
        2. cock
        3. balls
        """
        tf = check_list_num(test)
        self.assertEqual(tf, True)

    def test_check_ordered_list_2(self):
        test = "nigger"
        tf = check_list_num(test)
        self.assertEqual(tf, False)

    def test_blocktype_1(self):
        test = """1. lmao
        2. cock
        """
        type = block_to_block_type(test)
        self.assertEqual(type, BlockType.ORDERED_LIST)

    def test_blocktype_2(self):
        test = """1. lmao
        30. cock
        """
        type = block_to_block_type(test)
        self.assertEqual(type, BlockType.PARAGRAPH)
    
    def test_blocktype_3(self):
        test = textwrap.dedent("""\
            > lmao
            > cock""")
        type = block_to_block_type(test)
        self.assertEqual(type, BlockType.QUOTE)

    def test_blocktype_4(self):
        test = textwrap.dedent("""\
            - lmao
            - cock""")
        type = block_to_block_type(test)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_blocktype_5(self):
        test = textwrap.dedent("""\"\"\"\
                               for int in list:
                               cook his ass.
                               \"\"\"""")
        type = block_to_block_type(test)
        self.assertEqual(type, BlockType.CODE)

    def test_blocktype_6(self):
        test = "#### cock and bllas"
        type = block_to_block_type(test)
        self.assertEqual(type, BlockType.HEADING)

    def test_checklinequote(self):
        test = "> quote"
        isquote = checkforlinequote(test)
        self.assertEqual(isquote, True)

    def test_checklinequote_2(self):
        test = textwrap.dedent("""\
        > quote
        > quote 2
        > quote 3""")
        isquote = checkforlinequote(test)
        self.assertEqual(isquote, True)
    
    def test_checklinequote_3(self):
        test = textwrap.dedent("""\
            > quote
            > quote 2
             > quote 3""")
        isquote = checkforlinequote(test)
        self.assertEqual(isquote, False)

    def test_paragraphs(self):
        md = textwrap.dedent("""\
                               This is **bolded** paragraph
                               text in a p
                               tag here

                               This is another paragraph with _italic_ text and `code` here""")
        node = markdown_to_html_node(md)
        html = node.to_html()
        html = re.sub("\n", " ", html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblocks(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )