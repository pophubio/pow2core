from pow2core.config.load_config import LoadMineSeasonConfig


class TestLoadConfigGCW:
    def test_load_config_gcw_s6(self):
        config = LoadMineSeasonConfig().load_config("gcw-s6")
        assert config is not None
