import pytest

from resty.exceptions import URLBuildingError
from resty.managers import URLBuilder
from resty.enums import Endpoint


@pytest.mark.parametrize(
    "endpoints, endpoint, base, kwargs, expected",
    [
        (
            {
                Endpoint.CREATE: "users/",
            },
            Endpoint.CREATE,
            "base/",
            {},
            "base/users/",
        ),
        (
            {
                Endpoint.BASE: "users/",
            },
            Endpoint.CREATE,
            "base/",
            {},
            "base/users/",
        ),
        (
            {
                Endpoint.BASE: "users/",
            },
            Endpoint.CREATE,
            "base",
            {},
            "base/users/",
        ),
        (
            {
                Endpoint.BASE: "users/",
            },
            Endpoint.CREATE,
            None,
            {},
            "users/",
        ),
        (
            {
                Endpoint.BASE: "users/{pk}",
            },
            Endpoint.CREATE,
            None,
            {"pk": 123},
            "users/123",
        ),
        ({}, Endpoint.CREATE, "base/{pk}", {"pk": 123}, "base/123"),
        ({}, Endpoint.CREATE, None, {"pk": 123}, ""),
    ],
)
def test_build(endpoints, endpoint, base, kwargs, expected):
    builder = URLBuilder()

    assert (
        builder.build(endpoints=endpoints, endpoint=endpoint, base_url=base, **kwargs)
        == expected
    )


def test_build_missing_kwargs():
    with pytest.raises(URLBuildingError):
        builder = URLBuilder()
        builder.build({}, Endpoint.CREATE, "users/{pk}")
