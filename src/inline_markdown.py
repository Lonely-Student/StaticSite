# inline_markdown.py
from textnode import TextNode, TextType
import re

def extract_markdown_images(text):
    """Extract markdown images and return list of (alt_text, url) tuples."""
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    """Extract markdown links and return list of (anchor_text, url) tuples."""
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # If it's not a TEXT type node, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        parts = old_node.text.split(delimiter)
        
        # If we have an even number of parts, the delimiters aren't matched
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: no matching closing delimiter '{delimiter}' found")
        
        # Process the parts
        for i, part in enumerate(parts):
            if part == "":
                continue
            
            # Even indices (0, 2, 4...) are normal text
            # Odd indices (1, 3, 5...) are delimited text
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def split_nodes_image(old_nodes):
    """Split TextNodes based on markdown image syntax."""
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images, add the node as-is
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process the text, splitting on each image
        remaining_text = old_node.text
        for alt_text, url in images:
            # Split on the image markdown (only split once)
            sections = remaining_text.split(f"![{alt_text}]({url})", 1)
            
            # Add the text before the image
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update remaining text to be after the image
            remaining_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    """Split TextNodes based on markdown link syntax."""
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links, add the node as-is
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process the text, splitting on each link
        remaining_text = old_node.text
        for anchor_text, url in links:
            # Split on the link markdown (only split once)
            sections = remaining_text.split(f"[{anchor_text}]({url})", 1)
            
            # Add the text before the link
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Update remaining text to be after the link
            remaining_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    """Convert raw markdown text into a list of TextNodes."""
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply each splitting function in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes