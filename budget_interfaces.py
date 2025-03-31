# budget_interfaces.py
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

class IAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, transactions):
        pass

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
