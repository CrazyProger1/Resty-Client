from functools import cache
from urllib.parse import urljoin, urlparse

from resty.enums import Endpoint
from resty.exceptions import URLBuildingError
from resty.managers.types import BaseURLBuilder, Endpoints


class URLBuilder(BaseURLBuilder):
    @classmethod
    def _get_endpoint_url(cls, endpoints: Endpoints, endpoint: Endpoint) -> str | None:
        url = endpoints.get(endpoint, endpoints.get(Endpoint.BASE, None))
        return url

    @classmethod
    def _inject_params(cls, url: str, **params) -> str:
        try:
            return url.format(**params)
        except KeyError as e:
            raise URLBuildingError(f"Missing '{e.args[0]}' in {url}")

    @classmethod
    @cache
    def _normalize_url(cls, url: str | None) -> str:
        if not url:
            return ""

        if not url.endswith("/"):
            return url + "/"
        return url

    @classmethod
    def build(
        cls, endpoints: Endpoints, endpoint: Endpoint, base_url: str = None, **kwargs
    ) -> str:

        endpoint_url = cls._get_endpoint_url(endpoints=endpoints, endpoint=endpoint)

        if endpoint_url:
            url = urljoin(cls._normalize_url(url=base_url), endpoint_url)
        else:
            url = base_url or ""

        return cls._inject_params(url=url, **kwargs)
