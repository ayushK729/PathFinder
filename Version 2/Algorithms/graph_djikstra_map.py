import heapq
import time


def reconstruct(parent, start, end):
    path = []
    cur = end

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()
    return path


def graph_dijkstra_map(start, end, G):
    start_time = time.time()

    pq = [(0, start)]
    dist = {start: 0}
    parent = {}
    visited = set()
    visited_order = []

    while pq:

        cost, current = heapq.heappop(pq)

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
            weight = list(edge.values())[0].get("length", 1) if edge else 1

            new_cost = cost + weight

            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return None