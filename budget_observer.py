# budget_observer.py
from budget_interfaces import Observer

class ConsoleObserver(Observer):
    def update(self, message):
        print(">> [Observer] Notification:", message)
