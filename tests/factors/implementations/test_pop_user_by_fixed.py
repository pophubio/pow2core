from pow2core.factors.implementations.pop_user import POPUserFactorByFixed


class TestPOPUserFactorByFixed:
    def test_get_weight(self):
        factor = POPUserFactorByFixed(
            weights={True: 1, False: 0},
            precision=2,
        )
        assert factor.get_weight(is_pop_user=True).weight == 1
        assert factor.get_weight(is_pop_user=False).weight == 0
