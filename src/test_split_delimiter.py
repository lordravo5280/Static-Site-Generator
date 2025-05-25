import unittest
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_blocks

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("Hello world", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Hello world")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_one_delimiter_pair(self):
        node = TextNode("Hello **world**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.BOLD)
    
    def test_multiple_delimiter_pairs(self):
        node = TextNode("Hello **bold** and `code` text", TextType.TEXT)
        # First split for bold
        result1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split for code
        result2 = split_nodes_delimiter(result1, "`", TextType.CODE)
        
        self.assertEqual(len(result2), 5)
        self.assertEqual(result2[0].text, "Hello ")
        self.assertEqual(result2[0].text_type, TextType.TEXT)
        self.assertEqual(result2[1].text, "bold")
        self.assertEqual(result2[1].text_type, TextType.BOLD)
        self.assertEqual(result2[2].text, " and ")
        self.assertEqual(result2[2].text_type, TextType.TEXT)
        self.assertEqual(result2[3].text, "code")
        self.assertEqual(result2[3].text_type, TextType.CODE)
        self.assertEqual(result2[4].text, " text")
        self.assertEqual(result2[4].text_type, TextType.TEXT)

    def test_unbalanced_delimiter_pair(self):
        node = TextNode("Hello **world", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue("No closing delimiter" in str(context.exception))

    def test_mismatched_delimiters(self):
        node = TextNode("Hello **bold_", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Also test the other way around
        node = TextNode("Hello _bold**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_non_text_node_unchanged(self):
        node = TextNode("Hello world", TextType.BOLD)  # Already BOLD
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Hello world")
        self.assertEqual(result[0].text_type, TextType.BOLD)

class TestSplitImagesAndLinks(unittest.TestCase):
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
            "This is text with a link [to boot dev](https://www.boot.dev) and another link [to youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode(
            "This is text with a link [to boot dev]",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link [to boot dev]", TextType.TEXT),
                            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
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

    def test_excess_newlines_markdown_to_blocks(self):
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

if __name__ == "__main__":
    unittest.main()