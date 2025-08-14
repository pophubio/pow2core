from pow2core.config.load_config import LoadMineSeasonConfig
from pow2core.factors.const import FACTOR_NAME_LISTING_STATS


class TestLoadConfigGCW:
    def test_load_config_gcw_s6(self):
        config = LoadMineSeasonConfig().load_config("gcw-s6")
        assert config is not None

        factors = config.cpu.factors
        contains_listing_stats = False

        for factor in factors:
            if factor.name == FACTOR_NAME_LISTING_STATS:
                contains_listing_stats = True
                assert factor.config is not None
                assert factor.config.max_weight == 5
                assert factor.config.is_visible is True
                assert factor.config.algorithm == ""

        assert contains_listing_stats
