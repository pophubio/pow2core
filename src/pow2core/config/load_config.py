from pathlib import Path

import yaml

from ..distribute_strategies.const import (
    DISTRIBUTE_STRATEGY_FIXED_GROUP,
    DISTRIBUTE_STRATEGY_LEVEL_GROUP,
)
# 确保所有因子实现被导入和注册
from ..factors import implementations  # noqa: F401 - 导入以触发注册
from ..factors.registry import FactorRegistry
from ..distribute_strategies.schema import FixedGroupStrategyConfig, LevelGroupStrategyConfig
from ..config.schema import (
    MineSeasonConfig,
    CollectionConfig,
    SeasonConfig,
    CPUConfig,
    DiamondConfig,
    CombinationConfig,
    FactorConfig,
)


class LoadMineSeasonConfig:
    """加载挖钻赛季配置"""

    def __init__(self) -> None:
        self.config_dir = Path(__file__).parent.parent / "resource/config"

    def load_config(self, season_slug: str) -> MineSeasonConfig:
        """
        加载挖钻赛季配置, 并格式化
        """
        yaml_config = self.load_yaml_config(season_slug)

        collection_config = self.load_collection_config(yaml_config)
        season_config = self.load_season_config(yaml_config)
        cpu_config = self.load_cpu_config(yaml_config)
        diamond_config = self.load_diamond_config(yaml_config)
        combination_config = self.load_combination_config(yaml_config)

        return MineSeasonConfig(
            collection=collection_config,
            category=yaml_config["category"],
            image=yaml_config["image"],
            season=season_config,
            cpu=cpu_config,
            diamond=diamond_config,
            combination=combination_config,
        )

    def load_yaml_config(self, season_slug: str) -> dict:
        """从yaml中读取配置"""
        season_slug = season_slug.lower().split("-")
        if len(season_slug) != 2:
            raise ValueError(f"Invalid season slug: {season_slug}")

        config_path = self.config_dir / season_slug[0] / f"{season_slug[1]}.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with config_path.open() as f:
            return yaml.safe_load(f)

    def load_collection_config(self, yaml_config: dict) -> CollectionConfig:
        """加载合集配置并格式化"""
        if "collection" not in yaml_config:
            raise ValueError("collection config not found")

        return CollectionConfig.model_validate(yaml_config["collection"])

    def load_season_config(self, yaml_config: dict) -> SeasonConfig:
        """加载赛季配置并格式化"""
        if "season" not in yaml_config:
            raise ValueError("season config not found")

        return SeasonConfig.model_validate(yaml_config["season"])

    def load_cpu_config(self, yaml_config: dict) -> CPUConfig:
        """加载CPU配置并格式化"""
        if "cpu" not in yaml_config:
            raise ValueError("cpu config not found")

        factors = []
        for factor in yaml_config["cpu"]["factors"]:
            factors.append(self.load_factor_config(factor))

        return CPUConfig(
            base=yaml_config["cpu"]["base"],
            factors=factors,
        )

    def load_factor_config(self, factor: dict) -> FactorConfig:
        """加载因子配置并格式化"""
        factor_name = factor["name"]
        config = factor.get("config")
        priority = factor["priority"]
        children = factor.get("children")

        if children:
            # 复合因子处理 (如 ListingFactor)
            implementations = FactorRegistry.get_all_implementations(factor_name)
            if not implementations:
                raise ValueError(f"{factor_name} has no implementation")
            impl = implementations[0]  # 复合因子通常只有一个实现
            children = [self.load_factor_config(child) for child in children]
        else:
            # 单一因子处理
            algorithm = config["algorithm"]
            method = config.get("method")

            try:
                impl = FactorRegistry.get_implementation(factor_name, algorithm, method)
            except ValueError as e:
                raise ValueError(f"Factor {factor_name} implementation not found") from e

            config = impl.config_schema.model_validate(config)

        return FactorConfig(
            name=factor_name,
            implementation=impl.implementation_class,
            config=config,
            priority=priority,
            children=children,
        )

    def load_diamond_config(self, yaml_config: dict) -> DiamondConfig:
        """加载钻石配置并格式化"""
        if "diamond" not in yaml_config:
            raise ValueError("diamond config not found")

        yaml_config_diamond = yaml_config["diamond"]
        strategy = yaml_config_diamond["strategy"]
        if strategy == DISTRIBUTE_STRATEGY_FIXED_GROUP:
            diamond_config = FixedGroupStrategyConfig.model_validate(yaml_config_diamond["config"])
        elif strategy == DISTRIBUTE_STRATEGY_LEVEL_GROUP:
            diamond_config = LevelGroupStrategyConfig.model_validate(yaml_config_diamond["config"])
        else:
            raise ValueError(f"Invalid diamond strategy: {strategy}")

        return DiamondConfig(
            strategy=strategy,
            config=diamond_config,
        )

    def load_combination_config(self, yaml_config: dict) -> CombinationConfig:
        """加载变压器配置并格式化"""
        if "combination" not in yaml_config:
            raise ValueError("combination config not found")

        return CombinationConfig.model_validate(yaml_config["combination"])
