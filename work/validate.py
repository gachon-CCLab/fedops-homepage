from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from urllib.request import urlopen, Request
import argparse
import json
import re

args = argparse.ArgumentParser()
args.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1] / 'dist')
args.add_argument('--base-path', default='')
args.add_argument('--url', help='Optional live site base URL, including a project Pages path')
args.add_argument('--public', action='store_true')
options = args.parse_args()
root = options.root.resolve()
base_path = options.base_path.rstrip('/')
errors = []

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.images = [], [], []
        self.title = self.main = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'title': self.title = True
        if tag == 'main': self.main = True
        for key in ('src', 'href', 'data-image'):
            if a.get(key): self.links.append(a[key])
        if tag == 'img': self.images.append(a)
        if tag == 'a' and a.get('target') == '_blank' and 'noopener' not in a.get('rel', ''):
            errors.append('Unsafe blank target')

parsed = {}
for page in root.rglob('*.html'):
    content = page.read_text(encoding='utf-8')
    parser = Parser()
    parser.feed(content)
    parsed[page] = parser
    if not parser.title or not parser.main: errors.append(f'Missing title/main: {page}')
    if len(parser.ids) != len(set(parser.ids)): errors.append(f'Duplicate id: {page}')
    if '\ufffd' in content: errors.append(f'Encoding problem: {page}')
    if options.public and re.search(r'https?://(?:127\.0\.0\.1|localhost|\[::1\])', content):
        errors.append(f'Localhost leaked into public page: {page}')
    for image in parser.images:
        if not image.get('alt'): errors.append(f'Missing image alt: {page}')

assert parsed, 'No generated pages found'

def local_target(source, link):
    parts = urlsplit(link)
    if parts.scheme or parts.netloc: return None, parts
    path = unquote(parts.path)
    if path.startswith('/'):
        if base_path:
            if not (path == base_path or path.startswith(base_path + '/')):
                errors.append(f'Missing project base path: {source.name} -> {link}')
                return None, parts
            path = path[len(base_path):]
        target = root / path.lstrip('/')
    else:
        target = source.parent / path if path else source
    target = target.resolve()
    if not target.is_relative_to(root):
        errors.append(f'Path outside site: {link}')
        return None, parts
    if target.is_dir(): target = target / 'index.html'
    return target, parts

for page, parser in parsed.items():
    for link in parser.links:
        if link == '#': errors.append(f'Placeholder link: {page}')
        target, parts = local_target(page, link)
        if target is None: continue
        if not target.is_file(): errors.append(f'Broken local link: {page.name} -> {link}')
        elif parts.fragment and target in parsed and unquote(parts.fragment) not in parsed[target].ids:
            errors.append(f'Broken anchor: {link}')

for stylesheet in (root / 'assets').glob('*.css'):
    for link in re.findall(r'url\([\"\']?([^\"\')]+)[\"\']?\)', stylesheet.read_text(encoding='utf-8')):
        target, _ = local_target(stylesheet, link)
        if target is not None and not target.is_file(): errors.append(f'Broken CSS asset: {link}')

live = 0
if options.url:
    for page in parsed:
        if page.name == '404.html': continue
        rel = page.relative_to(root).as_posix().removesuffix('index.html')
        try:
            with urlopen(Request(options.url.rstrip('/') + '/' + rel, method='HEAD'), timeout=10) as response:
                if response.status != 200: errors.append(f'HTTP {response.status}: {rel}')
                live += 1
        except Exception as error: errors.append(str(error))

assert len(list((root/'assets').glob('studio-*.png'))) == 6
assert not errors, '\n'.join(errors)
print(json.dumps({'html_pages':len(parsed), 'live_routes_checked':live, 'original_screenshots':6, 'links_assets_anchors':'passed', 'public_build':options.public}, indent=2))
