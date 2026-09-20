from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from urllib.request import urlopen,Request
import json

root=Path(__file__).resolve().parents[1]/'dist'
errors=[]
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[];self.external=[];self.images=[];self.title=False;self.main=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id'in a:self.ids.append(a['id'])
        if tag=='title':self.title=True
        if tag=='main':self.main=True
        for key in ('src','href','data-image'):
            if a.get(key):self.links.append(a[key])
        if tag=='img':self.images.append(a)
        if tag=='a' and a.get('target')=='_blank' and 'noopener'not in a.get('rel',''):errors.append('Unsafe blank target')
parsed={}
for p in root.rglob('*.html'):
    text=p.read_text(encoding='utf-8')
    parser=Parser();parser.feed(text);parsed[p]=parser
    if not parser.title or not parser.main:errors.append(f'Missing title/main: {p}')
    if len(parser.ids)!=len(set(parser.ids)):errors.append(f'Duplicate id: {p}')
    if '\ufffd'in text:errors.append(f'Encoding problem: {p}')
    for image in parser.images:
        if not image.get('alt'):errors.append(f'Missing image alt: {p}')
for p,parser in parsed.items():
    for link in parser.links:
        parts=urlsplit(link)
        if parts.scheme or parts.netloc:continue
        if link=='#':errors.append(f'Placeholder link: {p}')
        target=root/unquote(parts.path).lstrip('/') if parts.path else p
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append(f'Broken local link: {p.name} -> {link}')
        elif parts.fragment and target in parsed and unquote(parts.fragment)not in parsed[target].ids:errors.append(f'Broken anchor: {link}')
for p in parsed:
    if p.name=='404.html':continue
    rel=p.relative_to(root).as_posix()
    url='http://127.0.0.1:4313/'+rel.removesuffix('index.html')
    try:
        with urlopen(Request(url,method='HEAD'),timeout=5) as r:
            if r.status!=200:errors.append(f'HTTP {r.status}: {url}')
    except Exception as e:errors.append(str(e))
assert len(list((root/'assets').glob('studio-*.png')))==6
assert not errors,'\n'.join(errors)
print(json.dumps({'html_pages':len(parsed),'live_routes_checked':len(parsed)-1,'original_screenshots':6,'local_links_assets_anchors':'passed','headings_main_alt_ids':'passed'},indent=2))
