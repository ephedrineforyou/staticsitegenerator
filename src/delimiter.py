import re

from blocks import BlockType, block_to_block_type
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        if not len(split_text) % 2:
            raise Exception(
                "Node text is not in a valid markdown format. Missing a closing delimiter."
            )

        for i in range(len(split_text)):
            if split_text[i]:
                if i % 2:
                    new_nodes.append(TextNode(split_text[i], text_type))
                else:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    # Iterate through all nodes in old_nodes, splitting each node into Text and Link nodes
    for node in old_nodes:
        # Check if the node is already categorized as a non-text type and add it to new nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract a list of tuples containing (Alt Text, Image Link) from the provided node.text
        image_tuples = extract_markdown_images(node.text)

        # Set a string to the initial node.text to be modified after splitting image links.  This variable
        # will contain the remaining text after each image link split.
        remaining_text = node.text

        if image_tuples:
            for image_tuple in image_tuples:
                # Pull alt text and image link from the current tuple
                image_alt, image_link = image_tuple[0], image_tuple[1]
                split_text = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                remaining_text = split_text[1]

                # Append the leading text node if it is not ""
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))

                # Append the image node from the extracted image tuple
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            # Check for trailing text after splitting all images and add a node containing the remaining text
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        # If no image_tuples were found, add the current node back to new_nodes and move on to the next node
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []

    # Iterate through all nodes in old_nodes, splitting each node into Text and Link nodes
    for node in old_nodes:
        # Check if the node is already categorized as a non-text type and add it to new nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract a list of tuples containing (Alt Text, Link URL) from the provided node.text
        link_tuples = extract_markdown_links(node.text)

        # Set a string to the initial node.text to be modified after splitting image links.  This variable
        # will contain the remaining text after each image link split.
        remaining_text = node.text

        if link_tuples:
            for link_tuple in link_tuples:
                # Pull alt text and image link from the current tuple
                link_alt, link_url = link_tuple[0], link_tuple[1]
                split_text = remaining_text.split(f"[{link_alt}]({link_url})", 1)
                remaining_text = split_text[1]

                # Append the leading text node if it is not ""
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))

                # Append the image node from the extracted image tuple
                new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            # Check for trailing text after splitting all images and add a node containing the remaining text
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        # If no image_tuples were found, add the current node back to new_nodes and move on to the next node
        else:
            new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)

    new_nodes = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        split_nodes_delimiter([text_node], "`", TextType.CODE),
                        "**",
                        TextType.BOLD,
                    ),
                    "*",
                    TextType.ITALIC,
                ),
                "_",
                TextType.ITALIC,
            )
        )
    )

    return new_nodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_parsed = []

    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] != "":
            blocks_parsed.append(blocks[i])

    return blocks_parsed


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    markdown_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                heading_split = block.split(" ", 1)
                hash_count = heading_split[0].count("#")
                if (
                    len(heading_split) < 2
                    or hash_count == 0
                    or hash_count > 6
                    or not heading_split[0].strip("#") == ""
                ):
                    raise Exception(
                        "Incorrect heading format encountered. Use 1-6 # followed by one space followed by the heading text."
                    )
                children_nodes = text_to_children(heading_split[1])
                markdown_nodes.append(ParentNode(f"h{hash_count}", children_nodes))
            case BlockType.CODE:
                code_split = block.split("```")
                if len(code_split) != 3 or code_split[0] != "" or code_split[2] != "":
                    raise IndexError(
                        "Code block incorrectly formatted. A code block must be fenced by ''' on the first and last lines"
                    )
                child_node = text_node_to_html_node(
                    TextNode(code_split[1].lstrip("\n"), TextType.TEXT)
                )
                markdown_nodes.append(
                    ParentNode("pre", [ParentNode("code", [child_node])])
                )
            case BlockType.QUOTE:
                quote_split = block.split("\n")
                cleaned = [line.lstrip(">").lstrip() for line in quote_split]
                combined_text = " ".join(cleaned)
                children_nodes = text_to_children(combined_text)
                markdown_nodes.append(ParentNode("blockquote", children_nodes))
            case BlockType.UNORDERED_LIST:
                ul_split = block.split("\n")
                children_nodes = []
                for line in ul_split:
                    cleaned = line[2:]
                    children_nodes.append(ParentNode("li", text_to_children(cleaned)))
                markdown_nodes.append(ParentNode("ul", children_nodes))
            case BlockType.ORDERED_LIST:
                ol_split = block.split("\n")
                children_nodes = []
                for line in ol_split:
                    cleaned = line[(line.index(". ") + 2) :]
                    children_nodes.append(ParentNode("li", text_to_children(cleaned)))
                markdown_nodes.append(ParentNode("ol", children_nodes))
            case BlockType.PARAGRAPH:
                paragraph_split = block.split("\n")
                cleaned = [line.strip() for line in paragraph_split]
                combined_text = " ".join(cleaned)
                children_nodes = text_to_children(combined_text)
                markdown_nodes.append(ParentNode("p", children_nodes))

    return ParentNode("div", markdown_nodes)
