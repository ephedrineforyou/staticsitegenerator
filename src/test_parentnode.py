import unittest

from htmlnode import LeafNode, ParentNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_eq(self):
        node = repr(
            ParentNode(
                "p",
                [
                    LeafNode(
                        "p",
                        "This is test text",
                        {"href": "https://www.google.com"},
                    )
                ],
            )
        )
        node2 = repr(
            ParentNode(
                "p",
                [
                    LeafNode(
                        "p",
                        "This is test text",
                        {"href": "https://www.google.com"},
                    )
                ],
            )
        )
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
