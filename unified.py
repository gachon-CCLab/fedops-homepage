"""Shared local presentation shell and Git-authored knowledge pages.

This is a design preview, not a replacement for the deployed documentation.
No third-party packages or database are needed to build these pages.
"""
from html import escape
from pathlib import Path
import re
from site_config import CONSOLE, REGISTRY, DOCS, DIST

GITHUB = 'https://github.com/gachon-CCLab/FedOps'


def brand():
    return '<a class="brand" href="/version-2/" aria-label="FedOps home"><span class="brandmark" aria-hidden="true"></span>FedOps</a>'


def site_document(title, description, body, section):
    items = [('home', '/version-2/', 'Home'),
             ('document', DOCS, 'Docs'), ('blog', '/blog/', 'Blog'), ('news', '/news/', 'News')]
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if section == key else '')+f'>{label}</a>' for key, url, label in items)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | FedOps</title><meta name="description" content="{escape(description, quote=True)}"><meta name="theme-color" content="#314B82">
<link rel="icon" href="/assets/fedops_icon.png" type="image/png"><link rel="apple-touch-icon" href="/assets/fedops_icon.png"><link rel="stylesheet" href="/assets/site.css?v=20260920b"><link rel="stylesheet" href="/assets/unified.css?v=20260920b">
<script src="/assets/site.js?v=20260920" defer></script><script src="/assets/unified.js?v=20260920" defer></script></head>
<body class="unified-site {section}-page"><a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap nav-inner">{brand()}<span class="badge">1.3</span><nav id="primary-navigation" class="nav-links" aria-label="Primary navigation">{nav}</nav>
<button class="menu-toggle" aria-controls="primary-navigation" aria-expanded="false">Menu</button><div class="nav-actions"><a href="{CONSOLE}" target="_blank" rel="noopener noreferrer" class="button console unified-primary">Open Console <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a></div></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div class="footer-top"><div>{brand()}<p>Gachon University · Cognitive Computing Lab<br>Local intelligence. Shared progress.</p></div><div class="footer-groups"><nav aria-label="Platform links"><b>Platform</b><a href="/version-2/">Home</a><a href="{CONSOLE}" target="_blank" rel="noopener noreferrer">Open Console ↗</a></nav><nav aria-label="Knowledge links"><b>Learn &amp; follow</b><a href="{DOCS}">Docs</a><a href="/blog/">Blog</a><a href="/news/">News</a></nav><nav aria-label="Community links"><b>Community</b><a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="https://flower.ai/profile/gfedops/apps" target="_blank" rel="noopener noreferrer">Flower Hub ↗</a><a href="https://sites.google.com/view/keylee" target="_blank" rel="noopener noreferrer">Gachon CCL ↗</a></nav></div></div>
<div class="footer-bottom"><span>© 2026 Cognitive Computing Lab, Gachon University</span><span>FedOps 1.3 · Design preview</span></div></div></footer></body></html>'''


def inline(text):
    """Render a deliberately small, escaped Markdown subset for authored posts."""
    tokens = re.compile(
        r'(?P<fence>`+)(?P<code>.+?)(?P=fence)'
        r'|\[(?P<label>[^\]]+)\]\((?P<href>[^\s)]+)\)'
        r'|\*\*(?P<strong>.+?)\*\*'
    )
    rendered, position = [], 0
    for match in tokens.finditer(text):
        rendered.append(escape(text[position:match.start()]))
        if match.group('code') is not None:
            # Code is escaped once and never interpreted as links or emphasis.
            rendered.append('<code>'+escape(match.group('code'))+'</code>')
        elif match.group('href') is not None:
            href = match.group('href')
            label = inline(match.group('label'))
            local_path = href.startswith('/') and not href.startswith('//')
            if local_path or href.startswith(('https://', 'http://127.0.0.1:')):
                rendered.append(f'<a href="{escape(href, quote=True)}">{label}</a>')
            else:
                rendered.append(label)
        else:
            rendered.append('<strong>'+inline(match.group('strong'))+'</strong>')
        position = match.end()
    rendered.append(escape(text[position:]))
    return ''.join(rendered)


def markdown(text):
    blocks, paragraph, items = [], [], []
    list_type, list_start = None, 1
    fence, language, code_lines = None, '', []
    def flush():
        nonlocal list_type, list_start
        if paragraph:
            blocks.append('<p>'+inline(' '.join(paragraph))+'</p>')
            paragraph.clear()
        if items:
            start = f' start="{list_start}"' if list_type == 'ol' and list_start != 1 else ''
            blocks.append(f'<{list_type}{start}>'+''.join('<li>'+inline(item)+'</li>' for item in items)+f'</{list_type}>')
            items.clear()
        list_type, list_start = None, 1
    def emit_code():
        class_name = f' class="language-{language}"' if language else ''
        code = '\n'.join(code_lines)+('\n' if code_lines else '')
        blocks.append(f'<pre><code{class_name}>'+escape(code)+'</code></pre>')
        code_lines.clear()
    for line in text.splitlines():
        if fence is not None:
            closing = r' {0,3}'+re.escape(fence[0])+'{'+str(len(fence))+r',}\s*'
            if re.fullmatch(closing, line):
                emit_code()
                fence = None
            else:
                code_lines.append(line)
            continue
        opening = re.fullmatch(r' {0,3}(`{3,}|~{3,})[ \t]*(.*)', line)
        ordered = re.fullmatch(r'(\d+)[.)]\s+(.+)', line)
        if opening:
            flush()
            fence = opening[1]
            info = opening[2].strip().split()
            language = info[0] if info and re.fullmatch(r'[A-Za-z0-9_+.-]+',info[0]) else ''
        elif not line.strip():
            flush()
        elif re.fullmatch(r'!\[([^\]]*)\]\((/assets/[^\s)]+)\)', line):
            flush()
            image = re.fullmatch(r'!\[([^\]]*)\]\((/assets/[^\s)]+)\)', line)
            blocks.append('<figure><img src="'+escape(image[2], quote=True)+'" alt="'+escape(image[1], quote=True)+'" loading="lazy"></figure>')
        elif line.startswith(('## ', '### ')):
            flush()
            level = len(line.split(' ')[0])
            blocks.append(f'<h{level}>'+inline(line[level+1:])+f'</h{level}>')
        elif line.startswith('- ') or ordered:
            current_type = 'ol' if ordered else 'ul'
            if paragraph or (items and list_type != current_type):
                flush()
            if not items:
                list_type = current_type
                list_start = int(ordered[1]) if ordered else 1
            items.append(ordered[2] if ordered else line[2:])
        else:
            if items: flush()
            paragraph.append(line.strip())
    if fence is not None:
        emit_code()
    flush()
    return ''.join(blocks)


def load_posts(root, section):
    posts, slugs = [], {}
    for source in sorted((root/'content'/section).glob('*.md')):
        raw = source.read_text(encoding='utf-8-sig')
        parts = raw.split('---',2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f'Missing front matter: {source}')
        meta = {}
        for line in parts[1].strip().splitlines():
            key, value = line.split(':',1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
        for field in ('title','slug','summary','category','status'):
            if not meta.get(field): raise ValueError(f'{source}: missing {field}')
        if not re.fullmatch('[a-z0-9-]+',meta['slug']):
            raise ValueError(f'Invalid slug: {source}')
        if meta['status'] not in ('draft', 'published'):
            raise ValueError(f'{source}: invalid status {meta["status"]!r}; use draft or published')
        if meta['slug'] in slugs:
            raise ValueError(f'Duplicate slug {meta["slug"]!r}: {slugs[meta["slug"]]} and {source}')
        slugs[meta['slug']] = source
        if meta['status'] != 'published' or meta.get('sample', '').lower() == 'true':
            continue
        meta['html'] = markdown(parts[2])
        posts.append(meta)
    return posts


def post_row(post, section):
    return f'<a class="news-row" href="/{section}/{post["slug"]}/"><span class="category">{escape(post["category"]).upper()}</span><div><h3>{escape(post["title"])}</h3><p>{escape(post["summary"])}</p></div><span class="text-link read">Read {"article" if section == "blog" else "update"} <span aria-hidden="true">→</span></span></a>'


def build_collection(root, page, section):
    posts = load_posts(root, section)
    title = 'Ideas behind the work.' if section == 'blog' else 'The next chapter.'
    summary = ('Technical perspectives, research, and practical examples from the FedOps community.'
               if section == 'blog' else 'Release information, documentation updates, and development progress from FedOps.')
    rows = ''.join(post_row(post, section) for post in posts)
    if not posts:
        rows = f'<div class="empty"><p class="eyebrow">{section.capitalize()}</p><h2>No {"articles" if section == "blog" else "updates"} published yet.</h2><p>In the meantime, explore the documentation and the research behind FedOps.</p><div class="actions" style="justify-content:center"><a class="button blue" href="{DOCS}">Read the documentation →</a><a class="button outline" href="{DOCS}v1.3/resources/">Explore research &amp; resources →</a></div></div>'
    body = f'<section class="page-head"><div class="wrap"><p class="eyebrow">{section.capitalize()}</p><h1>{title}</h1><p>{summary}</p></div></section><section class="section"><div class="wrap">{rows}</div></section>'
    page(Path(f'{section}/index.html'),section.capitalize(),summary,body,section)
    published_paths = {(DIST/section/'index.html').resolve()}
    for post in posts:
        body = f'<div class="wrap"><article class="prose article-standalone"><a class="back" href="/{section}/">← All {section}</a><br><span class="status-label">{escape(post["category"])}</span><h1>{escape(post["title"])}</h1><p>{escape(post["summary"])}</p>{post["html"]}<div class="article-bottom"><a href="/{section}/">← All {section}</a><a href="{DOCS}">FedOps 1.3 Docs →</a></div></article></div>'
        output = Path(f'{section}/{post["slug"]}/index.html')
        page(output,post['title'],post['summary'],body,section)
        published_paths.add((DIST/output).resolve())
    # These HTML files are generated outputs. Keep draft source Markdown intact.
    generated_root = (DIST/section).resolve()
    for old_page in generated_root.rglob('*.html'):
        resolved = old_page.resolve()
        assert resolved.is_relative_to(generated_root)
        if resolved not in published_paths:
            old_page.unlink()


def build_doc_redirects(root, links):
    for old_url, destination in links.items():
        if '#' in old_url:
            continue
        output = DIST/old_url.strip('/')/'index.html'
        output.parent.mkdir(parents=True,exist_ok=True)
        target = escape(destination,quote=True)
        output.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FedOps Docs</title><link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0;url={target}"></head><body><main><p>Opening <a href="{target}">FedOps 1.3 Docs</a>.</p></main></body></html>',encoding='utf-8')


def build_knowledge_pages(root,page):
    build_collection(root,page,'blog')
    build_collection(root,page,'news')
