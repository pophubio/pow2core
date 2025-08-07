# 更新日志

本文档记录 Pow2Core 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
项目遵循 [语义化版本控制](https://semver.org/spec/v2.0.0.html) 规范。

## [1.0.0] - 2025-08-07

### 新增功能
- **核心库架构**: 完整实现 Pow2Core 挖矿计算核心库
  - 基于装饰器注册模式的因子系统
  - 五种核心算法：fixed（固定）、linear（线性）、normalize（归一化）、threshold（阈值）、value（数值）
  - 九种因子实现：asset（资产）、rare（稀有度）、volume（交易量）、slot（卡槽）、listing（挂单）、listing_count（挂单计数）、listing_days（挂单天数）、d_days（持有天数）、combination（组合）
  - CPU 计算器用于 NFT 挖矿权重计算
  - 钻石分配策略：固定组（FixedGroup）和等级组（LevelGroup）

- **配置系统**:
  - 基于 YAML 的挖矿赛季配置
  - 使用 Pydantic 进行配置结构验证，确保类型安全
  - 包含不同挖矿赛季的示例配置（GCW S6、GS S3、OG S4）
  - 新增详细的示例配置文件 `s1.yaml`，包含完整的赛季参数设置

- **开发环境**:
  - 支持 Python 3.12+ 及现代化工具链
  - 集成 UV 包管理器，包含锁定文件
  - 使用 Ruff 进行代码格式化和检查，配置全面的规则集
  - 基于 Pytest 的测试框架，提供广泛的测试覆盖
  - 针对所有算法和实现的完整测试套件

- **项目基础设施**:
  - GitHub 问题模板，支持 Bug 报告、功能请求和文档改进
  - Git 配置，包含适当的忽略规则
  - 通过 py.typed 标记提供类型提示支持
  - 区分开发和生产依赖

- **文档**:
  - 完善的 README.md，包含使用示例和 NFT 数据结构说明
  - CLAUDE.md 提供开发指导和架构概述
  - 详细的项目结构文档

### 技术细节
- **依赖项**: numpy>=2.3.2, pydantic>=2.11.7, pyyaml>=6.0.2
- **架构模式**: 装饰器注册模式，算法和分配策略采用策略模式
- **测试**: 完整的单元测试覆盖，支持参数化测试
- **代码质量**: 88 字符行长度限制，Python 3.12 目标版本，全面的代码检查规则
