import unittest
from htmlnode import ParentNode, LeafNode

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
    
    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(), 
            '<div class="container"><span>child</span></div>'
        )
    
    def test_to_html_nested_parents(self):
        inner_leaf = LeafNode("span", "inner")
        inner_parent = ParentNode("div", [inner_leaf])
        outer_parent = ParentNode("section", [inner_parent])
        self.assertEqual(
            outer_parent.to_html(),
            "<section><div><span>inner</span></div></section>",
        )
    
    def test_to_html_many_children(self):
        children = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3"),
        ]
        parent_node = ParentNode("ul", children)
        self.assertEqual(
            parent_node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>",
        )
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("tag", str(context.exception))
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("children", str(context.exception))
    
    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
    
    def test_complex_nesting(self):
        # Create a complex nested structure
        deep_leaf = LeafNode("strong", "Deep text")
        level3 = ParentNode("p", [deep_leaf])
        level2 = ParentNode("div", [level3], {"class": "level2"})
        level1 = ParentNode("section", [level2])
        
        self.assertEqual(
            level1.to_html(),
            '<section><div class="level2"><p><strong>Deep text</strong></p></div></section>',
        )
    
    def test_mixed_parent_and_leaf_children(self):
        parent_child = ParentNode("div", [LeafNode("span", "nested")])
        leaf_child = LeafNode("p", "paragraph")
        parent = ParentNode("section", [parent_child, leaf_child])
        
        self.assertEqual(
            parent.to_html(),
            "<section><div><span>nested</span></div><p>paragraph</p></section>",
        )

if __name__ == "__main__":
    unittest.main()