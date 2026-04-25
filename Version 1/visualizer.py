import pygame
import sys
from Algorithms.bfs import bfs
from Algorithms.a_star import astar
from Algorithms.dijkstra import dijkstra
from Algorithms.dfs import dfs

# ---------------- ALGORITHMS ----------------
ALGORITHMS = {
    "BFS": bfs,
    "ASTAR": astar,
    "DIJKSTRA": dijkstra,
    "DFS": dfs
}

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 900, 600
ROWS, COLS = 20, 20

# Panels
panel_count = 1
panel_algorithms = ["BFS", "ASTAR", "DIJKSTRA"]

# State per panel
panel_visited = [[] for _ in range(3)]
panel_path = [[] for _ in range(3)]
panel_metrics = [None for _ in range(3)]

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,150,255)
YELLOW = (255,255,0)
DARK = (50,50,50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Comparison Mode")

font = pygame.font.SysFont(None, 24)

# ---------------- DRAW ----------------
def draw_all_panels(start, end, walls):
    screen.fill(BLACK)

    panel_width = WIDTH // panel_count
    cell_size = panel_width // COLS

    for i in range(panel_count):
        offset_x = i * panel_width

        visited = panel_visited[i]
        path = panel_path[i]

        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(
                    offset_x + col * cell_size,
                    row * cell_size,
                    cell_size,
                    cell_size
                )

                color = WHITE

                if (row, col) == start:
                    color = GREEN
                elif (row, col) == end:
                    color = RED
                elif (row, col) in walls:
                    color = DARK
                elif (row, col) in path:
                    color = YELLOW
                elif (row, col) in visited:
                    color = BLUE

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GREY, rect, 1)

        # Algorithm label
        screen.blit(font.render(panel_algorithms[i], True, BLACK), (offset_x + 10, 10))

        # Metrics
        if panel_metrics[i]:
            m = panel_metrics[i]
            screen.blit(font.render(f"T: {m['time']:.4f}", True, BLACK), (offset_x + 10, 40))
            screen.blit(font.render(f"N: {m['nodes']}", True, BLACK), (offset_x + 10, 60))
            screen.blit(font.render(f"P: {m['path']}", True, BLACK), (offset_x + 10, 80))

    # Separator lines
    for i in range(1, panel_count):
        x = i * panel_width
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), 3)

    pygame.display.update()


# ---------------- MAIN ----------------
def main():
    global panel_count

    start = None
    end = None
    walls = set()

    running = True

    while running:
        draw_all_panels(start, end, walls)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # ---------------- MOUSE ----------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                panel_width = WIDTH // panel_count
                cell_size = panel_width // COLS

                row = pos[1] // cell_size
                col = (pos[0] % panel_width) // cell_size

                if not start:
                    start = (row, col)
                elif not end:
                    end = (row, col)
                else:
                    walls.add((row, col))

            # ---------------- KEYBOARD ----------------
            if event.type == pygame.KEYDOWN:

                # Panel modes
                if event.key == pygame.K_1:
                    panel_count = 1
                elif event.key == pygame.K_2:
                    panel_count = 2
                elif event.key == pygame.K_3:
                    panel_count = 3

                # Change algorithms
                elif event.key == pygame.K_q:
                    panel_algorithms[0] = "BFS"
                elif event.key == pygame.K_w:
                    panel_algorithms[0] = "ASTAR"

                elif event.key == pygame.K_a:
                    panel_algorithms[1] = "DIJKSTRA"
                elif event.key == pygame.K_s:
                    panel_algorithms[1] = "DFS"

                elif event.key == pygame.K_z:
                    panel_algorithms[2] = "BFS"
                elif event.key == pygame.K_x:
                    panel_algorithms[2] = "ASTAR"

                # RUN
                elif event.key == pygame.K_SPACE:
                    if start and end:
                        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

                        for (r, c) in walls:
                            grid[r][c] = 1

                        results = []

                        # Run all panels
                        for i in range(panel_count):
                            algo = ALGORITHMS[panel_algorithms[i]]
                            res = algo(start, end, grid)
                            results.append(res)

                            if res:
                                panel_metrics[i] = {
                                    "time": res["time_taken"],
                                    "nodes": len(res["visited_order"]),
                                    "path": len(res["path"])
                                }
                                panel_visited[i] = []
                                panel_path[i] = []

                        # Animate
                        max_len = max(len(r["visited_order"]) for r in results if r)

                        for step in range(max_len):
                            for i in range(panel_count):
                                res = results[i]
                                if res and step < len(res["visited_order"]):
                                    panel_visited[i].append(res["visited_order"][step])

                            draw_all_panels(start, end, walls)
                            pygame.time.delay(10)

                        # Final path
                        for i in range(panel_count):
                            if results[i]:
                                panel_path[i] = results[i]["path"]

                # RESET
                elif event.key == pygame.K_r:
                    start = None
                    end = None
                    walls.clear()

                    for i in range(3):
                        panel_visited[i].clear()
                        panel_path[i].clear()
                        panel_metrics[i] = None

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()