import inspect

import hydra_zen as hz


class MyClass:
    def __init__(self, param=5) -> None:
        self.param = param

    def __call__(self, a):
        pass


def myfunc(a, x=MyClass(6), nested=MyClass(12)):
    print("works")


if __name__ == "__main__":
    params = {}
    for param_name, param in inspect.signature(myfunc).parameters.items():
        if (
            # param.kind == inspect.Parameter.KEYWORD_ONLY
            param.default != inspect.Parameter.empty
            and inspect.isclass(param.default.__class__)
            and hasattr(param.default, "__init__")
        ):
            inner_params = {}
            print(inspect.signature(param.default.__init__).parameters.keys())
            for inner_param_name in list(
                inspect.signature(param.default.__init__).parameters.keys()
            ):
                print(inner_param_name)
                inner_params[inner_param_name] = getattr(
                    param.default, inner_param_name
                )
            params[param_name] = hz.builds(
                param.default.__class__,
                **inner_params,
                populate_full_signature=True,
                zen_partial=True,
            )
    res = hz.builds(myfunc, **params, populate_full_signature=True, zen_partial=True)
    new_func = hz.instantiate(res)
    print(f"{hz.to_yaml(res)}")
    new_func("this")
