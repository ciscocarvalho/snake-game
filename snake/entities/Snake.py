from ..config import Defaults
from .Node import Node

defaults = Defaults()


class Snake:
    def __init__(self, display, amount_of_nodes):
        self.display = display
        self.points = 0
        self._nodes = []
        self.add_node(defaults.snake_head_color)

        for _ in range(1, amount_of_nodes):
            self.add_node()

        self.set_direction(defaults.direction)

    def get_all_nodes(self):
        # Since copy() creates a shallow copy, this isn't a problem
        return self._nodes.copy()

    def get_node(self, index):
        nodes = self.get_all_nodes()
        if index < 0:
            index = len(nodes) + index
        if len(nodes) <= 0 or index not in range(len(nodes)):
            return None
        else:
            return nodes[index]

    def get_head(self):
        return self.get_node(0)

    def get_tail(self):
        return self.get_node(-1)

    def get_node_coords(self):
        node_coords = []
        nodes = self.get_all_nodes()
        nodes.reverse()

        for node in nodes:
            node_coords.append(node.coords)

        return node_coords

    def set_direction(self, direction):
        self.get_head().direction = direction

    def get_direction(self):
        return self.get_head().direction

    def move(self):
        nodes = self.get_all_nodes()
        head = self.get_head()
        tail = self.get_tail()

        for i, node in enumerate(nodes):
            if node == tail:
                node.old_position = node.coords

            if node == head:
                node.old_position = node.coords
                node.coords = node.get_new_coords_by_current_direction()
            else:
                node.old_position = node.coords
                next_idx = i - 1
                if next_idx in range(0, len(nodes) - 1):
                    next = nodes[next_idx]
                    node.coords = next.old_position

            if (
                head.coords is not False
                and node != head
                and node.get_rect().colliderect(head.get_rect())
            ):
                head.coords = False
                break

        return head.coords

    def update(self):
        nodes = self.get_all_nodes()
        for node in nodes:
            node.update()

    def add_node(self, *args):
        node = Node(self.display, *args)
        old_tail = self.get_tail()
        if old_tail is not None:
            node.coords = old_tail.old_position
        self._nodes.append(node)
