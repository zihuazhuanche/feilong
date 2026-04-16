import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / 'scripts' / 'blog-pusher.py'


spec = importlib.util.spec_from_file_location('blog_pusher', MODULE_PATH)
blog_pusher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blog_pusher)


class BlogPusherSecurityTests(unittest.TestCase):
    def test_push_with_token_does_not_rewrite_remote_url(self):
        calls = []
        captured_env = {}

        def fake_run(cmd, cwd=None, check=None, text=None, capture_output=False, env=None):
            calls.append(cmd)
            if env:
                captured_env.update(env)
            if cmd[:4] == ['git', 'remote', 'get-url', 'origin']:
                return subprocess.CompletedProcess(cmd, 0, stdout='https://github.com/zihuazhuanche/feilong.git\n')
            return subprocess.CompletedProcess(cmd, 0, stdout='')

        with patch.object(blog_pusher.subprocess, 'run', side_effect=fake_run):
            blog_pusher.push_with_token('ghp_test_secret')

        forbidden = [cmd for cmd in calls if cmd[:4] == ['git', 'remote', 'set-url', 'origin']]
        self.assertEqual(forbidden, [], 'push should not rewrite git remote URLs')

        push_calls = [cmd for cmd in calls if cmd[:2] == ['git', 'push']]
        self.assertEqual(push_calls, [['git', 'push', 'origin', 'main']])
        self.assertEqual(captured_env.get('GIT_CONFIG_COUNT'), '1')
        self.assertEqual(captured_env.get('GIT_CONFIG_KEY_0'), 'http.https://github.com/.extraheader')
        self.assertTrue((captured_env.get('GIT_CONFIG_VALUE_0') or '').startswith('AUTHORIZATION: basic '))
        self.assertNotIn('ghp_test_secret', ' '.join(push_calls[0]))


if __name__ == '__main__':
    unittest.main()
