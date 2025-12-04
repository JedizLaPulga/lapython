# main.py - A tiny functional web browser using ONLY the Python standard library
import tkinter as tk
from tkinter import ttk
from urllib.parse import urlparse
from html.parser import HTMLParser
import http.client
import ssl

# ------------------------------------------------------------------
# Simple HTML Parser → builds a very basic tree of text and tags
# ------------------------------------------------------------------
class SimpleDOMNode:
    def __init__(self, tag=None, text=None, parent=None):
        self.tag = tag
        self.text = text.strip() if text else None
        self.children = []
        self.parent = parent
        self.style = {}  # future: very basic inline style support

class TinyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = SimpleDOMNode(tag="root")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = SimpleDOMNode(tag=tag, parent=self.stack[-1])
        self.stack[-1].children.append(node)
        self.stack.append(node)

    def handle_endtag(self, tag):
        if self.stack[-1].tag == tag:
            self.stack.pop()

    def handle_data(self, data):
        if data.strip():
            text_node = SimpleDOMNode(text=data, parent=self.stack[-1])
            self.stack[-1].children.append(text_node)

# ------------------------------------------------------------------
# Very simple layout: just calculates (x, y, width, height) for each node
# ------------------------------------------------------------------
BLOCK_TAGS = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol', 'body', 'html'}
INLINE_TAGS = {'a', 'span', 'strong', 'em', 'b', 'i'}

class LayoutEngine:
    def __init__(self, dom_root, width=800):
        self.width = width
        self.y = 10
        self.x = 10
        self.layout_nodes(dom_root)

    def layout_nodes(self, node):
        if node.tag in BLOCK_TAGS:
            node.x = 10
            node.y = self.y
            node.width = self.width - 20
            self.y += 30  # line height
        elif node.text:
            node.x = self.x
            node.y = self.y - 15
            self.x += len(node.text) * 8  # rough monospace width

        for child in node.children:
            self.layout_nodes(child)

# ------------------------------------------------------------------
# Renderer using Tkinter Canvas
# ------------------------------------------------------------------
class BrowserCanvas(tk.Canvas):
    def __init__(self, parent, dom_root):
        super().__init__(parent, bg="white")
        self.render(dom_root)

    def render(self, root):
        layout = LayoutEngine(root)
        self.draw_node(root)

    def draw_node(self, node):
        if node.text:
            self.create_text(node.x, node.y, text=node.text, anchor="nw", font=("Segoe UI", 12))
        for child in node.children:
            self.draw_node(child)

# ------------------------------------------------------------------
# HTTP requester (supports http and https via stdlib)
# ------------------------------------------------------------------
def fetch_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return "<h1>Unsupported scheme</h1>"

    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    if parsed.scheme == "http":
        conn = http.client.HTTPConnection(host, port)
    else:
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(host, port, context=context)

    conn.request("GET", path)
    response = conn.getresponse()
    if response.status != 200:
        conn.close()
        return f"<h1>Error {response.status} {response.reason}</h1>"

    data = response.read()
    conn.close()

    # Assume UTF-8 or fallback
    try:
        return data.decode('utf-8')
    except:
        return data.decode('latin-1')

# ------------------------------------------------------------------
# Main Browser GUI
# ------------------------------------------------------------------
class StdLibBrowser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python StdLib Browser")
        self.geometry("1000x700")

        # Navigation bar
        nav = ttk.Frame(self)
        nav.pack(fill=tk.X, padx=5, pady=5)

        self.address_var = tk.StringVar(value="https://example.com")
        addr = ttk.Entry(nav, textvariable=self.address_var)
        addr.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        addr.bind("<Return>", lambda e: self.load_url())

        go = ttk.Button(nav, text="Go", command=self.load_url)
        go.pack(side=tk.RIGHT)

        # Canvas for rendering
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def load_url(self):
        url = self.address_var.get()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self.canvas.delete("all")
        self.canvas.create_text(400, 300, text="Loading...", font=("Arial", 16))
        self.update()

        html = fetch_url(url)
        parser = TinyHTMLParser()
        parser.feed(html)
        self.canvas.delete("all")
        BrowserCanvas(self.canvas, parser.root)

if __name__ == "__main__":
    StdLibBrowser().mainloop()