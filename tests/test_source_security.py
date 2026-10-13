import hashlib
import io
import unittest
import zipfile
from unittest.mock import patch
from source_adapters.network import fetch_bytes, safe_path, source_identity
from source_adapters.external import parse_archive

class SourceSecurityTests(unittest.TestCase):
    def test_downloads_reject_local_non_https_and_credential_urls(self):
        for url in ['file:///etc/passwd', 'http://raw.githubusercontent.com/test',
                    'https://127.0.0.1/test', 'https://example.com/test',
                    'https://user:password@api.github.com/test', 'https://api.github.com:8443/test']:
            with self.subTest(url=url), patch('source_adapters.network.subprocess.check_output') as command:
                with self.assertRaises(ValueError): fetch_bytes(url)
                command.assert_not_called()

    def test_download_command_disables_curl_config_and_redirects(self):
        with patch('source_adapters.network.subprocess.check_output', return_value=b'{}') as command:
            fetch_bytes('https://api.github.com/repos/example/repo')
        args = command.call_args.args[0]
        self.assertEqual(args[:2], ['curl', '--disable'])
        self.assertNotIn('--location', args)
        self.assertNotIn('-L', args)
        self.assertEqual(command.call_args.kwargs['timeout'], 70)
        self.assertIn('--max-filesize', args)

    def test_download_size_is_checked_even_after_fetch(self):
        with patch('source_adapters.network.subprocess.check_output', return_value=b'oversized'):
            with self.assertRaisesRegex(ValueError, 'budget'): fetch_bytes('https://api.github.com/test', max_bytes=4)

    def test_invalid_pins_and_paths_fail_closed(self):
        with self.assertRaises(ValueError): source_identity('https://example.com/a/b', 'a' * 40)
        with self.assertRaises(ValueError): source_identity('https://github.com/a/b', 'main')
        for path in ['/absolute.lean', '../escape.lean', 'a/../escape.lean', 'C:/drive.lean', 'a\\b.lean', 'a\x00b.lean']:
            with self.subTest(path=path), self.assertRaises(ValueError): safe_path(path)
        self.assertEqual(safe_path('preprints/CAT(0)/paper.pdf'), 'preprints/CAT(0)/paper.pdf')

    def test_archive_traversal_is_rejected_without_extracting(self):
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, 'w') as archive: archive.writestr('../escape.lean', 'text')
        config = {'archive_sha256': hashlib.sha256(payload.getvalue()).hexdigest(), 'expected_members': 1}
        with self.assertRaises(ValueError): parse_archive(config, payload.getvalue())

    def test_compressed_member_limit_is_checked_before_read(self):
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('test/too-large.lean', b'x' * (8 * 1024 * 1024 + 1))
        config = {'archive_sha256': hashlib.sha256(payload.getvalue()).hexdigest(), 'expected_members': 1}
        with self.assertRaisesRegex(ValueError, 'decompression'): parse_archive(config, payload.getvalue())

if __name__ == '__main__': unittest.main()
