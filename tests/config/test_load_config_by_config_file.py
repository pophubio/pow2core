from pathlib import Path

from pow2core.config.load_config import LoadMineSeasonConfig


def test_load_config_by_config_file():
    config_path = Path(__file__).parent / "example.yaml"
    config = LoadMineSeasonConfig().load_config(config_file=config_path)
    assert config.season.slug == "test"
