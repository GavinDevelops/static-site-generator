import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):

    # def test_not_eq(self):
        # node = TextNode("This is a text node", "bold", "google.com")
        # node2 = TextNode("This is a text node", "bold", "test.com")
        # self.assertNotEqual(node, node2)
    def test_print_node(self):
        node = HTMLNode("TBAG tag", "I'm valuable", "chidl", {"href": "balls", "target": "your_mouth"})
        print(node)
        print(node.props_to_html())

    def test_leaf_node(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        node2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        p_tag = "<p>This is a paragraph of text.</p>"
        a_tag = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), p_tag)
        self.assertEqual(node2.to_html(), a_tag)

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        print(node.to_html())

    def test_parent_parent_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode("div", [
                    LeafNode("i", "first recursion i"),
                    LeafNode(None, "first recursion none"),
                    LeafNode("b", "first recursion b"),
                    ParentNode("div", [
                        LeafNode("i", "second recursion i"),
                        LeafNode(None, "second recursion none"),
                        LeafNode("b", "second recursion b"),
                    ])
                ])
            ],
        )

        print(node.to_html())


if __name__ == "__main__":
    unittest.main()
