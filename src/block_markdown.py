from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """Split a markdown document into blocks separated by blank lines."""
    # Split on double newlines (blank lines)
    blocks = markdown.split("\n\n")
    
    # Strip whitespace and filter out empty blocks
    filtered_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            filtered_blocks.append(stripped)
    
    return filtered_blocks

def block_to_block_type(block):
    """Determine the type of a markdown block."""
    lines = block.split("\n")
    
    # Check for heading (1-6 # followed by space)
    if block.startswith(("###### ", "##### ", "#### ", "### ", "## ", "# ")):
        return BlockType.HEADING
    
    # Check for code block (starts with ``` and ends with ```)
    if block.startswith("```") and block.endswith("```") and len(lines) > 1:
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with 1. 2. 3. etc.)
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    
    if is_ordered_list and len(lines) > 0:
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH

def text_to_children(text):
    """Convert inline markdown text to a list of HTMLNode children."""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    # Replace newlines with spaces for paragraphs
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the number of # characters
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    # Get the text after the # and space
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    # Remove the opening and closing ```
    if not block.startswith("```"):
        raise ValueError("Invalid code block")
    
    # Remove first ``` line and last ``` line
    # The content is everything between the first newline and the last ```
    first_newline = block.index("\n")
    code_text = block[first_newline + 1:-3]  # -3 to remove the closing ```
    
    # Code blocks should not parse inline markdown
    code_node = LeafNode("code", code_text)
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split("\n")
    # Remove the > from each line
    cleaned_lines = []
    for line in lines:
        # Remove > and optional space
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        elif line.startswith(">"):
            cleaned_lines.append(line[1:])
    
    text = "\n".join(cleaned_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        # Remove the "- " prefix
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        # Remove the "N. " prefix (where N is the number)
        # Find the first space after the number
        space_index = line.index(". ") + 2
        text = line[space_index:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    
    return ParentNode("ol", list_items)

def block_to_html_node(block):
    """Convert a single markdown block to an HTMLNode."""
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown):
    """Convert a full markdown document to an HTMLNode."""
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
    return ParentNode("div", children)