def get_neighbors(node, grid):
    x, y = node
    directions = [(-1,0),(1,0),(0,1),(0,-1)]

    rows = len(grid)
    cols = len(grid[0])

    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))

    return neighbors


def reconstruct_path(parent, start, end):
    path = []
    current = end

    while current != start:
        if current not in parent:
            return None
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path