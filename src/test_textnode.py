import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "www.pornhub.com")
        node2 = TextNode("This is a text node", TextType.LINK, "www.pornhub.com")
        self.assertEqual(node, node2)

    def test_non_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "www.pornhub.com")
        node2 = TextNode("This is a text node", TextType.LINK, "www.pornhub.com")
        self.assertNotEqual(node, node2)
    
    def test_non_eq_2(self):
        node = TextNode("This is a", TextType.BOLD_TEXT, "www.pornhub.com")
        node2 = TextNode("This is a text node", TextType.LINK, "www.pornhub.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()