class Observer:
    def observer_update(self, pcb_number):
        pass
    
    
class DataLogger(Observer):
    def update(self, pcb_number):
        print(f"DataLogger: Total prices logged as {pcb_number}")


class Subject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, pcb_number):
        for observer in self._observers:
            print(f"notify_observers: Total prices {pcb_number}")
            observer.observer_update(pcb_number)

    def subject_update_data(self,evt):
        pass
 
# class ConcreteSubject(Subject):
#     def do_something(self,data):
#         self.notify_observers(data)  