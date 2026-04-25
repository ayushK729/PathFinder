import time
import heapq
from Algorithms.grid_utility import heuristic


def graph_a_star_map(start, end, G):
    start_time = time.time()

    pq = [(0, start)]
    g_cost = {start: 0}
    parent = {}
    visited = set()
    visited_order = []

    while pq:

        _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == end:
            return {
                "visited_order": visited_order,
                "path": reconstruct(parent, start, end),
                "time_taken": time.time() - start_time
            }

        for neighbor in G.neighbors(current):

            edge = G.get_edge_data(current, neighbor)
            weight = list(edge.values())[0].get("length", 1)

            new_g = g_cost[current] + weight

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                parent[neighbor] = current

                f = new_g + heuristic(neighbor, end, G)
                heapq.heappush(pq, (f, neighbor))

    return None


def reconstruct(parent, start, end):
    path = []
    cur = end

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()
    return path