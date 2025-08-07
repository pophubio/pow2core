import pytest

from pow2core.distribute_strategies.fixed_group import FixedGroupStrategy


class TestFixedGroupStrategy:
    def test_init_with_valid_parameters(self):
        """测试使用有效参数初始化"""
        user_groups = [10, 20, 30]
        diamond_groups = [100, 50, 25]

        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        assert strategy.user_groups == [10, 20, 30]
        assert strategy.diamond_groups == [100, 50, 25]

    def test_init_with_mismatched_lengths(self):
        """测试人数组和钻石组长度不一致的情况"""
        user_groups = [10, 20]
        diamond_groups = [100, 50, 25]

        with pytest.raises(ValueError, match="预设人数组和钻石组长度不一致"):
            FixedGroupStrategy(user_groups, diamond_groups)

    def test_get_all_distributions_basic(self):
        """测试基本的钻石分配功能"""
        user_groups = [3, 2, 1]
        diamond_groups = [100, 50, 25]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        result = strategy.get_all_distributions(6)

        expected = [100, 100, 100, 50, 50, 25]
        assert result == expected

    def test_get_all_distributions_with_fewer_users(self):
        """测试总人数少于预设人数的情况"""
        user_groups = [5, 3, 2]
        diamond_groups = [100, 50, 25]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        result = strategy.get_all_distributions(7)

        expected = [100, 100, 100, 100, 100, 50, 50]
        assert result == expected

    def test_get_all_distributions_with_more_users(self):
        """测试总人数多于预设人数的情况"""
        user_groups = [2, 1]
        diamond_groups = [100, 50]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        with pytest.raises(ValueError, match="总人数5超过预设人数3"):
            strategy.get_all_distributions(5)

    def test_get_all_distributions_strict_mode_success(self):
        """测试严格模式下人数匹配的情况"""
        user_groups = [3, 2, 1]
        diamond_groups = [100, 50, 25]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        result = strategy.get_all_distributions(6, strict=True)

        expected = [100, 100, 100, 50, 50, 25]
        assert result == expected

    def test_get_all_distributions_strict_mode_failure(self):
        """测试严格模式下人数不匹配的情况"""
        user_groups = [3, 2, 1]
        diamond_groups = [100, 50, 25]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        with pytest.raises(ValueError, match="预设人数和总人数不一致"):
            strategy.get_all_distributions(5, strict=True)

    def test_get_all_distributions_empty_groups(self):
        """测试空组的情况"""
        user_groups = []
        diamond_groups = []

        with pytest.raises(ValueError, match="预设人数组和钻石组不能为空"):
            FixedGroupStrategy(user_groups, diamond_groups)

    def test_get_all_distributions_zero_users(self):
        """测试零用户的情况"""
        user_groups = [3, 2, 1]
        diamond_groups = [100, 50, 25]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        result = strategy.get_all_distributions(0)

        expected = []
        assert result == expected

    def test_get_distributions_by_some_rankings_basic(self):
        """测试获取部分排名的钻石分配"""
        user_groups = [3, 2, 1]
        diamond_groups = [100, 50, 25]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        rankings = [0, 2, 4, 5]
        result = strategy.get_distributions_by_some_rankings(rankings)

        expected = {0: 100, 2: 100, 4: 50, 5: 25}
        assert result == expected

    def test_get_distributions_by_some_rankings_all_rankings(self):
        """测试获取所有排名的钻石分配"""
        user_groups = [2, 1]
        diamond_groups = [100, 50]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        rankings = [0, 1, 2]
        result = strategy.get_distributions_by_some_rankings(rankings)

        expected = {0: 100, 1: 100, 2: 50}
        assert result == expected

    def test_get_distributions_by_some_rankings_empty_rankings(self):
        """测试空排名列表的情况"""
        user_groups = [3, 2, 1]
        diamond_groups = [100, 50, 25]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        result = strategy.get_distributions_by_some_rankings([])

        expected = {}
        assert result == expected

    def test_get_distributions_by_some_rankings_duplicate_rankings(self):
        """测试重复排名的情况"""
        user_groups = [2, 1]
        diamond_groups = [100, 50]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        rankings = [0, 0, 1, 2]
        result = strategy.get_distributions_by_some_rankings(rankings)

        expected = {0: 100, 1: 100, 2: 50}
        assert result == expected

    def test_get_distributions_by_some_rankings_out_of_range(self):
        """测试超出预设人数的排名"""
        user_groups = [2, 1]
        diamond_groups = [100, 50]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        rankings = [0, 2, 4]
        with pytest.raises(ValueError, match="无效排名:4超过预设最大人数3"):
            strategy.get_distributions_by_some_rankings(rankings)

    def test_get_distributions_by_some_rankings_exceed_preset_users(self):
        """测试排名数量超过预设人数的情况"""
        user_groups = [2, 1]
        diamond_groups = [100, 50]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        rankings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        with pytest.raises(ValueError, match="排行榜长度超过预设人数"):
            strategy.get_distributions_by_some_rankings(rankings)

    def test_get_distributions_by_some_rankings_negative_rankings(self):
        """测试负数排名的情况"""
        user_groups = [2, 1]
        diamond_groups = [100, 50]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        rankings = [-1, 0, 1]
        with pytest.raises(ValueError, match="无效排名:-1,排名不能为负数"):
            strategy.get_distributions_by_some_rankings(rankings)

    def test_complex_scenario(self):
        """测试复杂场景：多组、不同钻石数量"""
        user_groups = [5, 10, 15, 8, 2]
        diamond_groups = [1000, 500, 200, 100, 50]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        # 测试总分配
        total_result = strategy.get_all_distributions(40)
        assert len(total_result) == 40
        assert total_result[0:5] == [1000] * 5
        assert total_result[5:15] == [500] * 10
        assert total_result[15:30] == [200] * 15
        assert total_result[30:38] == [100] * 8
        assert total_result[38:40] == [50] * 2

        # 测试部分排名
        partial_rankings = [0, 7, 20, 35, 39]
        partial_result = strategy.get_distributions_by_some_rankings(partial_rankings)
        expected = {0: 1000, 7: 500, 20: 200, 35: 100, 39: 50}
        assert partial_result == expected

    def test_edge_case_single_group(self):
        """测试边界情况：只有一个组"""
        user_groups = [10]
        diamond_groups = [100]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        result = strategy.get_all_distributions(10)
        expected = [100] * 10
        assert result == expected

        partial_result = strategy.get_distributions_by_some_rankings([0, 5, 9])
        expected = {0: 100, 5: 100, 9: 100}
        assert partial_result == expected

    def test_edge_case_zero_diamonds(self):
        """测试边界情况：零钻石"""
        user_groups = [3, 2]
        diamond_groups = [0, 0]
        strategy = FixedGroupStrategy(user_groups, diamond_groups)

        result = strategy.get_all_distributions(5)
        expected = [0, 0, 0, 0, 0]
        assert result == expected
