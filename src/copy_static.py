import os
from os.path import isfile
import shutil
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No h1 header found")


def copy_static_to_public(input_path, output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for filename in os.listdir(input_path):
        from_path = os.path.join(input_path, filename)
        dest_path = os.path.join(output_path, filename)
        print(f"copy {from_path} to {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, output_path)
        else:
            copy_static_to_public(from_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating static html page from {from_path} to {dest_path} using {template_path}"
    )
    html_content = None
    header_content = None
    template = None
    with open(from_path) as f:
        markdown = f.read()
        header_content = extract_title(markdown)
        html_content = markdown_to_html_node(markdown).to_html()
        f.close()
    with open(template_path) as f:
        template = f.read()
        f.close()
    template = template.replace("{{ Title }}", header_content)
    template = template.replace("{{ Content }}", html_content)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(template)
        f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        new_content_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(new_content_path):
            new_filename = "".join([filename.split(".")[0], ".html"])
            new_dest_path = os.path.join(dest_dir_path, new_filename)
            generate_page(new_content_path, template_path, new_dest_path)
        else:
            new_dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(new_content_path, template_path, new_dest_path)
