from abc import ABC


class ReaderPublisher(ABC):
    _result = None
    _observers = []
    _config = None

    def __init__(self, config):
        self._config = config

    def attach(self, observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def get_result(self):
        return self._result
