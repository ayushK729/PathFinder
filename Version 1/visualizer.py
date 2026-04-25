import pygame
import sys
from Algorithms.bfs import bfs
from Algorithms.a_star import astar
from Algorithms.dijkstra import dijkstra
from Algorithms.dfs import dfs

ALGORITHMS = {
    "BFS": bfs,
    "ASTAR": astar,
    "DIJKSTRA": dijkstra,
    "DFS": dfs
}

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
DARK = (50, 50, 50)
LIGHT_GREY = (170, 170, 170)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

font = pygame.font.SysFont(None, 28)

# ---------------- DROPDOWN ----------------
dropdown_open = False
dropdown_rect = pygame.Rect(10, 10, 150, 30)
options = list(ALGORITHMS.keys())

# ---------------- DRAW ----------------
def draw_grid(start, end, walls, visited, path, algorithm, time_taken, nodes_visited, path_length):
    screen.fill(BLACK)

    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

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

    # Draw dropdown
    pygame.draw.rect(screen, LIGHT_GREY, dropdown_rect)
    text = font.render(algorithm, True, BLACK)
    screen.blit(text, (dropdown_rect.x + 5, dropdown_rect.y + 5))

    if dropdown_open:
        for i, option in enumerate(options):
            rect = pygame.Rect(10, 10 + (i + 1) * 30, 150, 30)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            option_text = font.render(option, True, BLACK)
            screen.blit(option_text, (rect.x + 5, rect.y + 5))

    # Draw metrics
    if time_taken is not None:
        t1 = font.render(f"Time: {time_taken:.5f}s", True, WHITE)
        screen.blit(t1, (10, 200))

    if nodes_visited is not None:
        t2 = font.render(f"Nodes Visited: {nodes_visited}", True, WHITE)
        screen.blit(t2, (10, 230))

    if path_length is not None:
        t3 = font.render(f"Path Length: {path_length}", True, WHITE)
        screen.blit(t3, (10, 260))

    pygame.display.update()


# ---------------- MAIN ----------------
def main():
    global dropdown_open

    start = None
    end = None
    walls = set()

    visited = []
    path = []

    current_algorithm = "BFS"

    # Metrics
    time_taken = None
    nodes_visited = None
    path_length = None

    running = True

    while running:
        draw_grid(start, end, walls, visited, path,
                  current_algorithm, time_taken, nodes_visited, path_length)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if dropdown_rect.collidepoint(pos):
                    dropdown_open = not dropdown_open

                elif dropdown_open:
                    for i, option in enumerate(options):
                        rect = pygame.Rect(10, 10 + (i + 1) * 30, 150, 30)
                        if rect.collidepoint(pos):
                            current_algorithm = option
                            dropdown_open = False

                else:
                    row = pos[1] // CELL_SIZE
                    col = pos[0] // CELL_SIZE

                    if not start:
                        start = (row, col)
                    elif not end:
                        end = (row, col)
                    else:
                        walls.add((row, col))

            # Keyboard
            if event.type == pygame.KEYDOWN:

                # Run algorithm
                if event.key == pygame.K_SPACE:

                    if start and end:
                        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

                        for (r, c) in walls:
                            grid[r][c] = 1

                        algo_function = ALGORITHMS.get(current_algorithm)
                        result = algo_function(start, end, grid) if algo_function else None

                        if result:
                            visited.clear()
                            path.clear()

                            # ✅ METRICS CALCULATED HERE (correct place)
                            nodes_visited = len(result["visited_order"])
                            path_length = len(result["path"])
                            time_taken = result["time_taken"]

                            # Animate visited
                            for node in result["visited_order"]:
                                visited.append(node)
                                draw_grid(start, end, walls, visited, path,
                                          current_algorithm, time_taken, nodes_visited, path_length)
                                pygame.time.delay(15)

                            # Animate path
                            for node in result["path"]:
                                path.append(node)
                                draw_grid(start, end, walls, visited, path,
                                          current_algorithm, time_taken, nodes_visited, path_length)
                                pygame.time.delay(40)

                        else:
                            print("No path found!")

                # Reset
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    walls.clear()
                    visited.clear()
                    path.clear()

                    # Reset metrics
                    time_taken = None
                    nodes_visited = None
                    path_length = None

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()