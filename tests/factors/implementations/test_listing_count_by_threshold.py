from decimal import Decimal

from pow2core.factors.implementations.listing_count import ListingCountFactorByThreshold


class TestListingCountFactorByThreshold:
    def test_gcw(self):
        factor = ListingCountFactorByThreshold(
            thresholds=[20, 10, 0],
            weights=[0.25, 0.5, 1],
        )

        assert factor.get_weight(21).weight == Decimal("0.25")
        assert factor.get_weight(20).weight == Decimal("0.25")
        assert factor.get_weight(19).weight == Decimal("0.5")
        assert factor.get_weight(10).weight == Decimal("0.5")
        assert factor.get_weight(9).weight == Decimal("1")
        assert factor.get_weight(0).weight == Decimal("1")
