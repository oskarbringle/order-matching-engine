import random
from .order import OrderType

class SkipListNode:
    def __init__(self, order, level):
        self.order = order
        self.forward = [None] * (level + 1)

class SkipList:
    MAX_LEVEL = 4

    def __init__(self, ascending=True):
        self.head = SkipListNode(None, self.MAX_LEVEL)
        self.level = 0
        self.ascending = ascending

    def random_level(self):
        lvl = 0
        while random.random() < 0.5 and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, order):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.head

        # Use ordering based on the ascending flag.
        for i in range(self.level, -1, -1):
            while current.forward[i]:
                if self.ascending:
                    if current.forward[i].order.price < order.price:
                        current = current.forward[i]
                    else:
                        break
                else:
                    if current.forward[i].order.price > order.price:
                        current = current.forward[i]
                    else:
                        break
            update[i] = current

        new_level = self.random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.head
            self.level = new_level

        new_node = SkipListNode(order, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def remove(self, price):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.head
        for i in range(self.level, -1, -1):
            while current.forward[i]:
                if self.ascending:
                    if current.forward[i].order.price < price:
                        current = current.forward[i]
                    else:
                        break
                else:
                    if current.forward[i].order.price > price:
                        current = current.forward[i]
                    else:
                        break
            update[i] = current

        target = current.forward[0]
        if target and target.order.price == price:
            for i in range(self.level + 1):
                if update[i].forward[i] != target:
                    break
                update[i].forward[i] = target.forward[i]

            while self.level > 0 and self.head.forward[self.level] is None:
                self.level -= 1

    def get_best_bid(self):
        # For buy orders, the list is descending, so the best bid is the first element.
        if not self.ascending:
            return self.head.forward[0].order if self.head.forward[0] else None
        # Otherwise (if ascending) traverse to the end.
        current = self.head
        while current.forward[0]:
            current = current.forward[0]
        return current.order if current != self.head else None

    def get_best_ask(self):
        # For sell orders, the list is ascending, so the best ask is the first element.
        if self.ascending:
            return self.head.forward[0].order if self.head.forward[0] else None
        # Otherwise (if descending) traverse to the end.
        current = self.head
        while current.forward[0]:
            current = current.forward[0]
        return current.order if current != self.head else None

    def to_list(self):
        result = []
        current = self.head.forward[0]
        while current:
            result.append(current.order)
            current = current.forward[0]
        return result
