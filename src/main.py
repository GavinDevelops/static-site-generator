import os
import shutil
from copy_static import copy_static_to_public, generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_static_to_public(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
