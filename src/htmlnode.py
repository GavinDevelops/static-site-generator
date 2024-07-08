from textnode import TextNode
import re


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not isinstance(self.props, dict):
            return ""
        s = ""
        for key in self.props:
            s = s + f' {key}="{self.props[key]}"'
        return s

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(value=value, tag=tag, children=children, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Value is None")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, props=props, children=children)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag is None")
        if self.children == None:
            raise ValueError("Children is somehow none")

        node = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            node = node + child.to_html()
        return node + f"</{self.tag}>"
