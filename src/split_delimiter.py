from textnode import TextType, TextNode
from extract import extract_markdown_images, extract_markdown_links
from htmlnode import LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            text = node.text
            result_nodes = []

            while text:
                start_index = text.find(delimiter)
                if start_index == -1:
                    if text:
                        result_nodes.append(TextNode(text, TextType.TEXT))
                    break
                if start_index > 0:
                    result_nodes.append(TextNode(text[:start_index], TextType.TEXT))
                end_index = text.find(delimiter, start_index + len(delimiter))

                if end_index == -1:
                    raise Exception(f"No closing delimiter '{delimiter}' found")
                between_text = text[start_index + len(delimiter):end_index]
                result_nodes.append(TextNode(between_text, text_type))
                text = text[end_index +len(delimiter):]
            result.extend(result_nodes)
    return result

def split_nodes_image(old_nodes):
    new_text_nodes = []
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)
        if node.text_type != TextType.TEXT:
            new_text_nodes.append(node)
            continue
        while images:
            alt, url = images[0]
            image_markdown = f"![{alt}]({url})"
            before, after = text.split(image_markdown, 1)
            if before:
                new_text_nodes.append(TextNode(before, TextType.TEXT))
            new_text_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
            images = extract_markdown_images(text)
        if text:
            new_text_nodes.append(TextNode(text, TextType.TEXT))
    return new_text_nodes

def split_nodes_link(old_nodes):
    new_text_nodes = []
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)
        if node.text_type != TextType.TEXT:
            new_text_nodes.append(node)
            continue
        while links:
            text_part, url = links[0]
            link_markdown = f"[{text_part}]({url})"
            before, after = text.split(link_markdown, 1)
            if before:
                new_text_nodes.append(TextNode(before, TextType.TEXT))
            new_text_nodes.append(TextNode(text_part, TextType.LINK, url))
            text = after
            links = extract_markdown_links(text)
        if text:
            new_text_nodes.append(TextNode(text, TextType.TEXT))
    return new_text_nodes

def markdown_to_blocks(markdown):
    markdown_blocks = []
    block_split = markdown.split("\n\n")
    for blocks in block_split:
        block_strip = blocks.strip()
        if block_strip != "":
            markdown_blocks.append(block_strip)
    return markdown_blocks

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        leaf_node = LeafNode(None, text_node.text)
        #print(repr(leaf_node.tag))
        return leaf_node
    elif text_node.text_type == TextType.BOLD:
        leaf_node = LeafNode("b", text_node.text)
        #print(repr(leaf_node.tag))
        return leaf_node
    elif text_node.text_type == TextType.ITALIC:
        leaf_node = LeafNode("i", text_node.text)
        #print(repr(leaf_node.tag))
        return leaf_node
    elif text_node.text_type == TextType.CODE:
        leaf_node = LeafNode("code", text_node.text)
        #print(repr(leaf_node.tag))
        return leaf_node
    elif text_node.text_type == TextType.LINK:
        text_list = []
        text = LeafNode(None, text_node.text)
        text_list.append(text)
        parent_node = ParentNode("a", text_list, {"href": text_node.url})
        #print(repr(parent_node.tag))
        return parent_node
    elif text_node.text_type == TextType.IMAGE:
        leaf_node = LeafNode("img", value=None, props={"src":  text_node.url, "alt": text_node.text})
        #print(repr(leaf_node.tag))
        return leaf_node
    else:
        raise Exception(f"Invalid TextType: {text_node.text_type}")
    
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
    