from block_types import BlockType, block_to_block_type
from htmlnode import HTMLNode
from split_delimiter import markdown_to_blocks


def markdown_to_html_node(markdown):
    from textnode import TextNode, TextType
    from split_delimiter import text_node_to_html_node
    blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode("div", None, None, [])
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.paragraph:
            p_node = HTMLNode("p", None, None, [])
            content = block.replace("\n", " ")
            p_children = text_to_children(content)
            p_node.children = p_children
            parent_node.children.append(p_node)
        if block_type == BlockType.heading:
            counter = 0
            for char in block:
                if char == "#":
                    counter += 1
                else:
                    break
            heading_node = HTMLNode(f"h{counter}", None, None, [])
            content = block[counter:].strip()
            children = text_to_children(content)
            heading_node.children = children
            parent_node.children.append(heading_node)
        if block_type == BlockType.quote:
            quote_node = HTMLNode("blockquote", None, None, [])
            content = "\n".join([line.lstrip(">").lstrip() for line in block.split("\n")])
            children = text_to_children(content)
            quote_node.children = children
            parent_node.children.append(quote_node)
        if block_type == BlockType.code:
            pre_node = HTMLNode("pre", None, None, [])
            code_node = HTMLNode("code", None, None, [])
            content = block.split("```")[1].strip()
            text_node = TextNode(content, TextType.TEXT)
            code_content_node = text_node_to_html_node(text_node)
            code_node.children = [code_content_node]
            pre_node.children = [code_node]
            parent_node.children.append(pre_node)
        if block_type == BlockType.unordered_list:
            ul_node = HTMLNode("ul", None, None, [])
            list_items = block.split("\n")
            for item in list_items:
                if not item.strip():
                    continue
                item_content = item.lstrip("-*").lstrip()
                li_node = HTMLNode("li", None, None, [])
                item_children = text_to_children(item_content)
                li_node.children = item_children
                ul_node.children.append(li_node)
            parent_node.children.append(ul_node)
        if block_type == BlockType.ordered_list:
            ol_node = HTMLNode("ol", None, None, [])
            list_items = block.split("\n")
            for item in list_items:
                if not item.strip():
                    continue
                import re
                item_content = re.sub(r'^\d+\.\s*', '', item)
                li_node = HTMLNode("li", None, None, [])
                item_children = text_to_children(item_content)
                li_node.children = item_children
                ol_node.children.append(li_node)
            parent_node.children.append(ol_node)


    return parent_node

def text_to_children(text):
    from split_delimiter import text_node_to_html_node, text_to_textnodes
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes