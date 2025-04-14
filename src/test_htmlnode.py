import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_func_props_to_html(self):
        node = HTMLNode(tag="div",props={"href": "https://www.google.com", "target": "_blank",})
        node_props = node.props_to_html()
        check_string = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node_props, check_string)
    
    def test_func_props_to_html_none(self):
        node = HTMLNode(tag="div")
        node_props = node.props_to_html()
        check_string = ""
        self.assertEqual(node_props, check_string)

    def test_func_leaf_to_html(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_func_leaf_to_html_link(self):
        node = LeafNode(tag="a", value="Hello, world!", props={"href":"www.cbt.com"})
        self.assertEqual(node.to_html(), "<a href=\"www.cbt.com\">Hello, world!</a>")

    def test_func_leaf_to_html_img(self):
        node = LeafNode(tag="img", value="Hello, world!", props={"src":"./xd"})
        self.assertEqual(node.to_html(), "<img src=\"./xd\">Hello, world!</img>")

    def test_func_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_func_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

    def test_func_to_html_r(self):
        child_node_1 = LeafNode(tag="b", value="cock")
        child_node_2 = LeafNode(tag="h", value="and")
        child_node_3 = LeafNode(tag="n", value="balls")
        child_node_4 = LeafNode(tag="m", value="torture")
        parent_node_1 = ParentNode("parent1", [child_node_1, child_node_2])
        parent_node_2 = ParentNode("parent2", [child_node_3])
        parent_node_3 = ParentNode("parent3", [parent_node_1,parent_node_2,child_node_4])
        self.assertEqual(parent_node_3.to_html(), "<parent3><parent1><b>cock</b><h>and</h></parent1><parent2><n>balls</n></parent2><m>torture</m></parent3>")