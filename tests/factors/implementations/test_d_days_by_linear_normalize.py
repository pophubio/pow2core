from datetime import datetime, timezone, timedelta
from decimal import Decimal

from pow2core.factors.implementations.d_days import DDaysFactorByLinearNormalize


class TestDDaysFactorByLinearNormalize:
    def test_with_diff_tz(self):
        created_at = datetime.strptime("2024-11-29 10:09:52", "%Y-%m-%d %H:%M:%S")
        created_at = created_at.replace(tzinfo=timezone(timedelta(hours=0)))

        now = datetime.strptime("2025-08-05 23:00:00", "%Y-%m-%d %H:%M:%S")
        now = now.replace(tzinfo=timezone(timedelta(hours=8)))
        factor = DDaysFactorByLinearNormalize(
            created_at=created_at,
            multiplier=10,
            now=now,
            tz_hours=8,
            precision=2,
            max_weight=1.1,
            is_visible=True,
        )

        assert factor.get_weight(now-timedelta(days=4)).weight == Decimal("1.00")
        assert factor.get_weight(now-timedelta(days=146)).weight == Decimal("1.06")
        assert factor.get_weight(now-timedelta(days=206)).weight == Decimal("1.08")

    def test_with_same_tz(self):
        created_at = datetime.strptime("2024-11-29 02:09:52", "%Y-%m-%d %H:%M:%S")
        created_at = created_at.replace(tzinfo=timezone(timedelta(hours=0)))

        now = datetime.strptime("2025-08-05 23:00:00", "%Y-%m-%d %H:%M:%S")
        now = now.replace(tzinfo=timezone(timedelta(hours=8)))
        factor = DDaysFactorByLinearNormalize(
            created_at=created_at,
            multiplier=10,
            now=now,
            tz_hours=8,
            precision=2,
            max_weight=1.1,
            is_visible=True,
        )

        assert factor.get_weight(now-timedelta(days=4)).weight == Decimal("1.00")
        assert factor.get_weight(now-timedelta(days=146)).weight == Decimal("1.06")
        assert factor.get_weight(now-timedelta(days=206)).weight == Decimal("1.08")
