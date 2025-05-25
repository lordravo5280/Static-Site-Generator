import unittest

from textnode import TextNode, TextType
from split_delimiter import text_node_to_html_node, text_to_textnodes
from extract import extract_markdown_images, extract_markdown_links, extract_title


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://tiaa.org")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is not a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://starwars.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")      
        self.assertEqual(html_node.props, {"href": "https://starwars.com"})         

    def test_image(self):
        node = TextNode("this is alt text", TextType.IMAGE, "https://starwars.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")      
        self.assertEqual(html_node.props, {"src": "https://starwars.com", "alt": "this is alt text"})

class TestMarkdownLinksandImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Here are links to [Boot.dev](https://www.boot.dev) and [GitHub](https://github.com)"
        )
        self.assertListEqual([
            ("Boot.dev", "https://www.boot.dev"),
            ("GitHub", "https://github.com")
        ], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This text has no links")
        self.assertListEqual([], matches)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(len(nodes), len(expected))
        
        for i in range(len(nodes)):
            self.assertEqual(nodes[i].text, expected[i].text)
            self.assertEqual(nodes[i].text_type, expected[i].text_type)
            self.assertEqual(nodes[i].url, expected[i].url)
    
    def test_text_to_textnodes_complex(self):
        text = "This is **bold** and _italic_ with `code` and a [link](https://boot.dev) and an ![image](https://example.com/img.png)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png")
        ]

        self.assertEqual(len(nodes), len(expected))

        for i in range(len(nodes)):
            self.assertEqual(nodes[i].text, expected[i].text)
            self.assertEqual(nodes[i].text_type, expected[i].text_type)
            self.assertEqual(nodes[i].url, expected[i].url)

class TestExtractHeader(unittest.TestCase):
    def test_header_extract(self):
        markdown = "# Heading 1"
        markdown_extract = "Heading 1"
        title = extract_title(markdown)
        self.assertEqual(title, markdown_extract)

    def test_header_extract_wrong_number(self):
        with self.assertRaises(Exception):
            title = "## Heading 2"
            extract_title(title)

    def test_header_extract_extra_spaces(self):
        with self.assertRaises(Exception):
            title = "  # Heading 1"
            extract_title(title)            

if __name__ == "__main__":
    unittest.main()