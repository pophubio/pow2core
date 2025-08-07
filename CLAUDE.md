# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Pow2Core 是一个用于 Pow2 挖矿计算的核心库，主要处理 NFT 挖矿中的因子计算和权重分配。项目使用 Python 3.12+ 开发，采用配置驱动的架构设计。

## 开发命令

### 包管理和环境
```bash
# 安装依赖（包括开发依赖）
uv sync --all-extras

# 安装开发依赖
uv add --dev pytest ruff

# 运行单个测试
uv run pytest tests/factors/algorithms/test_fixed.py::TestFactorByFixed::test_init_with_int_weights

# 运行所有测试
uv run pytest

# 运行特定模块的测试
uv run pytest tests/factors/
```

### 代码质量检查
```bash
# 代码格式化和检查
uv run ruff check
uv run ruff format

# 修复可自动修复的问题
uv run ruff check --fix
```

## 核心架构

### 因子注册系统
项目使用装饰器注册模式管理因子实现：

- **FactorRegistry**: 核心注册中心，位于 `src/pow2core/factors/registry.py`
- **装饰器注册**: 每个因子实现类使用 `@FactorRegistry.register()` 装饰器自动注册
- **因子算法**: 支持 fixed、linear、normalize、threshold、value 五种基础算法
- **因子实现**: 各种具体的因子实现（asset、rare、volume、slot 等）

### 配置系统
- **配置文件**: YAML 格式的赛季配置，位于 `src/pow2core/resource/config/`
- **配置加载**: `LoadMineSeasonConfig` 类负责从 YAML 加载和验证配置
- **配置 Schema**: 使用 Pydantic 模型确保配置的类型安全性

### CPU 计算器
- **CPUCalculator**: 主要计算引擎，基于因子配置计算 NFT 的挖矿权重
- **因子加载**: 动态根据配置实例化对应的因子实现
- **权重计算**: 综合多个因子的权重计算最终结果

### 分发策略
支持两种钻石分配策略：
- **FixedGroup**: 固定组分配
- **LevelGroup**: 等级组分配

## 重要设计模式

### 装饰器注册模式
```python
@FactorRegistry.register(
    name=FACTOR_NAME_ASSET,
    algorithm=FACTOR_ALGORITHM_NORMALIZE,
    method=NORMALIZE_METHOD_LOG,
    config_schema=AssetFactorByNormalizeConfig,
)
class AssetFactorByLogNormalize(FactorByNormalize):
    pass
```

### 配置驱动开发
所有因子参数、算法选择、权重配置都通过 YAML 文件驱动，支持不同赛季使用不同参数。

### 策略模式
分发策略和因子算法都使用策略模式，便于扩展新的计算方法。

## 代码结构要点

- **因子系统**: `src/pow2core/factors/` - 包含算法、实现和注册逻辑
- **配置系统**: `src/pow2core/config/` - 配置加载和验证
- **CPU计算**: `src/pow2core/cpu/` - 主要计算逻辑
- **分发策略**: `src/pow2core/distribute_strategies/` - 钻石分配策略
- **测试**: `tests/` - 完整的单元测试覆盖

## 添加新因子的流程

1. 在 `src/pow2core/factors/implementations/` 中创建新的因子实现类
2. 使用 `@FactorRegistry.register()` 装饰器注册
3. 在 `src/pow2core/factors/schema.py` 中添加对应的配置 Schema
4. 在 `src/pow2core/factors/const.py` 中定义相关常量
5. 在配置文件中使用新因子
6. 添加相应的单元测试

## 测试策略

- 每个因子算法都有独立的测试文件
- 测试覆盖不同的输入参数和边界条件
- 使用 pytest 框架，支持参数化测试
