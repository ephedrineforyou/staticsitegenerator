from textnode import TextNode, TextType


def main():
    print("hello world")
    test_node = TextNode("Anchor Text", TextType.LINK, "http://www.google.com")
    print(test_node)


if __name__ == "__main__":
    main()
