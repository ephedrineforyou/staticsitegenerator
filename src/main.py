import os
import shutil
import sys

from delimiter import extract_title, markdown_to_html_node

# from htmlnode import ParentNode


def clean_and_copy_directory(src, dst, first_call=True):
    # 1. Clean the destination directory
    if os.path.exists(dst) and first_call:
        # shutil.rmtree is the standard way to delete non-empty dirs,
        # but we use it only for cleaning, not copying.
        shutil.rmtree(dst)
    if not os.path.exists(dst):
        os.makedirs(dst)

    # 2. Iterate through source contents
    for item in os.listdir(src):
        s_path = os.path.join(src, item)
        d_path = os.path.join(dst, item)

        if os.path.isdir(s_path):
            # Recursively copy subdirectory
            clean_and_copy_directory(s_path, d_path, False)
        else:
            # Copy file
            shutil.copy2(s_path, d_path)
            print(f"Copied: {s_path} to {d_path}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    markdown_html = markdown_to_html_node(markdown_content).to_html()
    markdown_title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", markdown_title).replace(
        "{{ Content }}", markdown_html
    )

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    for item in os.listdir(dir_path_content):
        if item.endswith(".md"):
            with open(f"{dir_path_content}/{item}", "r", encoding="utf-8") as f:
                markdown_content = f.read()

            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            markdown_html = markdown_to_html_node(markdown_content).to_html()
            markdown_title = extract_title(markdown_content)

            template_content = template_content.replace(
                "{{ Title }}", markdown_title
            ).replace("{{ Content }}", markdown_html)

            template_content = template_content.replace(
                'href="/', f'href="{basepath}'
            ).replace('src="/', f'src="{basepath}')

            os.makedirs(dest_dir_path, exist_ok=True)

            with open(f"{dest_dir_path}/{item[:-3]}.html", "w") as f:
                f.write(template_content)
        elif not os.path.isfile(f"{dir_path_content}/{item}"):
            generate_pages_recursive(
                f"{dir_path_content}/{item}",
                template_path,
                f"{dest_dir_path}/{item}",
                basepath,
            )


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    source_dir = "static"
    destination_dir = "docs"
    markdown_content_path = "content"
    template_path = "template.html"

    # Ensure source exists before running
    if os.path.exists(source_dir):
        clean_and_copy_directory(source_dir, destination_dir)
    else:
        print(f"Source directory '{source_dir}' not found.")

    if os.path.exists(markdown_content_path):
        if os.path.exists(template_path):
            generate_pages_recursive(
                markdown_content_path, template_path, destination_dir, basepath
            )
        else:
            print(f"HTML Template at '{template_path}' not found.")
    else:
        print(f"Markdown file at '{markdown_content_path}' not found.")


if __name__ == "__main__":
    main()
