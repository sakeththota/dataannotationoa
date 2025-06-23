import urllib.request
from html.parser import HTMLParser
from collections import defaultdict

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_td = False
        self.current_row = []
        self.table_data = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
            self.current_data = ''
    
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
            self.current_row.append(self.current_data.strip())
        elif tag == 'tr':
            if self.current_row:
                self.table_data.append(self.current_row)
                self.current_row = []

    def handle_data(self, data):
        if self.in_td:
            self.current_data += data

def print_unicode_grid_from_doc(doc_url):
    try:
        with urllib.request.urlopen(doc_url) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch document: {e}")
        return

    parser = TableParser()
    parser.feed(html)

    points = []
    for row in parser.table_data:
        if len(row) != 3:
            continue
        try:
            x = int(row[0])
            char = row[1]
            y = int(row[2])
            points.append((x, y, char))
        except ValueError:
            continue

    if not points:
        print("No valid table data found.")
        return

    # Build and print grid
    grid = defaultdict(dict)
    max_x = max_y = 0
    for x, y, char in points:
        grid[y][x] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    for y in range(max_y + 1):
        row = ''.join(grid[y].get(x, ' ') for x in range(max_x + 1))
        print(row)

print_unicode_grid_from_doc("https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub")