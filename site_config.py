"""Shared local/public build settings. Console and Docs stay separate services."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import os
import re

ROOT = Path(__file__).resolve().parent
PUBLIC = os.environ.get('FEDOPS_ENV', 'local') == 'production'
BASE_PATH = os.environ.get('FEDOPS_BASE_PATH', '').rstrip('/')
if BASE_PATH and not re.fullmatch(r'/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*', BASE_PATH):
    raise ValueError('FEDOPS_BASE_PATH must be an absolute path without a trailing slash or traversal.')
DIST = Path(os.environ.get('FEDOPS_OUTPUT_DIR', str(ROOT / 'dist'))).resolve()
DOCS = 'https://gachon-cclab.github.io/fedops-docs-1.3/'
CONSOLE = os.environ.get('FEDOPS_CONSOLE_URL', 'https://ccl.gachon.ac.kr/fedops' if PUBLIC else 'http://127.0.0.1:4314/fedops/task')
REGISTRY = os.environ.get('FEDOPS_REGISTRY_URL', 'https://ccl.gachon.ac.kr/fedops/registry' if PUBLIC else 'http://127.0.0.1:4314/fedops/registry')
for setting in (CONSOLE, REGISTRY):
    parsed = urlsplit(setting)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Service links must be HTTP(S) URLs without credentials.')
    if PUBLIC and (parsed.hostname in ('localhost', '127.0.0.1', '::1') or parsed.scheme != 'https'):
        raise ValueError('Public builds require HTTPS service URLs, not localhost.')


def with_base_path(html):
    """Prefix local HTML paths once, including screenshot data attributes."""
    if not BASE_PATH:
        return html
    def replace(match):
        prefix, path = match.groups()
        if path == BASE_PATH or path.startswith(BASE_PATH + '/'):
            return match.group(0)
        return prefix + escape(BASE_PATH, quote=True) + path
    return re.sub(r'((?<![\w-])(?:href|src|data-image)=[\"\'])(/(?!/)[^\"\']*)', replace, html)
