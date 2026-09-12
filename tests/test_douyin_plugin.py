import json
import re
import subprocess
import unittest
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1] / "Douyin.Clean.Loon.plugin"
TEXT = PLUGIN.read_text()
FILTERS = re.findall(r"response\.json\.jq\(`([^`]*)`\)", TEXT)


def jq(index, value):
    result = subprocess.run(
        ["jq", "-c", FILTERS[index]],
        input=json.dumps(value),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class DouyinPluginTests(unittest.TestCase):
    def setUp(self):
        self.home = {
            "data": {
                "tab_config": {"experiment": True},
                "tab_list": [{
                    "extra": {
                        "tab_list": [
                            {"tab_id": "homepage_follow"},
                            {"tab_id": "homepage_mall"},
                            {"tab_id": "homepage_hot_container"},
                            {"tab_id": "homepage_tablive"},
                        ],
                        "side_bar": {
                            "modules": [
                                {"module_title": "常用功能", "items": []},
                                {"module_title": "设置", "items": [{"name": "设置"}]},
                            ]
                        },
                    }
                }],
            }
        }

    def test_minimal_tabs(self):
        result = jq(0, self.home)
        ids = [item["tab_id"] for item in result["data"]["tab_list"][0]["extra"]["tab_list"]]
        self.assertEqual(ids, ["homepage_follow", "homepage_hot_container"])

    def test_keep_live(self):
        result = jq(1, self.home)
        ids = [item["tab_id"] for item in result["data"]["tab_list"][0]["extra"]["tab_list"]]
        self.assertEqual(ids, ["homepage_follow", "homepage_hot_container", "homepage_tablive"])

    def test_direct_tab_list_shape_seen_in_gray_releases(self):
        value = {"data": {"tab_list": [
            {"channel_id": "homepage_nearby"},
            {"channel_id": "homepage_follow"},
            {"channel_id": "homepage_hot_container"},
        ]}}
        result = jq(0, value)
        self.assertEqual(
            [item["channel_id"] for item in result["data"]["tab_list"]],
            ["homepage_follow", "homepage_hot_container"],
        )

    def test_sidebar(self):
        result = jq(2, self.home)
        modules = result["data"]["tab_list"][0]["extra"]["side_bar"]["modules"]
        self.assertEqual([item["module_title"] for item in modules], ["设置"])

    def test_settings(self):
        value = {"data": {"/service/settings/v3/": {"body": {"data": {"settings": {
            "homepage_two_session_tab_skin_2025": True,
            "homepage_tab_skin_enable": True,
            "dynamic_plus_icon_config": {"icon": "promotion"},
            "unrelated": True,
        }}}}}}
        result = jq(3, value)
        settings = result["data"]["/service/settings/v3/"]["body"]["data"]["settings"]
        self.assertFalse(settings["homepage_two_session_tab_skin_2025"])
        self.assertFalse(settings["homepage_tab_skin_enable"])
        self.assertNotIn("dynamic_plus_icon_config", settings)
        self.assertTrue(settings["unrelated"])

    def test_no_shared_ip_blocking(self):
        active = [line for line in TEXT.splitlines() if line and not line.startswith("#")]
        self.assertFalse(any("IP-CIDR" in line or "DEST-PORT" in line for line in active))


if __name__ == "__main__":
    unittest.main()
