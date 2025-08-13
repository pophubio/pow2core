from pow2core.factors.implementations.mining_limit_reached import MiningLimitReachedFactorByFixed


class TestMiningLimitReachedFactorByFixed:
    def test_get_weight(self):
        factor = MiningLimitReachedFactorByFixed(
            weights={True: 0, False: 1},
            precision=2,
        )
        assert factor.get_weight(is_reached=True).weight == 0
        assert factor.get_weight(is_reached=False).weight == 1
