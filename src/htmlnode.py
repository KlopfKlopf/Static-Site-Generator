class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        html_string = ""
        if self.props is None:
            return ""
        for attribute, value in self.props.items():
            html_string += f" {attribute}={value}"
        return html_string
        
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: No value passed.")
        if self.tag is None:
            return self.value
        html_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_string
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: No Tag provided.")
        if self.children is None:
            raise ValueError("Invalid HTML: ParentNode has no Children.")
        child_html_string = ""
        for child_node in self.children:
            child_html_string += child_node.to_html()
        html_string = f"<{self.tag}>{child_html_string}</{self.tag}>"
        return html_string
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    