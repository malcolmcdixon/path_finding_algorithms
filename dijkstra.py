from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


class Node:
    def __init__(self, name):
        self.name: str = name
        self._connections: list[Connection] = []
        self.distance: float = float("inf")
        self._via: Optional[Node] = None

    @property
    def connections(self) -> list[Connection]:
        return self._connections

    @property
    def via(self) -> Optional[Node]:
        return self._via

    @via.setter
    def via(self, node: Node) -> None:
        if self == node:
            raise ValueError("Cannot set via to self")
        self._via = node

    def __eq__(self, other: Node) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def add_connection(self, connection: Connection) -> None:
        # avoid connection to self
        if self != connection.connected_to:
            self._connections.append(connection)


@dataclass
class Connection:
    connected_to: Node
    distance: float


def get_node_by_name(nodes: list[Node], name: str) -> Optional[Node]:
    for n in nodes:
        if n.name == name:
            return n
    return None


def import_map(file: str) -> list[Node]:
    nodes = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            start, end, distance = line.rstrip().split(",")

            start_node = get_node_by_name(nodes, start)
            if start_node is None:
                start_node = Node(start)
                nodes.append(start_node)

            end_node = get_node_by_name(nodes, end)
            if end_node is None:
                end_node = Node(end)
                nodes.append(end_node)

            distance = float(distance)
            conn_s_e = Connection(end_node, distance)
            conn_e_s = Connection(start_node, distance)
            start_node.add_connection(conn_s_e)
            end_node.add_connection(conn_e_s)

    return nodes


def find_best_route(nodes: list[Node], start: str, end: str) -> Optional[list[Node]]:
    completed: list[Node] = []
    start_node = get_node_by_name(nodes, start)
    if start_node is None:
        return None
    start_node.distance = 0
    end_node = get_node_by_name(nodes, end)
    if end_node is None:
        return None

    while True:
        # sort nodes by distance, shortest at end, pop() much quicker at end of array
        nodes.sort(reverse=True, key=lambda node: node.distance)

        node = nodes.pop()

        # reached end node, must be shortest route
        if node == end_node:
            completed.append(node)
            break

        for connection in node.connections:
            # if node already visited process next connection
            if connection.connected_to not in nodes:
                continue

            # get connected to's node
            ct_node = connection.connected_to
            # update distance and via
            distance = node.distance + connection.distance
            if distance < ct_node.distance:
                ct_node.distance = distance
                ct_node.via = node

        completed.append(node)

    route = []
    node = end_node
    while node:
        route.append(node)
        node = node.via

    route.sort(key=lambda node: node.distance)

    return route


def main():
    nodes = import_map("map_input.txt")

    route = find_best_route(nodes, "S", "E")

    if route:
        for node in route:
            print(node.name, node.distance)
    else:
        print("Invalid start and / or end nodes")


if __name__ == "__main__":
    main()
