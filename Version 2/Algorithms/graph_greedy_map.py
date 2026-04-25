import heapq
import time

def heuristic(a, b, G):
    # straight-line distance using node coordinates
    ax, ay = G.nodes[a]["x"], G.nodes[a]["y"]
    bx, by = G.nodes[b]["x"], G.nodes[b]["y"]
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5


def reconstruct(parent, start, end):
    path = []
    cur = end

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()
    return path


def graph_greedy_bfs(start, end, G):
    start_time = time.time()

    pq = [(0, start)]
    visited = set()
    parent = {}
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
            if neighbor not in visited:
                parent[neighbor] = current
                priority = heuristic(neighbor, end, G)
                heapq.heappush(pq, (priority, neighbor))

    return None