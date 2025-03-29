import os

# Define the extensions you want to include
include_extensions = {'.py', '.ipynb', '.md', '.yaml', '.yml', '.txt'}

def combine_files_with_headers(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in sorted(filenames):
                ext = os.path.splitext(filename)[1]
                if ext in include_extensions and filename != os.path.basename(output_file):
                    filepath = os.path.join(dirpath, filename)
                    relpath = os.path.relpath(filepath, root_dir)
                    outfile.write(f"# === {relpath} ({ext}) ===\n")
                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except UnicodeDecodeError:
                        outfile.write("# [Could not decode file due to encoding issues]\n")
                    outfile.write('\n\n')

# Set your folder and output destination
combine_files_with_headers(
    r"E:\Coding\S_P_500_Stock_Trading\symbolikai",
    r"E:\Coding\S_P_500_Stock_Trading\combined_output.txt"
)
