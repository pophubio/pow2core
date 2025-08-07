import pytest

from pow2core.distribute_strategies.level_group import LevelGroupStrategy


class TestLevelGroupStrategy:
    def test_init_with_valid_parameters(self):
        """测试使用有效参数初始化"""
        group_ratios = [0.1, 0.3, 0.6]
        base_diamond_groups = [100, 50, 25]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500},
            {"level": 2, "users": 100, "diamonds": 5000},
            {"level": 3, "users": 200, "diamonds": 10000}
        ]

        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        assert strategy.group_ratios == [0.1, 0.3, 0.6]
        assert strategy.base_diamond_groups == [100, 50, 25]
        assert strategy.level_thresholds == [
            {"level": 3, "users": 200, "diamonds": 10000},
            {"level": 2, "users": 100, "diamonds": 5000},
            {"level": 1, "users": 50, "diamonds": 2500},
        ]

    def test_init_with_invalid_ratios_sum(self):
        """测试比率和不等于1的情况"""
        group_ratios = [0.1, 0.3, 0.5]  # 总和为0.9，不等于1
        base_diamond_groups = [100, 50, 25]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]

        with pytest.raises(ValueError, match="每组人数占总人数的百分比之和必须为1"):
            LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

    def test_init_with_unsorted_level_thresholds(self):
        """测试未排序的等级阈值"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 3, "users": 200, "diamonds": 10000},
            {"level": 1, "users": 50, "diamonds": 2500},
            {"level": 2, "users": 100, "diamonds": 5000}
        ]

        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        # 验证等级阈值已按level排序
        expected_sorted = [
            {"level": 3, "users": 200, "diamonds": 10000},
            {"level": 2, "users": 100, "diamonds": 5000},
            {"level": 1, "users": 50, "diamonds": 2500},
        ]
        assert strategy.level_thresholds == expected_sorted

    def test_get_user_and_diamond_groups_below_first_threshold(self):
        """测试总人数低于第一个阈值的情况"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        user_groups, diamond_groups = strategy.get_user_and_diamond_groups(30)

        # 当总人数低于第一个阈值时，使用第一个阈值的人数，比例为1
        expected_user_groups = [25, 25]  # 50 * [0.5, 0.5]
        expected_diamond_groups = [100, 50]  # [100*1, 50*1]

        assert user_groups == expected_user_groups
        assert diamond_groups == expected_diamond_groups

    def test_get_user_and_diamond_groups_at_first_threshold(self):
        """测试总人数等于第一个阈值的情况"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        user_groups, diamond_groups = strategy.get_user_and_diamond_groups(50)

        expected_user_groups = [25, 25]
        expected_diamond_groups = [100, 50]

        assert user_groups == expected_user_groups
        assert diamond_groups == expected_diamond_groups

    def test_get_user_and_diamond_groups_above_first_threshold(self):
        """测试总人数高于第一个阈值的情况"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500},
            {"level": 2, "users": 100, "diamonds": 5000}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        user_groups, diamond_groups = strategy.get_user_and_diamond_groups(75)

        # 75/50 = 1.5 比例
        expected_user_groups = [37, 38]  # 75 * [0.5, 0.5]，最后一组调整
        expected_diamond_groups = [150, 75]  # [100*1.5, 50*1.5]

        assert user_groups == expected_user_groups
        assert diamond_groups == expected_diamond_groups

    def test_get_user_and_diamond_groups_multiple_thresholds(self):
        """测试多个阈值的情况"""
        group_ratios = [0.3, 0.4, 0.3]
        base_diamond_groups = [100, 50, 25]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500},
            {"level": 2, "users": 100, "diamonds": 5000},
            {"level": 3, "users": 200, "diamonds": 10000}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        user_groups, diamond_groups = strategy.get_user_and_diamond_groups(150)

        # 150/100 = 1.5 比例
        expected_user_groups = [45, 60, 45]  # 150 * [0.3, 0.4, 0.3]
        expected_diamond_groups = [150, 75, 37]  # [100*1.5, 50*1.5, 25*1.5]

        assert user_groups == expected_user_groups
        assert diamond_groups == expected_diamond_groups

    def test_get_all_distributions_basic(self):
        """测试基本的钻石分配功能"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)
        
        result = strategy.get_all_distributions(50)
        
        # 50人，每组25人，钻石分别为100和50
        expected = [100] * 25 + [50] * 25
        assert result == expected

    def test_get_all_distributions_with_ratio_adjustment(self):
        """测试比率调整的情况"""
        group_ratios = [0.3, 0.4, 0.3]
        base_diamond_groups = [100, 50, 25]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)
        
        result = strategy.get_all_distributions(50)
        
        # 50人，按比例分配：15, 20, 15
        expected = [100] * 15 + [50] * 20 + [25] * 15
        assert result == expected

    def test_get_distributions_by_some_rankings_basic(self):
        """测试获取部分排名的钻石分配"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        rankings = [0, 25, 49]
        result = strategy.get_distributions_by_some_rankings(total_users=50, rankings=rankings)

        expected = {0: 100, 25: 50, 49: 50}
        assert result == expected

    def test_get_distributions_by_some_rankings_empty_rankings(self):
        """测试空排名列表的情况"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        result = strategy.get_distributions_by_some_rankings(total_users=50, rankings=[])

        expected = {}
        assert result == expected

    def test_complex_scenario(self):
        """测试复杂场景：多组、多阈值"""
        group_ratios = [0.2, 0.3, 0.5]
        base_diamond_groups = [200, 100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500},
            {"level": 2, "users": 100, "diamonds": 5000},
            {"level": 3, "users": 200, "diamonds": 10000}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)
        total_users = 150

        # 测试150人，比例150/100=1.5
        result = strategy.get_all_distributions(total_users)

        # 150 * [0.2, 0.3, 0.5] = [30, 45, 75]
        # 钻石：[200*1.5, 100*1.5, 50*1.5] = [300, 150, 75]
        expected = [300] * 30 + [150] * 45 + [75] * 75
        assert result == expected

        # 测试部分排名
        partial_rankings = [0, 29, 30, 74, 75, 149]
        partial_result = strategy.get_distributions_by_some_rankings(total_users=total_users, rankings=partial_rankings)
        expected = {0: 300, 29: 300, 30: 150, 74: 150, 75: 75, 149: 75}
        assert partial_result == expected

    def test_edge_case_single_group(self):
        """测试边界情况：只有一个组"""
        group_ratios = [1.0]
        base_diamond_groups = [100]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        result = strategy.get_all_distributions(50)
        expected = [100] * 50
        assert result == expected

    def test_edge_case_zero_users(self):
        """测试边界情况：零用户"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [100, 50]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        result = strategy.get_all_distributions(0)
        expected = []
        assert result == expected

    def test_edge_case_zero_base_diamonds(self):
        """测试边界情况：零基础钻石"""
        group_ratios = [0.5, 0.5]
        base_diamond_groups = [0, 0]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        result = strategy.get_all_distributions(50)
        expected = [0] * 50
        assert result == expected

    def test_ratio_adjustment_mechanism(self):
        """测试比率调整机制"""
        group_ratios = [0.3, 0.3, 0.4]
        base_diamond_groups = [100, 50, 25]
        level_thresholds = [
            {"level": 1, "users": 50, "diamonds": 2500}
        ]
        strategy = LevelGroupStrategy(group_ratios, base_diamond_groups, level_thresholds)

        user_groups, diamond_groups = strategy.get_user_and_diamond_groups(50)

        # 验证最后一组被调整以确保总和正确
        assert sum(user_groups) == 50
        assert user_groups[0] == 15  # 50 * 0.3
        assert user_groups[1] == 15  # 50 * 0.3
        assert user_groups[2] == 20  # 50 - 15 - 15 = 20 (调整后)
