from collections import defaultdict, deque
import heapq

class AirportGraph:
    def __init__(self):
        self.graph = defaultdict(list)  # adjacency list: airport -> list of (neighbor, distance)

    def add_route(self, source, destination, distance=1):
        self.graph[source].append((destination, distance))
        self.graph[destination].append((source, distance))  # remove if routes are one-way

    def bfs(self, start, target):
        visited = set()
        queue = deque([start])
        while queue:
            airport = queue.popleft()
            if airport == target:
                return True
            for neighbor, _ in self.graph[airport]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False

    def dijkstra(self, start, target):
        heap = [(0, start)]
        distances = {airport: float('inf') for airport in self.graph}
        distances[start] = 0
        while heap:
            current_distance, airport = heapq.heappop(heap)
            if airport == target:
                return current_distance
            for neighbor, weight in self.graph[airport]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))
        return float('inf')  # target unreachable
