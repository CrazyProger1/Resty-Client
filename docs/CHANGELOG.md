# Rest-Client Changelog

## v0.0.2

- Added serializer many schemas support
- Added get_schema serializer method

## v0.0.3

- Refactored manager & httpx client
- Added more examples
- Added serializer tests
- Added URL injecting mechanism (allows to perform many-layer requests: `api/v1/users/123/product/321`).
  See [example](../examples/crud_many_layers)
- Added deserialize_many serializer method

## v0.0.4

- Manager fixes
