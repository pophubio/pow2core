---
name: ⚡ Performance Issue
about: Report performance problems or optimization suggestions
title: "[PERF] "
labels: ["performance", "needs-triage"]
assignees: []
---

## 🐌 Performance Problem

A clear and concise description of the performance issue you're experiencing.

## 📊 Current Performance

**What is the current performance?**
- **Operation:** [e.g., factor calculation, config loading, CPU computation]
- **Current time:** [e.g., 5 seconds for 1000 NFTs]
- **Resource usage:** [e.g., CPU: 80%, Memory: 2GB]
- **Scale:** [e.g., 1000 NFTs, 100 factors]

## 🎯 Expected Performance

**What performance do you expect?**
- **Target time:** [e.g., 1 second for 1000 NFTs]
- **Resource usage:** [e.g., CPU: 20%, Memory: 500MB]

## 🔄 Steps to Reproduce

1. Load configuration with `LoadMineSeasonConfig()`
2. Create calculator with `CPUCalculator()`
3. Process [X] NFTs with [Y] factors
4. Observe slow performance

**Code example:**
```python
from pow2core.config.load_config import LoadMineSeasonConfig
from pow2core.cpu.calculator import CPUCalculator
import time

# Start timing
start_time = time.time()

config_loader = LoadMineSeasonConfig()
season_config = config_loader.load_config("gcw-s6")
calculator = CPUCalculator(season_config.cpu)
calculator.load_factors()

# Process NFTs
for nft in nft_list:
    result = calculator.calculate(nft)

# End timing
end_time = time.time()
print(f"Processing time: {end_time - start_time:.2f} seconds")
```

## 📈 Performance Metrics

**Please provide:**
- [ ] Execution time measurements
- [ ] Memory usage (if applicable)
- [ ] CPU usage (if applicable)
- [ ] Number of items processed
- [ ] System specifications

**System Info:**
- **OS:** [e.g., macOS 14.0]
- **Python:** [e.g., 3.12.0]
- **CPU:** [e.g., Apple M2, Intel i7]
- **Memory:** [e.g., 16GB]
- **Storage:** [e.g., SSD, HDD]

## 🔍 Profiling Results

If you've done any profiling, please share the results:

```bash
# Example profiling command
python -m cProfile -o profile.stats your_script.py
```

## 💡 Optimization Ideas

If you have suggestions for optimization, please describe them:

- [ ] Algorithm improvements
- [ ] Data structure changes
- [ ] Caching strategies
- [ ] Parallel processing
- [ ] Memory optimization
- [ ] Other: [Please specify]

## 📋 Impact Assessment

**How critical is this performance issue?**
- [ ] Critical - blocks production use
- [ ] High - significantly impacts user experience
- [ ] Medium - noticeable but tolerable
- [ ] Low - minor inconvenience

## 🔗 Related Issues

- Related to #[issue number]
- Similar to #[issue number]
- Blocked by #[issue number]

## 📝 Additional Context

Add any other context about the performance issue here, such as:
- When did this start happening?
- Has performance degraded over time?
- Are there specific conditions that make it worse?
- Workarounds you've tried 