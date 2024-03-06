from textnode import TextNode

text = "This is a text node"
text_type = "bold"
url = "https://www.boot.dev"

node1 = TextNode(text, text_type, url)
node2 = TextNode(text, text_type, url)

print(node1 == node2)
print(node1)