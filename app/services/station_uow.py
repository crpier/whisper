from abc import ABC, abstractmethod

from app.adapters.repository import AbstractStationRepository


class AbstractStationUnitOfWork(ABC):
    stations: AbstractStationRepository

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

class ThreadStationUnitOfWork(AbstractStationUnitOfWork):
    pass
