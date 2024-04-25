from abc import ABC, abstractmethod


class BaseRESTClient(ABC):

    @abstractmethod
    async def request(self): ...
