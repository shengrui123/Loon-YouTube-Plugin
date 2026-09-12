import unittest
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1] / "Douyin.Clean.Loon.plugin"
TEXT = PLUGIN.read_text()
ACTIVE = [line.strip() for line in TEXT.splitlines() if line.strip() and not line.startswith("#")]


class DouyinSplashPluginTests(unittest.TestCase):
    def test_contains_only_request_rewrite(self):
        self.assertFalse(any(line.startswith("response if") for line in ACTIVE))
        self.assertNotIn("[Script]", ACTIVE)
        requests = [line for line in ACTIVE if line.startswith("request if")]
        self.assertEqual(len(requests), 1)

    def test_covers_known_splash_paths(self):
        rule = next(line for line in ACTIVE if line.startswith("request if"))
        for marker in ("splash", "luna", "launch", "advert"):
            self.assertIn(marker, rule)

    def test_direct_rules_are_limited_to_port_6443(self):
        rules = [line for line in ACTIVE if "IP-CIDR" in line]
        self.assertEqual(len(rules), 5)
        self.assertTrue(all("DEST-PORT,6443" in line for line in rules))

    def test_no_page_or_feed_cleanup(self):
        functional = "\n".join(
            line for line in ACTIVE
            if line.startswith(("request if", "response if")) or line == "[Script]"
        )
        for marker in ("homepage", "sidebar", "request_combine", "follow/feed", "search/item"):
            self.assertNotIn(marker, functional)


if __name__ == "__main__":
    unittest.main()
