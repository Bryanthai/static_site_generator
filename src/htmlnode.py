class HTMLNode:
    def __init__(self, tag = None , value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_props = ""
        if self.props == None:
            return html_props
        for prop in self.props:
            html_props += f" {prop}=\"{self.props[prop]}\""
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        elif self.tag == "a":
            if self.props["href"] == None:
                raise ValueError("This link doesnt have a href")
            return f"<{self.tag} href=\"{self.props["href"]}\">{self.value}</{self.tag}>"
        elif self.tag == "img":
            if self.props["src"] == None:
                raise ValueError("This link doesnt have a src")
            if self.props["alt"] == None:
                raise ValueError("This link doesnt have a alt text")
            return f"<{self.tag} src=\"{self.props["src"]}\" alt=\"{self.props["alt"]}\">{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("There is no tag in this parent node")
        if self.children == None:
            raise ValueError("There is no value in this parent node")
        str = ""
        for child in self.children:
            str += child.to_html()
        return f"<{self.tag}>{str}</{self.tag}>"