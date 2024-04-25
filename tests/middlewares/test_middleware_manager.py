import pytest

from resty.middlewares import (
    MiddlewareManager,
    BaseMiddleware,
    BaseResponseMiddleware,
    BaseRequestMiddleware,
)


@pytest.mark.parametrize(
    "base",
    [
        BaseMiddleware,
        BaseResponseMiddleware,
        BaseRequestMiddleware,
    ],
)
def test_add_middleware(base):
    manager = MiddlewareManager()

    class MyMiddleware(base):
        async def __call__(self, *args, **kwargs): ...

    manager.add_middleware(MyMiddleware())

    assert type(tuple(manager.middlewares)[0]) is MyMiddleware


@pytest.mark.parametrize(
    "base",
    [
        BaseMiddleware,
        BaseResponseMiddleware,
        BaseRequestMiddleware,
    ],
)
def test_remove_middleware(base):
    manager = MiddlewareManager()

    class MyMiddleware(base):
        async def __call__(self, *args, **kwargs): ...

    middleware = MyMiddleware()

    manager.add_middleware(middleware)

    manager.remove_middleware(middleware)

    assert len(tuple(manager.middlewares)) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "base",
    [
        BaseMiddleware,
        BaseResponseMiddleware,
        BaseRequestMiddleware,
    ],
)
async def test_with_middleware(base):
    manager = MiddlewareManager()

    class MyMiddleware(base):
        async def __call__(self, *args, **kwargs):
            assert args[0] == "test"

    with manager.middleware(MyMiddleware()):
        assert len(tuple(manager.middlewares)) == 1

        await manager("test")

    assert len(tuple(manager.middlewares)) == 0


def test_invalid_middleware():
    with pytest.raises(TypeError):
        manager = MiddlewareManager()
        manager.add_middleware("test")
