from pow2core.config.load_config import LoadMineSeasonConfig


class TestLoadConfigOG:
    def test_load_config_og_s4(self):
        config = LoadMineSeasonConfig().load_config("og-s4")
        assert config is not None
