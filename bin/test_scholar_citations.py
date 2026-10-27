from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from update_scholar_citations import main, parse_profile


def row(article='paper1', count='12', author='author1', include_count=True):
    citation = f'<td><a class="gsc_a_ac gs_ibl">{count}</a></td>' if include_count else ''
    return f'''<tr class="gsc_a_tr"><td><a class="gsc_a_at"
        href="/citations?view_op=view_citation&amp;citation_for_view={author}:{article}">
        Research &amp; <i>remote sensing</i></a></td>{citation}</tr>'''


class ScholarCitationChecks(unittest.TestCase):
    def test_count_title_and_id_are_parsed(self):
        self.assertEqual(parse_profile(row(count='2,036'), 'author1'), {
            'paper1': {'title': 'Research & remote sensing', 'citations': 2036}})

    def test_present_empty_citation_cell_means_zero(self):
        self.assertEqual(parse_profile(row(count=''), 'author1')['paper1']['citations'], 0)

    def test_missing_citation_cell_is_not_zero(self):
        with self.assertRaises(ValueError):
            parse_profile(row(include_count=False), 'author1')

    def test_other_authors_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            parse_profile(row(author='someone_else'), 'author1')

    def test_challenge_page_is_not_citation_data(self):
        with self.assertRaises(ValueError):
            parse_profile('<html><title>Access unavailable</title></html>', 'author1')

    def test_unknown_citation_text_is_not_zero(self):
        with self.assertRaises(ValueError):
            parse_profile(row(count='N/A'), 'author1')

    def test_network_failure_preserves_verified_counts(self):
        with tempfile.TemporaryDirectory(prefix='scholar-check-', dir=Path(__file__).parent) as folder:
            output = Path(folder) / 'snapshot.json'
            existing = '{"publications":{"paper1":{"citations":12}}}'
            output.write_text(existing, encoding='utf-8')
            with patch('sys.argv', ['update_scholar_citations.py', '--author', 'author1', '--output', str(output)]), \
                    patch('update_scholar_citations.urlopen', side_effect=OSError('Unavailable')), \
                    redirect_stdout(io.StringIO()):
                self.assertEqual(main(), 0)
            self.assertEqual(output.read_text(encoding='utf-8'), existing)


if __name__ == '__main__':
    unittest.main()
