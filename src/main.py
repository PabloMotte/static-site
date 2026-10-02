#!/usr/bin/env python3
import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive  #, generate_page

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main() -> None:
    basepath = "/"
    if sys.argv[1].startswith("/"):
        basepath = sys.argv[1]
    print(f"Setting basepath to '{basepath}'")
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    # generate_page(
    #     os.path.join(dir_path_content, "index.md"),
    #     template_path,
    #     os.path.join(dir_path_public, "index.html"),
    # )
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath,
    )


if __name__ == "__main__":
    main()
