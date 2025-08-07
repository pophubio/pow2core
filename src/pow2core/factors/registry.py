from pydantic import BaseModel, Field


class FactorImplementation(BaseModel):
    """因子实现信息"""
    name: str = Field(description="因子名称")
    algorithm: str | None = Field(description="算法")
    method: str | None = Field(description="实现方法, 比如归一化的linear/log")
    implementation_class: type = Field(description="实现类")
    config_schema: type | None = Field(description="配置schema")


class FactorRegistry:
    """因子注册中心"""
    _implementations: dict[str, list[FactorImplementation]] = {}  # noqa: RUF012

    @classmethod
    def register(
        cls,
        name: str,
        algorithm: str | None = None,
        method: str | None = None,
        config_schema: type | None = None,
    ):
        """装饰器: 注册因子实现"""
        def decorator(implementation_class: type):

            impl = FactorImplementation(
                name=name,
                algorithm=algorithm,
                method=method,
                implementation_class=implementation_class,
                config_schema=config_schema
            )

            if name not in cls._implementations:
                cls._implementations[name] = []
            cls._implementations[name].append(impl)

            return implementation_class
        return decorator

    @classmethod
    def get_implementation(cls, name: str, algorithm: str, method: str | None = None) -> FactorImplementation:
        """根据名称、算法和方法获取因子实现"""
        if name not in cls._implementations:
            raise ValueError(f"Factor {name} not found")

        for impl in cls._implementations[name]:
            # 算法必须匹配,方法可选匹配
            if impl.algorithm == algorithm and (impl.method is None or impl.method == method):
                return impl

        raise ValueError(f"No implementation found for {name} with algorithm {algorithm} and method {method}")

    @classmethod
    def get_all_implementations(cls, name: str) -> list[FactorImplementation]:
        """获取指定名称的所有因子实现"""
        return cls._implementations.get(name, [])

    @classmethod
    def list_all_factors(cls) -> dict[str, list[FactorImplementation]]:
        """获取所有注册的因子实现"""
        return cls._implementations.copy()
