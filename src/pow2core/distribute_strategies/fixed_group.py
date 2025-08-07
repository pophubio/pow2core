class FixedGroupStrategy:
    """
    按固定人数组和钻石组分配钻石
    """
    def __init__(self, user_groups: list[int], diamond_groups: list[int]) -> None:
        """
        Args:
            user_groups: 每组的人数
            diamond_groups: 每组中每人对应的钻石数

        Raises:
            ValueError: 预设人数组和钻石组长度不一致
            ValueError: 预设人数组和钻石组不能为空
        """
        if len(user_groups) != len(diamond_groups):
            raise ValueError("预设人数组和钻石组长度不一致")

        if not user_groups or not diamond_groups:
            raise ValueError("预设人数组和钻石组不能为空")

        self.user_groups = user_groups
        self.diamond_groups = diamond_groups

    def get_all_distributions(
        self,
        total_users: int,
        strict: bool = False,
    ) -> list[int]:
        """
        按照排名给所有用户分配钻石
        找到用户所在组,然后分配钻石

        Args:
            total_users: 总人数
            strict: 是否严格模式, 严格模式下预设人数和总人数必须一致

        Returns:
            list[int]: 钻石数量列表, 索引是排名, 从0开始
        """
        max_total_user = sum(self.user_groups)
        if total_users > max_total_user:
            raise ValueError(f"总人数{total_users}超过预设人数{max_total_user}")

        if strict and max_total_user != total_users:
                raise ValueError("预设人数和总人数不一致")

        distributions = [0] * total_users
        start_ranking = 0

        for group_idx, user_group_size in enumerate(self.user_groups):
            end_ranking = min(start_ranking + user_group_size, total_users)
            for i in range(start_ranking, end_ranking):
                distributions[i] = self.diamond_groups[group_idx]
            start_ranking = end_ranking

            if start_ranking >= total_users:
                break

        return distributions

    def get_distributions_by_some_rankings(
        self,
        rankings: list[int],
    ) -> dict[int, int]:
        """
        获取一部分排名的钻石分配

        Args:
            rankings: 排行榜,元素是排名, 排名是从0开始的

        Returns:
            dict[int, int]: 排名到钻石数量的映射
        """
        rankings = set(rankings)  # 去重
        max_total_user = sum(self.user_groups)
        if len(rankings) > max_total_user:
            raise ValueError("排行榜长度超过预设人数")

        result = {}
        start_ranking = 0

        for group_idx, user_group_size in enumerate(self.user_groups):
            end_ranking = start_ranking + user_group_size
            diamond = self.diamond_groups[group_idx]

            for ranking in rankings:
                if ranking < 0:
                    raise ValueError(f"无效排名:{ranking},排名不能为负数")

                if ranking >= max_total_user:
                    raise ValueError(f"无效排名:{ranking}超过预设最大人数{max_total_user}")

                if start_ranking <= ranking < end_ranking:
                    result[ranking] = diamond

            start_ranking = end_ranking

        return result
