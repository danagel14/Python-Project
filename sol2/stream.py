import threading

class Stream:
    def __init__(self):
        self.lst = []
        self.action = None
        self.running = True
        self.cond = threading.Condition()
        self.thread = threading.Thread(target=self.run)
        self.children = []
        self.thread.start()

    def run(self):
        while self.running:
            with self.cond:
                while not self.lst and self.running:
                    self.cond.wait()
                if not self.running:
                    break
                item = self.lst.pop(0)
            if self.action:
                self.action(item)

    def add(self, item):
        with self.cond:
            self.lst.append(item)
            self.cond.notify()

    def forEach(self, func):
        self.action = func

    def apply(self, func):
        new_stream = Stream()

        def new_action(x):
            result = func(x)
            if isinstance(result, bool):
                if result:
                    new_stream.add(x)
            else:
                new_stream.add(result)

        self.action = new_action
        self.children.append(new_stream)
        return new_stream

    def stop(self):
        self.running = False
        with self.cond:
            self.cond.notify_all()
        self.thread.join()
        for child in self.children:
            child.stop()
