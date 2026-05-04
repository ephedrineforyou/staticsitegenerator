import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node6 = TextNode("This is a link node", TextType.LINK, "http://www.google.com")
        node7 = TextNode("This is a link node", TextType.LINK, "http://www.google.com")
        self.assertEqual(node, node2)
        self.assertEqual(node6, node7)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is another text node", TextType.BOLD)
        node4 = TextNode("This is a code node", TextType.CODE)
        node5 = TextNode(
            "This is an image node", TextType.IMAGE, "http://www.google.com"
        )
        node7 = TextNode("This is a link node", TextType.LINK, "http://www.google.com")
        node8 = TextNode("This is a link node", TextType.LINK)

        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node7, node8)

    def test_url_checks(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.google.com")
        node6 = TextNode("This is a link node", TextType.LINK, "http://www.google.com")
        node7 = TextNode("This is a link node", TextType.LINK, "http://www.google.com")

        self.assertNotEqual(node, node2)
        self.assertEqual(node6, node7)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "http://www.google.com"})

    def test_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "http://www.google.com", "alt": "This is an image"}
        )


if __name__ == "__main__":
    unittest.main()
