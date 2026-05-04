import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = repr(LeafNode("p", "This is a test value"))
        node2 = repr(LeafNode("p", "This is a test value"))
        node3 = repr(
            LeafNode(
                "p",
                "This is test text",
                {"href": "https://www.google.com"},
            )
        )
        node4 = repr(
            LeafNode(
                "p",
                "This is test text",
                {"href": "https://www.google.com"},
            )
        )
        node5 = LeafNode(
            "a",
            "This is test text",
            {"href": "https://www.google.com", "target": "blank"},
        )
        node5_html = (
            '<a href="https://www.google.com" target="blank">This is test text</a>'
        )
        node5_to_html = node5.to_html()
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertEqual(node5_html, node5_to_html)

    def test_not_eq(self):
        node = repr(LeafNode("p", "This is a test value"))
        node2 = repr(LeafNode("p", "This is a test value"))
        node3 = repr(
            LeafNode(
                "p",
                "This is test text",
                {"href": "https://www.google.com"},
            )
        )
        node4 = repr(
            LeafNode(
                "p",
                "This is test text",
                {"href": "https://www.google.com"},
            )
        )
        node5 = repr(
            LeafNode(
                "a",
                "This is test text",
                {"href": "https://www.google.com", "target": "blank"},
            )
        )
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node2, node5)

    def test_to_html(self):
        node = repr(
            LeafNode(
                "p",
                "This is test text",
                {"href": "https://www.google.com", "target": "blank"},
            )
        )
        node2 = repr(
            LeafNode(
                "p",
                "This is test text",
                {"href": "https://www.google.com"},
            )
        )
        node3 = repr(
            LeafNode(
                "p",
                "This is test text",
                {"href": "https://www.google.com"},
            )
        )
        self.assertNotEqual(node, node2)
        self.assertEqual(node2, node3)


if __name__ == "__main__":
    unittest.main()
