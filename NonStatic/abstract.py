class Inventory(object):

    def __init__(self, items=[]):
        self.items = []

        if len(items) > 0:
            for i in items:
                self.items.append(i)

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        for i in self.items:
            if i.name == item.name:
                self.items.remove(item)
