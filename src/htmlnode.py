class HTMLNode:
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        attributes_html = ""
        if self.props is not None:
            for attr, value in self.props.items():
                attributes_html += f' {attr}="{value}"'
        
        if self.children is None or len(self.children) == 0:
            if self.value is None:
                return f"<{self.tag}{attributes_html}></{self.tag}>"
            else:
                return f"<{self.tag}{attributes_html}>{self.value}</{self.tag}>"
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{attributes_html}>{children_html}</{self.tag}>"
    
    def props_to_html(self):
        html_string = ""
        if self.props == None:
            return ""
        for key, value in sorted(self.props.items()):
            html_string = html_string + f' {key}="{value}"'
        return html_string
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        #print(f"LeafNode init - props before: {props}")
        props = props if props is not None else {}
        #print(f"LeafNode init - props after: {props}")
        super().__init__(tag=tag, value=value, props=props, children=[])
        #print(f"LeafNode init - self.props after super: {self.props}")
        self.value = value
    
    def to_html(self):
        #print(f"Debug - tag: {self.tag}, value: {self.value}, props: {self.props}")
        if self.tag is None:
            return self.value or ""
        if not self.value and self.tag is None:
            raise ValueError("LeafNode must have a value")
        
        html = f"<{self.tag}"
        
        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
        
        html += f">{self.value}</{self.tag}>"
        
        return html
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have a child")
        
        html = f"<{self.tag}"

        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
        html += ">"

        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"

        return html