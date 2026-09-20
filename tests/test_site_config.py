import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SiteConfigTests(unittest.TestCase):
    def run_config(self, code, **settings):
        env = {key:value for key,value in os.environ.items() if not key.startswith('FEDOPS_')}
        env.update(settings)
        return subprocess.run([sys.executable, '-c', code], cwd=ROOT, env=env, capture_output=True, text=True)

    def test_project_pages_paths_and_external_docs(self):
        code = '''from site_config import with_base_path
html = '<a href="/news/post/">Post</a><img src="/assets/a.png"><button data-image="/assets/b.png"></button><a href="https://gachon-cclab.github.io/fedops-docs-1.3/">Docs</a><a href="#section">Jump</a><a href="//example.org">External</a>'
out = with_base_path(html)
assert 'href="/fedops-homepage/news/post/"' in out
assert 'src="/fedops-homepage/assets/a.png"' in out
assert 'data-image="/fedops-homepage/assets/b.png"' in out
assert 'href="https://gachon-cclab.github.io/fedops-docs-1.3/"' in out
assert 'href="#section"' in out and 'href="//example.org"' in out
assert with_base_path(out) == out
'''
        result = self.run_config(code, FEDOPS_BASE_PATH='/fedops-homepage')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_public_default_console_is_remote(self):
        result = self.run_config('from site_config import CONSOLE; assert CONSOLE == "https://ccl.gachon.ac.kr/fedops"', FEDOPS_ENV='production')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_public_build_rejects_local_console(self):
        result = self.run_config('import site_config', FEDOPS_ENV='production', FEDOPS_CONSOLE_URL='http://127.0.0.1:4314/fedops/task')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Public builds require', result.stderr)

    def test_base_path_rejects_traversal(self):
        result = self.run_config('import site_config', FEDOPS_BASE_PATH='/../../x')
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
