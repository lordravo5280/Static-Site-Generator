import unittest

from block_types import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        markdown = "# This is a heading"
        self.assertEqual(block_to_block_type(markdown), BlockType.heading)

    def test_block_to_block_type_unordered(self):
        markdown = "- This is an unordered list\n- this too"
        self.assertEqual(block_to_block_type(markdown), BlockType.unordered_list)

    def test_block_to_block_type_ordered(self):
        markdown = "1. This is an ordered list\n2. This too\n3. Also this"
        self.assertEqual(block_to_block_type(markdown), BlockType.ordered_list)  

    def test_block_to_block_type_code(self):
        markdown = "```This is a code\nMore Code\nLast line of code```"
        self.assertEqual(block_to_block_type(markdown), BlockType.code)

    def test_block_to_block_type_quote(self):
        markdown = ">...and you can quote me on that\n>No further comments"
        self.assertEqual(block_to_block_type(markdown), BlockType.quote)

    def test_block_to_block_type_paragraph(self):
        markdown = "I'm a paragraph!"
        self.assertEqual(block_to_block_type(markdown), BlockType.paragraph)

    def test_block_to_block_type_empty(self):
        markdown = ""
        self.assertEqual(block_to_block_type(markdown), BlockType.paragraph)        

if __name__ == "__main__":
    unittest.main()