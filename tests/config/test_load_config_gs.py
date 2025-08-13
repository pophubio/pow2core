from pow2core.config.load_config import LoadMineSeasonConfig


class TestLoadConfigGS:
    def test_load_config_gs_s3(self):
        config = LoadMineSeasonConfig().load_config("gs-s3")
        assert config is not None
