from pow2core.factors.implementations.is_listing import IsListingFactorByFixed


class TestIsListingFactorByFixed:
    def test_get_weight(self):
        factor = IsListingFactorByFixed(
            weights={True: 1, False: 0},
            precision=2,
        )
        assert factor.get_weight(is_listing=True).weight == 1
        assert factor.get_weight(is_listing=False).weight == 0
