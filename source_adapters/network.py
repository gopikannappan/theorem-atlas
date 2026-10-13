"""Bounded HTTPS reads from the public GitHub endpoints used by the adapters."""
import re
import subprocess
from urllib.parse import urlsplit

SHA = re.compile(r'[0-9a-f]{40}')
REPOSITORY = re.compile(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+')
ALLOWED_HOSTS = {'api.github.com', 'raw.githubusercontent.com'}


def safe_path(path):
    if not isinstance(path, str) or not path or path.startswith('/') or '\\' in path or ':' in path:
        raise ValueError('Expected a safe relative upstream path')
    if any(part in {'', '.', '..'} for part in path.split('/')) or any(ord(c) < 32 or ord(c) == 127 for c in path):
        raise ValueError('Invalid upstream path')
    return path


def source_identity(repository, commit):
    if not REPOSITORY.fullmatch(repository) or not SHA.fullmatch(commit):
        raise ValueError('Expected a GitHub repository and exact commit SHA')
    slug = repository.removeprefix('https://github.com/')
    if any(part in {'.', '..'} for part in slug.split('/')):
        raise ValueError('Invalid repository name')
    return slug


def fetch_bytes(url, max_bytes=8 * 1024 * 1024):
    parts = urlsplit(url)
    if (parts.scheme != 'https' or parts.hostname not in ALLOWED_HOSTS or parts.port not in {None, 443}
        or parts.username or parts.password or parts.fragment
        or any(ord(c) < 32 or ord(c) == 127 for c in url)):
        raise ValueError('Only public GitHub HTTPS download endpoints are permitted')
    # --disable is first so a local .curlrc cannot add credentials or change behavior.
    # Redirects are intentionally not followed; source changes require explicit inspection.
    payload = subprocess.check_output([
        'curl', '--disable', '--fail', '--silent', '--show-error', '--proto', '=https',
        '--max-time', '60', '--max-filesize', str(max_bytes), url,
    ], timeout=70)
    if len(payload) > max_bytes:
        raise ValueError('Source exceeds download budget')
    return payload


def fetch_text(url):
    return fetch_bytes(url).decode('utf-8')
