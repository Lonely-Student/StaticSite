# test_inline_markdown.py
import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_single(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))
    
    def test_bold_single(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bolded phrase", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" in the middle", TextType.TEXT))
    
    def test_italic_single(self):
        node = TextNode("This is text with an *italic word* here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic word", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" here", TextType.TEXT))
    
    def test_multiple_delimiters(self):
        node = TextNode("Code `block one` and `block two` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("Code ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("block one", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("block two", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode(" here", TextType.TEXT))
    
    def test_no_delimiter(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This is just plain text", TextType.TEXT))
    
    def test_delimiter_at_start(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0], TextNode("Bold", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode(" at the start", TextType.TEXT))
    
    def test_delimiter_at_end(self):
        node = TextNode("At the end is **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0], TextNode("At the end is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
    
    def test_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("Already bold", TextType.BOLD))
    
    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First `code` node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second `code` node", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0], TextNode("First ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" node", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("Already bold", TextType.BOLD))
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
    
    def test_unmatched_delimiter(self):
        node = TextNode("This has an `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_empty_delimiter_content(self):
        node = TextNode("Empty `` delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Empty strings are skipped
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0], TextNode("Empty ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode(" delimiters", TextType.TEXT))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)
    
    def test_extract_markdown_images_none(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_with_links(self):
        text = "![image](https://example.com/img.png) and [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)
    
    def test_extract_markdown_links_single(self):
        text = "Check out [this link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this link", "https://example.com")], matches)
    
    def test_extract_markdown_links_none(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_ignores_images(self):
        text = "![image](https://example.com/img.png) and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)
    
    def test_extract_markdown_links_and_images_mixed(self):
        text = "![img](url1) [link](url2) ![img2](url3)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("img", "url1"), ("img2", "url3")], images)
        self.assertListEqual([("link", "url2")], links)
    
    def test_extract_markdown_empty_alt_text(self):
        text = "![](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/img.png")], matches)
    
    def test_extract_markdown_empty_anchor_text(self):
        text = "[](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)
    
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
    
    def test_split_images_single(self):
        node = TextNode(
            "Text with ![one image](https://example.com/img.png) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("one image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_at_start(self):
        node = TextNode(
            "![image](https://example.com/img.png) at start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" at start", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_at_end(self):
        node = TextNode(
            "At end ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("At end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_no_images(self):
        node = TextNode("Text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Text with no images", TextType.TEXT)], new_nodes)
    
    def test_split_images_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Already bold", TextType.BOLD)], new_nodes)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_single(self):
        node = TextNode(
            "Check [this link](https://example.com) out",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("this link", TextType.LINK, "https://example.com"),
                TextNode(" out", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_at_start(self):
        node = TextNode(
            "[link](https://example.com) at start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" at start", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_at_end(self):
        node = TextNode(
            "At end [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("At end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_no_links(self):
        node = TextNode("Text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Text with no links", TextType.TEXT)], new_nodes)
    
    def test_split_links_non_text_node(self):
        node = TextNode("Already italic", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Already italic", TextType.ITALIC)], new_nodes)
    
    def test_split_links_ignores_images(self):
        node = TextNode(
            "![image](https://example.com/img.png) [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Should only split on the link, leaving the image markdown intact
        self.assertListEqual(
            [
                TextNode("![image](https://example.com/img.png) ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("Text with ![img](url1)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More ![img2](url2) text", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text_type, TextType.IMAGE)

    def test_text_to_textnodes_full(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("This is just plain text", TextType.TEXT)], nodes)
    
    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_only_italic(self):
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_only_code(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_only_image(self):
        text = "This is an ![image](https://example.com/img.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_only_link(self):
        text = "This is a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_multiple_same_type(self):
        text = "**bold1** and **bold2** here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_mixed_formatting(self):
        text = "**bold** *italic* `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_image_and_link(self):
        text = "![img](url1) [link](url2)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "url1"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual([], nodes)
    
    def test_text_to_textnodes_complex(self):
        text = "Start **bold with *italic* inside** `code` ![img](url) [link](url) end"
        nodes = text_to_textnodes(text)
        # This tests that the order matters - bold is processed first, 
        # so the italic inside won't be split separately
        self.assertTrue(any(node.text_type == TextType.BOLD for node in nodes))
        self.assertTrue(any(node.text_type == TextType.CODE for node in nodes))
        self.assertTrue(any(node.text_type == TextType.IMAGE for node in nodes))
        self.assertTrue(any(node.text_type == TextType.LINK for node in nodes))

if __name__ == "__main__":
    unittest.main()