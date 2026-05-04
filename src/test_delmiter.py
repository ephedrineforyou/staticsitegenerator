import unittest

from blocks import BlockType, block_to_block_type
from delimiter import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):
    def test_middle_delim(self):
        old_nodes = [
            TextNode("This has a `code` delimiter in the middle", TextType.TEXT)
        ]
        expected_return = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" delimiter in the middle", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

        self.assertEqual(expected_return, new_nodes)

    def test_no_delim(self):
        old_nodes = [TextNode("This has no delimiters", TextType.TEXT)]
        expected_return = [
            TextNode("This has no delimiters", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

        self.assertEqual(expected_return, new_nodes)

    def test_multiple_delim(self):
        old_nodes = [
            TextNode(
                "This has a `code` delimiter and a **bold** delimiter after it, and finally an *italic* delimiter",
                TextType.TEXT,
            )
        ]
        expected_return = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" delimiter and a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" delimiter after it, and finally an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" delimiter", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(old_nodes, "`", TextType.CODE),
                "**",
                TextType.BOLD,
            ),
            "*",
            TextType.ITALIC,
        )

        self.assertEqual(expected_return, new_nodes)

    def test_non_text(self):
        old_nodes = [TextNode("This is an image", TextType.IMAGE)]
        expected_return = [TextNode("This is an image", TextType.IMAGE)]

        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(old_nodes, "`", TextType.CODE),
                "**",
                TextType.BOLD,
            ),
            "*",
            TextType.ITALIC,
        )
        self.assertEqual(expected_return, new_nodes)

    def test_multiple_old_nodes(self):
        old_nodes = [
            TextNode(
                "This has a `code` delimiter and a **bold** delimiter after it, and finally an *italic* delimiter",
                TextType.TEXT,
            ),
            TextNode("This is a simple node", TextType.TEXT),
        ]
        expected_return = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" delimiter and a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" delimiter after it, and finally an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" delimiter", TextType.TEXT),
            TextNode("This is a simple node", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(old_nodes, "`", TextType.CODE),
                "**",
                TextType.BOLD,
            ),
            "*",
            TextType.ITALIC,
        )

        self.assertEqual(expected_return, new_nodes)

    def test_exception(self):
        old_nodes = [TextNode("This has unequal *delimiters", TextType.TEXT)]

        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "*", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        node_text = "This *is* _text_ `with` **a** [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png)"

        new_nodes = text_to_textnodes(node_text)

        self.assertListEqual(
            [
                TextNode("This ", TextType.TEXT),
                TextNode("is", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("with", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("a", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md_block = """
# Heading Test
"""

        type_check = block_to_block_type(md_block.strip())
        self.assertEqual(type_check, BlockType.HEADING)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
