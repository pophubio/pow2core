# Pow2Core

Pow2Core 是一个用于 Pow2 挖矿计算的核心库，专门处理 NFT 挖矿中的因子计算和权重分配。

## ✨ 特性

- 🎯 **多因子权重计算系统**：支持稀有度、资产、交易量、挂单等多种因子
- 🔧 **灵活的算法支持**：Fixed、Linear、Normalize、Threshold、Value 五种基础算法
- 📊 **装饰器注册模式**：自动化的因子实现管理
- ⚙️ **配置驱动架构**：通过 YAML 配置不同赛季的挖矿参数
- 💎 **多种分发策略**：支持固定组和等级组钻石分配
- 🧪 **完整测试覆盖**：全面的单元测试确保代码质量

## 📦 安装

### 前置要求

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (推荐的包管理器)

### 使用 uv 安装

```bash
# 克隆项目
git clone https://github.com/pophubio/pow2core.git
cd pow2core

# 安装依赖
uv sync

# 安装开发依赖
uv sync --dev
```

## 🚀 快速开始

### 基本用法

```python
from pow2core.config.load_config import LoadMineSeasonConfig
from pow2core.cpu.calculator import CPUCalculator

# 加载赛季配置
config_loader = LoadMineSeasonConfig()
season_config = config_loader.load_config("gcw-s6")

# 创建CPU计算器
calculator = CPUCalculator(season_config.cpu)
calculator.load_factors()

# 计算NFT的挖矿权重
nft_data = {
    "rare": 100,
    "asset": 50000,
    "volume": 1000.0,
    # ... 其他因子数据
}

result = calculator.calculate(nft_data)
print(f"计算结果: {result}")
```

### 配置文件示例

```yaml
# src/pow2core/resource/config/gcw/s6.yaml
nft:
  slugs:
    - GoldenCicadaWarrior

season:
  slug: gcw-s6
  title: PoW² 蝉甲S6挖钻
  start_at: "2025-08-01 20:00:00+08"
  epoch_hours: 24
  max_epoch: 15

cpu:
  base: 10000
  factors:
    - name: rare
      priority: 5
      config:
        algorithm: normalize
        method: linear
        min_rare: 1
        max_rare: 9432
        alpha: 1047
```

## 🏗️ 架构设计

### 因子注册系统

Pow2Core 使用装饰器注册模式管理因子实现：

```python
@FactorRegistry.register(
    name=FACTOR_NAME_ASSET,
    algorithm=FACTOR_ALGORITHM_NORMALIZE,
    method=NORMALIZE_METHOD_LOG,
    config_schema=AssetFactorByNormalizeConfig,
)
class AssetFactorByLogNormalize(FactorByNormalize):
    def __init__(self, ratio: float, min_alpha: float, ...):
        super().__init__(...)
```

### 支持的因子类型

| 因子名称 | 说明 | 支持算法 |
|---------|------|----------|
| rare | 稀有度因子 | Fixed, Normalize |
| asset | 资产因子 | Normalize |
| volume | 交易量因子 | Linear, Normalize |
| slot | 卡槽因子 | Fixed |
| d_days | 持有天数因子 | Normalize |
| listing | 挂单因子 | 复合因子 |

### 算法类型

- **Fixed**: 固定权重映射
- **Linear**: 线性插值计算
- **Normalize**: 归一化计算（支持对数和线性方法）
- **Threshold**: 阈值分段计算
- **Value**: 直接数值计算

## 🧪 开发

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定模块测试
uv run pytest tests/factors/

# 运行单个测试
uv run pytest tests/factors/algorithms/test_fixed.py::TestFactorByFixed::test_init_with_int_weights

```

### 代码质量检查

```bash
# 代码格式化
uv run ruff format

# 代码检查
uv run ruff check

# 自动修复
uv run ruff check --fix
```

### 添加新因子

1. 在 `src/pow2core/factors/implementations/` 创建新的实现类
2. 使用 `@FactorRegistry.register()` 装饰器注册
3. 在 `src/pow2core/factors/schema.py` 添加配置 Schema
4. 在 `src/pow2core/factors/const.py` 定义常量
5. 添加单元测试

示例：

```python
# src/pow2core/factors/implementations/my_factor.py
@FactorRegistry.register(
    name=FACTOR_NAME_MY_FACTOR,
    algorithm=FACTOR_ALGORITHM_LINEAR,
    config_schema=MyFactorConfig,
)
class MyFactor(FactorByLinear):
    def __init__(self, min_value: int, max_value: int, **kwargs):
        super().__init__(
            name=FACTOR_NAME_MY_FACTOR,
            min_value=min_value,
            max_value=max_value,
            **kwargs
        )
```

## 📁 项目结构

```
src/pow2core/
├── config/              # 配置加载和验证
├── cpu/                 # CPU计算器
├── distribute_strategies/ # 分发策略
├── factors/             # 因子系统
│   ├── algorithms/      # 基础算法实现
│   ├── implementations/ # 具体因子实现
│   ├── registry.py      # 因子注册中心
│   └── schema.py        # 配置Schema
└── resource/
    └── config/          # YAML配置文件
```

## 🤝 贡献

### 报告问题

我们提供了多种Issue模板来帮助您更好地报告问题：

- 🐛 **[Bug Report](/.github/ISSUE_TEMPLATE/bug_report.md)** - 报告功能错误或异常
- ✨ **[Feature Request](/.github/ISSUE_TEMPLATE/feature_request.md)** - 建议新功能或改进
- 📚 **[Documentation](/.github/ISSUE_TEMPLATE/documentation.md)** - 文档问题或改进建议
- ⚡ **[Performance Issue](/.github/ISSUE_TEMPLATE/performance.md)** - 性能问题或优化建议
- ⚙️ **[Configuration Issue](/.github/ISSUE_TEMPLATE/configuration.md)** - 配置相关问题
- 📝 **[General Issue](/.github/ISSUE_TEMPLATE/default.md)** - 其他类型的问题

### 开发贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 开发指南

- 确保所有测试通过 (`uv run pytest`)
- 遵循代码风格 (`uv run ruff check`)
- 添加适当的测试覆盖
- 更新相关文档

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## 👥 作者

- **POP Lab**: [twitter](https://x.com/pophubiolab)

## 🙏 致谢

感谢所有为 Pow2Core 项目做出贡献的开发者们！
