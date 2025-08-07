from datetime import datetime, timezone, timedelta
from decimal import Decimal

from pow2core.factors.implementations.listing_days import ListingDaysFactorByLinear


class TestListingDaysFactorByLinear:
    def test_gcw(self):
        now = datetime.strptime("2025-08-07 02:00:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        factor = ListingDaysFactorByLinear(
            now=now,
            tz_hours=8,
            min_listing_days=1,
            max_listing_days=10,
            min_weight=1,
            max_weight=5,
            precision=2,
        )

        assert factor.get_weight(None).weight == Decimal("5.00")
        assert factor.get_weight(now-timedelta(days=0)).weight == Decimal("1.00")
        assert factor.get_weight(now-timedelta(days=4)).weight == Decimal("2.78")
        assert factor.get_weight(now-timedelta(days=9)).weight == Decimal("5.00")
        assert factor.get_weight(now-timedelta(days=10)).weight == Decimal("5.00")
        assert factor.get_weight(now-timedelta(days=11)).weight == Decimal("5.00")
        assert factor.get_weight(now-timedelta(days=110)).weight == Decimal("5.00")
