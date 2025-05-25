import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode(tag="p", value="Hello", props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_prop_dict(self):
        node = HTMLNode(tag="h1", value="This is my header", props={})
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_multi_prop(self):
        node = HTMLNode(tag="h1", value="This is my header", props={ "href": "https://www.google.com", "target": "_blank",})
        result = node.props_to_html()
        self.assertEqual(result, f' href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_lead_to_html_a(self):
        node = LeafNode("a", "link", {"href": "https://starwars.com"})
        self.assertEqual(node.to_html(), '<a href="https://starwars.com">link</a>')

    def test_leaf_with_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_with_empty_value_raises_error(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image", "width": "500"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_with_multiple_attributes(self):
        node = LeafNode("img", "image content", {"src": "image.jpg", "alt": "An image", "width": "500"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image" width="500">image content</img>')

    def test_leaf_span_tag(self):
        node = LeafNode("span", "Some text", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Some text</span>')

class TestParentNode(unittest.TestCase):
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
    def test_to_html_with_more_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("span", "baby")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>baby</span></div>")
    
    def test_to_html_with_leaf_parent_children(self):
        leaf_node = LeafNode("span", "baby")
        another_leaf_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [another_leaf_node, leaf_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>baby</span></div>")

    def test_to_html_with_parent_prop(self):
        props = {"prop1": "value1"}
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props)
        self.assertEqual(parent_node.to_html(), '<div prop1="value1"><span>child</span></div>')

    def test_none_tag_raises_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("span", "child")])
            node.to_html()

    def test_none_children_raises_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()

    def test_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_multiple_props(self):
        props = {"class": "container", "id": "main", "data-test": "value"}
        parent_node = ParentNode("div", [LeafNode("span", "content")], props)
        self.assertEqual(
            parent_node.to_html(), 
            '<div class="container" id="main" data-test="value"><span>content</span></div>'
        )

    def test_complex_structure(self):
        # Create a complex structure with multiple levels and siblings
        deep_leaf = LeafNode("em", "emphasized")
        p_with_em = ParentNode("p", [LeafNode(None, "Text with "), deep_leaf, LeafNode(None, " words.")])
        header = ParentNode("header", [LeafNode("h1", "Title")])
        article = ParentNode("article", [p_with_em, LeafNode("p", "Another paragraph")])
        body = ParentNode("body", [header, article])
        
        expected = "<body><header><h1>Title</h1></header><article><p>Text with <em>emphasized</em> words.</p><p>Another paragraph</p></article></body>"
        self.assertEqual(body.to_html(), expected)

if __name__ == "__main__":
    unittest.main()