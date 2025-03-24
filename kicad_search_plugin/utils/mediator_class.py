class Mediator:
    def __init__(self):
        self.subscribers = []

    def register(self, subscriber):
        if subscriber not in self.subscribers:
            print(f"sub:{subscriber}")
            self.subscribers.append(subscriber)
            print(f"add:{self.subscribers}")
            

    def notify(self, message):
        for subscriber in self.subscribers:
            if hasattr(subscriber, 'update_with_total_prices'):
                subscriber.update_with_total_prices(message)