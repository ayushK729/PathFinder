# path finding engine version 1
import time
from collections import deque
from Algorithms.grid_utility import get_neighbors, reconstruct_path

# function to calculate neighbors of current node
def get_neighbors(node,grid):
    x,y=node
    direction_set=[(-1,0),(+1,0),(0,+1),(0,-1)]
    neighbors=[]
    row=len(grid)
    col=len(grid[0])

    for dx,dy in direction_set:
        nx,ny=x+dx,y+dy
        if 0<=nx<row and 0<=ny<col:
            if grid[nx][ny]==0:
                neighbors.append((nx,ny))
        
    return neighbors

# algorithm for Breadth First Search
def bfs(start,end,grid):
    start_time=time.time()
    queue=deque([start])
    visited_node=set([start])
    parent={}
    visited_order=[]

    while queue:
        current=queue.popleft()
        visited_order.append(current)

        if(current == end):
            end_time=time.time()
            path=path_reconstruct(parent,start,end)
            return {
                "visited_order":visited_order,
                "path":path,
                "time_taken":end_time-start_time
            }
        
        for neighbor in get_neighbors(current,grid):
            if neighbor not in visited_node:
                visited_node.add(neighbor)
                parent[neighbor]=current
                queue.append(neighbor)

    return None

def path_reconstruct(parent,start,end):
    path=[]
    current = end
    while current!=start:
        path.append(current)
        current=parent[current]

    path.append(start)
    path.reverse()
    return path

if __name__ == "__main__":
   start=(3,3)
   end=(0,0)
   result=bfs(start,end)

   if result:
       print("Visited Order: ",result["visited_order"])
       print("Path --> ",result["path"])
       print("Time Taken --> ", result["time_taken"])

   else:
        print("No path found!")
    

    