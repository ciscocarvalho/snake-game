from ..config import Defaults
from .Node import Node

defaults = Defaults()


class Snake:
    def __init__(self, display, nodes_amount, coords=[0, 0]):
        self.display = display
        self.head_color = defaults.snake_head_color
        self.points = 0

        self.head = self.tail = None
        self.add_node(defaults.snake_head_color)

        for _ in range(1, nodes_amount):
            self.add_node()

        self.set_direction(defaults.direction)

    def get_node_coords(self):
        node_coords = []

        def add_to_list(node):
            nonlocal node_coords
            node_coords.append(node.coords)

        self.traverse_nodes_backward(add_to_list)
        return node_coords

    def set_direction(self, direction):
        self.head.direction = direction

    def get_direction(self):
        return self.head.direction

    def move(self):
        def move_node(node):
            node.move()

        self.traverse_nodes_backward(move_node)

        def check_collision(node):
            if (
                self.head.coords is not False
                and not node.is_head()
                and node.get_rect().colliderect(self.head.get_rect())
            ):
                self.head.coords = False

        self.traverse_nodes_forward(check_collision)
        return self.head.coords

    def update(self):
        def update_node(node):
            node.update()

        self.traverse_nodes_forward(update_node)

    def add_node(self, *args):
        new_tail = Node(self.display, *args)
        if self.head is None:
            self.head = new_tail
        else:
            old_tail = self.tail
            old_tail.next = new_tail
            new_tail.previous = old_tail
            new_tail.coords = old_tail.old_position
        self.tail = new_tail

    def traverse_nodes_forward(self, cb):
        current_node = self.head
        while True:
            if current_node is None:
                break
            cb(current_node)
            current_node = current_node.next

    def traverse_nodes_backward(self, cb):
        current_node = self.tail
        while True:
            if current_node is None:
                break
            cb(current_node)
            current_node = current_node.previous
