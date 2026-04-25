import pygame
import osmnx as ox
import time

from map_loader import load_map
from Algorithms.graph_bfs_map import graph_bfs_map
from Algorithms.graph_a_star import graph_a_star_map
from Algorithms.graph_dfs import graph_dfs_map
from Algorithms.graph_greedy_map import graph_greedy_bfs
from Algorithms.graph_djikstra_map import graph_dijkstra_map
from Algorithms.utils import get_nearest_node


# ---------------- MAP ----------------
PLACE = "Delhi, India"
G = load_map(PLACE)

G = ox.project_graph(G)
nodes, edges = ox.graph_to_gdfs(G)

# ---------------- SCREEN ----------------
pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Map Visualizer")

font = pygame.font.SysFont(None, 26)

# ---------------- COORD SYSTEM ----------------
xs = nodes["x"]
ys = nodes["y"]

min_x, max_x = xs.min(), xs.max()
min_y, max_y = ys.min(), ys.max()


def project(x, y):
    px = (x - min_x) / (max_x - min_x) * WIDTH
    py = (y - min_y) / (max_y - min_y) * HEIGHT
    return int(px), int(py)


# ---------------- STATE ----------------
start = None
end = None
visited_draw = []
path_draw = []

exec_time = 0
path_distance = 0

current_algorithm = "BFS"

ALGORITHMS = {
    "BFS": graph_bfs_map,
    "ASTAR": graph_a_star_map,
    "DFS": graph_dfs_map,
    "GREEDY": graph_greedy_bfs,
    "DIJKSTRA":graph_dijkstra_map
}

# ---------------- LOOP ----------------
running = True

while running:

    screen.fill((0, 0, 0))

    # ---------------- SIMPLE MAP EDGES (RESTORED) ----------------
    for u, v, data in G.edges(data=True):
        x1, y1 = nodes.loc[u, "x"], nodes.loc[u, "y"]
        x2, y2 = nodes.loc[v, "x"], nodes.loc[v, "y"]

        pygame.draw.line(
            screen,
            (90, 90, 90),
            project(x1, y1),
            project(x2, y2),
            1
        )

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            x = min_x + (mx / WIDTH) * (max_x - min_x)
            y = min_y + (my / HEIGHT) * (max_y - min_y)

            node = get_nearest_node(G, x, y)

            if not start:
                start = node
            elif not end:
                end = node

        elif event.type == pygame.KEYDOWN:

            # RESET
            if event.key == pygame.K_r:
                start = None
                end = None
                visited_draw = []
                path_draw = []
                exec_time = 0
                path_distance = 0

            # SWITCH ALGO
            elif event.key == pygame.K_1:
                current_algorithm = "BFS"
            elif event.key == pygame.K_2:
                current_algorithm = "ASTAR"
            elif event.key == pygame.K_3:
                current_algorithm = "DFS"
            elif event.key == pygame.K_4:
                current_algorithm = "GREEDY"
            elif event.key == pygame.K_5:
                current_algorithm = "DIJKSTRA"

            # RUN
            elif event.key == pygame.K_SPACE and start and end:

                algo_func = ALGORITHMS[current_algorithm]

                t0 = time.time()
                result = algo_func(start, end, G)
                exec_time = time.time() - t0

                if result:

                    visited_draw = []
                    path_draw = []

                    for n in result["visited_order"]:
                        visited_draw.append(n)
                        x, y = nodes.loc[n, "x"], nodes.loc[n, "y"]
                        pygame.draw.circle(screen, (0, 150, 255), project(x, y), 2)
                        pygame.display.update()
                        pygame.time.delay(1)

                    path_draw = result["path"]

                    # distance
                    path_distance = 0
                    for i in range(len(path_draw) - 1):
                        u = path_draw[i]
                        v = path_draw[i + 1]
                        edge_data = G.get_edge_data(u, v)
                        if edge_data:
                            path_distance += list(edge_data.values())[0].get("length", 0)

    # ---------------- PATH ----------------
    for n in path_draw:
        x, y = nodes.loc[n, "x"], nodes.loc[n, "y"]
        pygame.draw.circle(screen, (255, 255, 0), project(x, y), 3)

    # ---------------- START / END ----------------
    if start:
        x, y = nodes.loc[start, "x"], nodes.loc[start, "y"]
        pygame.draw.circle(screen, (0, 255, 0), project(x, y), 6)

    if end:
        x, y = nodes.loc[end, "x"], nodes.loc[end, "y"]
        pygame.draw.circle(screen, (255, 0, 0), project(x, y), 6)

    # ---------------- UI ----------------
    screen.blit(font.render(f"Algorithm: {current_algorithm}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Time: {exec_time:.4f}s", True, (255, 255, 255)), (10, 35))
    screen.blit(font.render(f"Distance: {path_distance/1000:.2f} km", True, (255, 255, 255)), (10, 60))

    pygame.display.update()

pygame.quit()