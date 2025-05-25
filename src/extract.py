import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_title(markdown):
    m_split = markdown.splitlines()
    for line in m_split:
        matches = re.search(r"^#{1} (.*$)", line)
        if matches != None:
            return matches.group(1).strip()
    raise Exception("No header found")