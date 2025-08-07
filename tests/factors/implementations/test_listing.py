from datetime import datetime, timezone, timedelta

from pow2core.factors.implementations.listing_days import ListingDaysFactorByLinear
from pow2core.factors.implementations.listing_count import ListingCountFactorByThreshold
from pow2core.factors.implementations.listing import ListingFactor


class TestListingDaysFactorByLinear:
    now = datetime.strptime("2025-08-07 02:00:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    listing_days_factor = ListingDaysFactorByLinear(
        now=now,
        tz_hours=8,
        min_listing_days=1,
        max_listing_days=10,
        min_weight=1,
        max_weight=5,
        precision=2,
    )

    listing_count_factor = ListingCountFactorByThreshold(
        thresholds=[20, 10, 0],
        weights=[0.25, 0.5, 1],
    )

    def test_real_listing_count(self):
        factor = ListingFactor(
            listing_days_factor=self.listing_days_factor,
            listing_count_factor=self.listing_count_factor,
        )
        listing_count = 10
        listing_count_weight = self.listing_count_factor.get_weight(listing_count)

        listing_start_at = self.now - timedelta(days=5)
        listing_days_weight = self.listing_days_factor.get_weight(listing_start_at)

        result = factor.get_weight(
            listing_count=listing_count,
            listing_start_at=listing_start_at,
        )
        assert result.value == listing_count
        assert result.weight == listing_count_weight.weight
        assert result.children[self.listing_count_factor.name].value == listing_count
        assert result.children[self.listing_count_factor.name].weight == listing_count_weight.weight
        assert result.children[self.listing_days_factor.name].value == 6
        assert result.children[self.listing_days_factor.name].weight == listing_days_weight.weight

    def test_real_listing_days(self):
        factor = ListingFactor(
            listing_days_factor=self.listing_days_factor,
            listing_count_factor=self.listing_count_factor,
        )
        listing_count = 9
        listing_count_weight = self.listing_count_factor.get_weight(listing_count)
        listing_start_at = self.now - timedelta(days=5)
        listing_days_weight = self.listing_days_factor.get_weight(listing_start_at)
        result = factor.get_weight(
            listing_count=listing_count,
            listing_start_at=listing_start_at,
        )
        assert result.value == listing_days_weight.value
        assert result.weight == listing_days_weight.weight
        assert result.children[self.listing_days_factor.name].value == 6
        assert result.children[self.listing_days_factor.name].weight == listing_days_weight.weight
        assert result.children[self.listing_count_factor.name].value == listing_count
        assert result.children[self.listing_count_factor.name].weight == listing_count_weight.weight
