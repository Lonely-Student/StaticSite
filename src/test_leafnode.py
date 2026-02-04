import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")
    
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("a", "Link", {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.boot.dev" target="_blank">Link</a>'
        )
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is a heading")
        self.assertEqual(node.to_html(), "<h1>This is a heading</h1>")
    
    def test_leaf_to_html_span_with_class(self):
        node = LeafNode("span", "Highlighted text", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Highlighted text</span>')
    
    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(repr(node), "LeafNode(p, Hello, {'class': 'text'})")

if __name__ == "__main__":
    unittest.main()