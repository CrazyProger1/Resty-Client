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

- Manager important fixes!!!!

## v0.0.5

- Improved test coverage to 100%
- Improved architecture
- Added examples

## v0.0.6

- Changed Manager API:

Now instantiating manager is required.

You can pass the REST Client into the constructor:

```python
manager = UserManager(client=client)

response = await manager.read(
    response_type=UserReadSchema,
)
```

or specify the client explicitly during calling:

```python
manager = UserManager()

response = await manager.read(
    response_type=UserReadSchema,
    client=client,
)
```

- Added Django pagination middlewares:

  - `LimitOffsetPaginationMiddleware`
  - `PagePaginationMiddleware`


