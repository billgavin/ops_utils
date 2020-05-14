import fire

from functools import update_wrapper
from types import MappingProxyType
from typing import Hashable, Callable, Union

def specificdispatch(key: Union[int, str] = 0) -> Callable:

    def decorate(func: Callable) -> Callable:

        registry = {}

        def dispatch(key: Hashable) -> Callable:

            try:
                impl = registry[key]
            except KeyError:
                impl = registry[object]
            return impl

        def register(key: Hashable, func: Callable=None) -> Callable:

            if func is None:
                return lambda f: register(key, f)

            registry[key] = func
            return func

        def wrapper(*args, **kw):
            if isinstance(key, int):
                return dispatch(args[key])(*args, **kw)
            elif isinstance(key, str):
                return dispatch(kw[key])(*args, **kw)
            else:
                raise KeyError('The key must be int or str')

        registry[object] = func
        wrapper.register = register
        wrapper.dispatch = dispatch
        wrapper.registry = MappingProxyType(registry)
        update_wrapper(wrapper, func)

        return wrapper
    return decorate


class Test:
    @specificdispatch(key='message')
    def test_dispatch(self, message, *args, **kw):
        print(f'default: {message} args: {args} kw: {kw}')

    @test_dispatch.register('test')
    def _(self, message, *args, **kw):
        print(f'test: {message} args: {args} kw{kw}')

if __name__ == '__main__':
    fire.Fire(Test)
