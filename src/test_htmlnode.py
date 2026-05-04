import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = repr(HTMLNode())
        node2 = repr(HTMLNode())
        node3 = repr(
            HTMLNode(
                "p",
                "This is test text",
                [node2, node],
                {"href": "https://www.google.com"},
            )
        )
        node4 = repr(
            HTMLNode(
                "p",
                "This is test text",
                [node2, node],
                {"href": "https://www.google.com"},
            )
        )
        node5 = HTMLNode(
            "p",
            "This is test text",
            [node2, node],
            {"href": "https://www.google.com", "target": "blank"},
        )
        node5_html = ' href="https://www.google.com" target="blank"'
        node5_to_html = node5.props_to_html()
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertEqual(node5_html, node5_to_html)

    def test_not_eq(self):
        node = repr(HTMLNode())
        node2 = repr(HTMLNode())
        node3 = repr(
            HTMLNode(
                "p",
                "This is test text",
                [node2, node],
                {"href": "https://www.google.com"},
            )
        )
        node4 = repr(
            HTMLNode(
                "p",
                "This is test text",
                [node2, node],
                {"href": "https://www.google.com"},
            )
        )
        node5 = repr(HTMLNode("p", "This is test text"))
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node2, node5)

    def test_props_to_html(self):
        node = repr(
            HTMLNode(
                "p",
                "This is test text",
                [HTMLNode()],
                {"href": "https://www.google.com", "target": "blank"},
            )
        )
        node2 = repr(
            HTMLNode(
                "p",
                "This is test text",
                [HTMLNode()],
                {"href": "https://www.google.com"},
            )
        )
        node3 = repr(
            HTMLNode(
                "p",
                "This is test text",
                [HTMLNode()],
                {"href": "https://www.google.com"},
            )
        )
        self.assertNotEqual(node, node2)
        self.assertEqual(node2, node3)


if __name__ == "__main__":
    unittest.main()
