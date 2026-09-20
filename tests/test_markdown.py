"""Regression checks for authoring Markdown posts without a database."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from unified import inline, load_posts, markdown


class MarkdownTests(unittest.TestCase):
    def test_fenced_code_preserves_whitespace_and_escapes_html(self):
        source = 'Before.\n\n```python\nif a < b:\n    print("<script>")\n\n# **literal**\n```\n\nAfter.'
        rendered = markdown(source)
        self.assertIn('<pre><code class="language-python">if a &lt; b:\n    print(&quot;&lt;script&gt;&quot;)\n\n# **literal**\n</code></pre>', rendered)
        self.assertTrue(rendered.startswith('<p>Before.</p>'))
        self.assertTrue(rendered.endswith('<p>After.</p>'))
        self.assertNotIn('<script>', rendered)
        self.assertNotIn('<strong>', rendered)

    def test_longer_fence_can_quote_shorter_fence(self):
        self.assertEqual(markdown('````markdown\n```python\nexample\n```\n````'),
                         '<pre><code class="language-markdown">```python\nexample\n```\n</code></pre>')

    def test_unclosed_fence_remains_code_through_end_of_post(self):
        self.assertEqual(markdown('~~~\n<b>literal</b>'),
                         '<pre><code>&lt;b&gt;literal&lt;/b&gt;\n</code></pre>')

    def test_inline_code_does_not_become_links_or_emphasis(self):
        self.assertEqual(inline('Use `[Docs](https://example.com/) **raw** <b>`.'),
                         'Use <code>[Docs](https://example.com/) **raw** &lt;b&gt;</code>.')
        self.assertEqual(inline('Use ``a ` b``.'), 'Use <code>a ` b</code>.')

    def test_link_destination_is_not_processed_as_markdown(self):
        self.assertEqual(inline('[**Docs**](https://example.com/**v1**?a=1&b=2)'),
                         '<a href="https://example.com/**v1**?a=1&amp;b=2"><strong>Docs</strong></a>')

    def test_unsafe_links_and_raw_html_cannot_execute(self):
        self.assertEqual(inline('[Click](javascript:alert) <img src=x onerror=alert>'),
                         'Click &lt;img src=x onerror=alert&gt;')
        self.assertEqual(inline('[Click](//example.com/)'), 'Click')

    def test_numbered_steps_and_bullets_are_separate_lists(self):
        source = '3. Prepare **data**\n4. Train\n- Review\n- Publish\n\nDone.'
        self.assertEqual(markdown(source),
                         '<ol start="3"><li>Prepare <strong>data</strong></li><li>Train</li></ol>'
                         '<ul><li>Review</li><li>Publish</li></ul><p>Done.</p>')

    def test_existing_headings_and_images_still_render(self):
        self.assertEqual(markdown('## Studio\n\n![Studio screenshot](/assets/studio-01.png)'),
                         '<h2>Studio</h2><figure><img src="/assets/studio-01.png" alt="Studio screenshot" loading="lazy"></figure>')


class PostValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root/'content'/'blog').mkdir(parents=True)

    def write_post(self, filename, slug, status='published', sample='false'):
        path = self.root/'content'/'blog'/filename
        path.write_text(f'---\ntitle: Example\nslug: {slug}\nsummary: Summary\ncategory: Research\nstatus: {status}\nsample: {sample}\n---\n## Content\n\nA paragraph.', encoding='utf-8')
        return path

    def test_only_published_non_sample_posts_are_loaded(self):
        self.write_post('published.md', 'published')
        self.write_post('draft.md', 'draft', status='draft')
        self.write_post('sample.md', 'sample', sample='true')
        posts = load_posts(self.root, 'blog')
        self.assertEqual([post['slug'] for post in posts], ['published'])
        self.assertIn('<h2>Content</h2>', posts[0]['html'])

    def test_duplicate_slugs_fail_with_both_source_names(self):
        self.write_post('first.md', 'same-slug')
        self.write_post('second.md', 'same-slug')
        with self.assertRaisesRegex(ValueError, r'Duplicate slug.*same-slug.*first\.md.*second\.md'):
            load_posts(self.root, 'blog')

    def test_draft_slug_conflicts_are_caught_before_publication(self):
        self.write_post('first.md', 'same-slug')
        self.write_post('second.md', 'same-slug', status='draft')
        with self.assertRaisesRegex(ValueError, 'Duplicate slug'):
            load_posts(self.root, 'blog')

    def test_misspelled_status_fails_instead_of_silently_hiding_post(self):
        self.write_post('typo.md', 'a-post', status='publshed')
        with self.assertRaisesRegex(ValueError, r'typo\.md: invalid status.*publshed.*draft or published'):
            load_posts(self.root, 'blog')


if __name__ == '__main__':
    unittest.main()
