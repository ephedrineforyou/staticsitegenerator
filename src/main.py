import os
import shutil


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


def main():
    source_dir = "static"
    destination_dir = "public"

    print(os.getcwd())
    # Ensure source exists before running
    if os.path.exists(source_dir):
        clean_and_copy_directory(source_dir, destination_dir)
    else:
        print(f"Source directory '{source_dir}' not found.")


if __name__ == "__main__":
    main()
