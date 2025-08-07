---
name: ⚙️ Configuration Issue
about: Report problems with Pow2Core configuration
title: "[CONFIG] "
labels: ["configuration", "needs-triage"]
assignees: []
---

## ⚙️ Configuration Problem

A clear and concise description of the configuration issue you're experiencing.

## 📁 Configuration Details

**Configuration file:** [e.g., `src/pow2core/resource/config/gcw/s6.yaml`]
**Season:** [e.g., gcw-s6, gs-s3, og-s4]

## 🔍 Current Configuration

Please share the relevant configuration section (remove sensitive information):

```yaml
# Example configuration
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

## ❌ Error Message

If you're getting an error, please share the complete error message:

```
Traceback (most recent call last):
  File "your_script.py", line X, in <module>
    ...
```

## ✅ Expected Behavior

A clear and concise description of what you expected to happen with this configuration.

## 🔄 Steps to Reproduce

1. Create configuration file with the above content
2. Load configuration using `LoadMineSeasonConfig()`
3. Try to create `CPUCalculator()`
4. Observe the error/issue

**Code example:**
```python
from pow2core.config.load_config import LoadMineSeasonConfig
from pow2core.cpu.calculator import CPUCalculator

config_loader = LoadMineSeasonConfig()
season_config = config_loader.load_config("gcw-s6")  # This line fails
calculator = CPUCalculator(season_config.cpu)
```

## 🧪 Validation

**Have you validated your configuration?**
- [ ] YAML syntax is correct
- [ ] All required fields are present
- [ ] Field types match expected types
- [ ] Factor names match registered factors
- [ ] Algorithm names are valid

## 🔧 Troubleshooting Steps

**What have you tried?**
- [ ] Checked YAML syntax with online validator
- [ ] Verified factor names in `pow2core.factors.const`
- [ ] Confirmed algorithm names in `pow2core.factors.algorithms`
- [ ] Tested with minimal configuration
- [ ] Compared with working configuration examples

## 📋 Configuration Checklist

**Please confirm:**
- [ ] Configuration file is in the correct location
- [ ] File has `.yaml` extension
- [ ] Indentation uses spaces (not tabs)
- [ ] All required fields are provided
- [ ] No syntax errors in YAML
- [ ] Factor names match exactly (case-sensitive)
- [ ] Algorithm names match exactly (case-sensitive)

## 🖥️ Environment

**System Information:**
- **OS:** [e.g., macOS 14.0]
- **Python:** [e.g., 3.12.0]
- **Pow2Core Version:** [e.g., 0.1.0]
- **Package Manager:** [e.g., uv, pip]

## 📝 Additional Context

Add any other context about the configuration issue here, such as:
- Is this a new configuration or did it work before?
- Are you following a specific example or tutorial?
- What changes did you make recently?
- Are there any custom factors or algorithms involved? 