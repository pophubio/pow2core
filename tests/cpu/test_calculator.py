from datetime import datetime, timezone, timedelta
from decimal import Decimal

from pow2core.config.load_config import LoadMineSeasonConfig
from pow2core.cpu.calculator import CPUCalculator


class TestCalculator:
    def test_example_s1(self):
        now = datetime.now(timezone.utc)
        # 加载赛季配置
        config_loader = LoadMineSeasonConfig()
        season_config = config_loader.load_config("example-s1")

        # 创建CPU计算器
        calculator = CPUCalculator(season_config.cpu)
        calculator.load_factors()

        # 计算NFT的挖矿权重
        nft_data = {
            "rare": {"rare": 100},
            "d_days": {"start_at": now-timedelta(days=10)},
            "combination": {"ratio": Decimal(2)},
            "listing_stats": {
                "listing_start_at": now-timedelta(days=3),
                "listing_count": 0,
            },
        }

        result = calculator.calculate(nft_data)
        for factor_name, factor_weight in result.factor_weights.items():
            print(f"factor: {factor_name}")
            print(f"  weight: {factor_weight.weight}")
            print(f"  value: {factor_weight.value}")
        print("cpu:", result.cpu)

