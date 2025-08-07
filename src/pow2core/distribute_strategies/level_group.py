from .fixed_group import FixedGroupStrategy


class LevelGroupStrategy:
    """
    按等级组分配钻石
    1. 分级策略: 不同等级有不同的钻石总量和人数阈值
    2. 组分配机制: 每组内基础钻石数
    3. 最终分配逻辑: 按等级和人数比例计算每人获得的钻石
    """
    def __init__(
        self,
        group_ratios: list[float],
        base_diamond_groups: list[int],
        level_thresholds: list[dict[str, int]],
    ) -> None:
        """
        Args:
            group_ratios: 每组人数占总人数的百分比
            base_diamond_groups: 每组中每人对应的钻石数的基础值
            level_thresholds: 每个等级的阈值, {level: 1, users: 50, diamonds: 2500}
        """
        if sum(group_ratios) != 1:
            raise ValueError("每组人数占总人数的百分比之和必须为1")

        self.group_ratios = group_ratios
        self.base_diamond_groups = base_diamond_groups
        self.level_thresholds = sorted(level_thresholds, key=lambda x: x["level"], reverse=True)

    def get_all_distributions(
        self,
        total_users: int,
    ) -> list[int]:
        """
        获取所有用户的钻石分配

        Args:
            total_users: 总人数

        Returns:
            list[int]: 钻石数量列表, 索引是排名, 从0开始
        """
        user_groups, diamond_groups = self.get_user_and_diamond_groups(total_users=total_users)

        return FixedGroupStrategy(
            user_groups=user_groups,
            diamond_groups=diamond_groups,
        ).get_all_distributions(total_users=total_users)

    def get_distributions_by_some_rankings(
        self,
        total_users: int,
        rankings: list[int],
    ) -> dict[int, int]:
        """
        获取一部分排名的钻石分配

        Args:
            total_users: 总人数
            rankings: 排行榜, 元素是排名, 排名是从0开始的

        Returns:
            dict[int, int]: 排名到钻石数量的映射
        """
        user_groups, diamond_groups = self.get_user_and_diamond_groups(total_users=total_users)
        return FixedGroupStrategy(
            user_groups=user_groups,
            diamond_groups=diamond_groups,
        ).get_distributions_by_some_rankings(rankings=rankings)

    def get_user_and_diamond_groups(self, total_users: int) -> tuple[list[int], list[int]]:
        """
        获取每组人数和每组中每人对应的钻石数

        Args:
            total_users: 总人数

        Returns:
            tuple[list[int], list[int]]: 每组人数和每组中每人对应的钻石数
        """
        first_level_threshold = self.level_thresholds[-1]
        if total_users < first_level_threshold["users"]:
            total_users = first_level_threshold["users"]
            ratio = 1
        else:
            for level_threshold in self.level_thresholds:
                ratio = total_users / level_threshold["users"]
                if total_users > level_threshold["users"]:
                    break

        user_groups = [int(total_users * i) for i in self.group_ratios]
        user_groups[-1] = total_users - sum(user_groups[:-1])
        diamond_groups = [int(i * ratio) for i in self.base_diamond_groups]
        return user_groups, diamond_groups
