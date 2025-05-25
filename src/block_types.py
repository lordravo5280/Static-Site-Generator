from enum import Enum

import re

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(markdown):
    if markdown == "":
        return BlockType.paragraph
    if re.match(r"^`{3}(.*?)`{3}$", markdown, re.DOTALL):
        return BlockType.code
    if re.match(r"^#{1,6} (.*?)", markdown):
        return BlockType.heading
    if all(line.startswith(">") for line in markdown.splitlines()):
        return BlockType.quote
    if all(line.startswith("- ") for line in markdown.splitlines()):
        return BlockType.unordered_list
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(markdown.splitlines())):
        return BlockType.ordered_list
    return BlockType.paragraph