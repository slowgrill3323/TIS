import re
import sys
import os

# Patterns for the blocks to remove (no requirement for '>' on same line)
DIV_START_PATTERN = re.compile(
    r'<div[^>]*id=["\']ewd_tree_root["\']',
    re.IGNORECASE
)

MAIN_TABLE_START_PATTERN = re.compile(
    r'<table[^>]*id=["\']mainTable["\']',
    re.IGNORECASE
)

GRAY_TABLE_START_PATTERN = re.compile(
    r'<table[^>]*style=["\']\s*background-color:#676767;\s*width:100%;?\s*;?["\']',
    re.IGNORECASE
)


def remove_block(html_text, start_pattern, tag_name):
    """
    Remove a block starting with a tag that matches start_pattern
    and ending at the matching closing </tag_name>. Handles nesting
    and multi-line start tags.
    """
    lines = html_text.splitlines(keepends=True)

    output = []
    inside_target = False
    depth = 0

    # Regexes for counting nested tags
    open_tag_re = re.compile(r'<\s*' + re.escape(tag_name) + r'\b', re.IGNORECASE)
    close_tag_re = re.compile(r'</\s*' + re.escape(tag_name) + r'\s*>', re.IGNORECASE)

    for line in lines:
        if not inside_target:
            # Look for the starting tag (even if the tag isn't closed on this line)
            if start_pattern.search(line):
                inside_target = True
                depth = 1  # we found the first opening tag
                # Do not append this line (we're removing the whole block)
                continue
            else:
                output.append(line)
        else:
            # We are inside the block to remove; track nested tags
            opens = len(open_tag_re.findall(line))
            closes = len(close_tag_re.findall(line))

            depth += opens
            depth -= closes

            # When depth returns to 0, we've closed the original tag
            if depth <= 0:
                inside_target = False
            # Skip all lines while inside target block
            continue

    return "".join(output)


def process_html(html_text):
    # 1. Remove <div id="ewd_tree_root"> ... </div>
    html_text = remove_block(html_text, DIV_START_PATTERN, "div")
    # 2. Remove <table id="mainTable"> ... </table>
    html_text = remove_block(html_text, MAIN_TABLE_START_PATTERN, "table")
    # 3. Remove <table style="background-color:#676767; width:100%;"> ... </table>
    html_text = remove_block(html_text, GRAY_TABLE_START_PATTERN, "table")
    return html_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python strip_tis_chrome_ui.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    # Read original file
    with open(filename, "r", encoding="utf-8") as f:
        original_html = f.read()

    # Process
    modified_html = process_html(original_html)

    # Write back in place
    with open(filename, "w", encoding="utf-8") as f:
        f.write(modified_html)

    print(f"Removed ewd_tree_root div and target tables from '{filename}'.")


if __name__ == "__main__":
    main()
