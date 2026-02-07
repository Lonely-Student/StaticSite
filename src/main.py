# main.py
import os
import shutil
import sys
from pathlib import Path
from block_markdown import markdown_to_html_node

def copy_static_to_public(public_dir="public"):
    """Copy all contents from static directory to public directory."""
    static_dir = "static"
    
    # Delete the public directory if it exists
    if os.path.exists(public_dir):
        print(f"Deleting {public_dir} directory...")
        shutil.rmtree(public_dir)
    
    # Create a fresh public directory
    print(f"Creating {public_dir} directory...")
    os.mkdir(public_dir)
    
    # Copy all contents from static to public
    copy_directory_contents(static_dir, public_dir)

def copy_directory_contents(src, dst):
    """Recursively copy all files and directories from src to dst."""
    if not os.path.exists(src):
        raise ValueError(f"Source directory {src} does not exist")
    
    # List all items in the source directory
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Copy the file
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # It's a directory, create it and recurse
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            copy_directory_contents(src_path, dst_path)

def extract_title(markdown):
    """Extract the h1 title from a markdown document."""
    lines = markdown.split("\n")
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            # Remove the # and any leading/trailing whitespace
            return stripped[2:].strip()
    
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """Generate an HTML page from markdown using a template."""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)
    
    # Replace paths with basepath
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(full_html)
    
    print(f"Page generated successfully at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """Recursively generate HTML pages from markdown files in a directory."""
    # List all items in the content directory
    items = os.listdir(dir_path_content)
    
    for item in items:
        content_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(content_path):
            # Check if it's a markdown file
            if content_path.endswith('.md'):
                # Convert .md to .html for destination
                relative_path = os.path.relpath(content_path, dir_path_content)
                html_filename = Path(relative_path).stem + '.html'
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                # Generate the page
                generate_page(content_path, template_path, dest_path, basepath)
        else:
            # It's a directory, create corresponding directory in dest and recurse
            new_content_dir = content_path
            relative_dir = os.path.relpath(content_path, dir_path_content)
            new_dest_dir = os.path.join(dest_dir_path, relative_dir)
            
            # Create the destination directory if it doesn't exist
            if not os.path.exists(new_dest_dir):
                os.makedirs(new_dest_dir)
            
            # Recurse into the subdirectory
            generate_pages_recursive(new_content_dir, template_path, new_dest_dir, basepath)

def main():
    # Change to the project root directory (parent of src)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Starting static site generator with basepath: {basepath}")
    
    # Use docs directory for GitHub Pages
    output_dir = "docs"
    
    # Copy static files
    copy_static_to_public(output_dir)
    
    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", output_dir, basepath)
    
    print("Site generation complete!")

if __name__ == "__main__":
    main()