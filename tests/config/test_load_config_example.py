from pow2core.config.load_config import LoadMineSeasonConfig


class TestLoadConfigExample:
    def test_load_config_example_s1(self):
        config = LoadMineSeasonConfig().load_config("example-s1")
        assert config is not None
