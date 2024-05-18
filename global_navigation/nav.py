import random
import math
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.parent = None

def get_distance(node1, node2):
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def get_nearest_node(tree, point):
    nearest_node = tree[0]
    min_distance = get_distance(nearest_node, point)
    for node in tree:
        distance = get_distance(node, point)
        if distance < min_distance:
            min_distance = distance
            nearest_node = node
    return nearest_node

def steer(nearest_node, sampled_point, step_size):
    distance = get_distance(nearest_node, sampled_point)
    if distance <= step_size:
        return sampled_point
    else:
        theta = math.atan2(sampled_point.y - nearest_node.y, sampled_point.x - nearest_node.x)
        new_x = nearest_node.x + step_size * math.cos(theta)
        new_y = nearest_node.y + step_size * math.sin(theta)
        return Node(new_x, new_y)

def is_collision_free(nearest_node, new_node, obstacles):
    for obstacle in obstacles:
        xmin, xmax, ymin, ymax = obstacle
        if xmin <= new_node.x <= xmax and ymin <= new_node.y <= ymax:
            return False
    return True

def rrt(start, goal, obstacles, x_max, y_max, step_size, max_iterations):
    tree = [start]
    for i in range(max_iterations):
        if random.random() < 0.1:
            sampled_point = goal
        else:
            sampled_x = random.random() * x_max
            sampled_y = random.random() * y_max
            sampled_point = Node(sampled_x, sampled_y)
        nearest_node = get_nearest_node(tree, sampled_point)
        new_node = steer(nearest_node, sampled_point, step_size)
        if is_collision_free(nearest_node, new_node, obstacles):
            new_node.parent = nearest_node
            tree.append(new_node)
            if get_distance(new_node, goal) < step_size:
                goal.parent = new_node
                # Construir el camino encontrado
                path = [goal]
                while goal.parent:
                    path.append(goal.parent)
                    goal = goal.parent
                path.reverse()  # Revertir la lista para tener el camino desde start hasta goal
                return path
    return None

def plot_path(path, obstacles):
    plt.figure(figsize=(8, 8))
    plt.xlim(0, 10)
    plt.ylim(0, 10)

    for obstacle in obstacles:
        xmin, xmax, ymin, ymax = obstacle
        width = xmax - xmin
        height = ymax - ymin
        rect = plt.Rectangle((xmin, ymin), width, height, color='gray')
        print(rect)
        plt.gca().add_patch(rect)

    # Dibujar camino
    path_x = [node.x for node in path]
    path_y = [node.y for node in path]
    plt.plot(path_x, path_y, color='blue', linewidth=2)

    plt.scatter(start.x, start.y, color='green', s=100, label='Start')
    plt.scatter(goal.x, goal.y, color='red', s=100, label='Goal')

    plt.title("RRT Path Planning")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.grid(True)
    plt.savefig("ddee.png")
    #plt.show()



start = Node(0, 0)
goal = Node(2, 8)

obstacles = [[1,3,2,6]]  # Define tus obstáculos como [xmin, xmax, ymin, ymax]

x_max, y_max = 10, 10

step_size = 1.0

max_iterations = 1000

path = rrt(start, goal, obstacles, x_max, y_max, step_size, max_iterations)

if path:
    print("Path found")
    plot_path(path, obstacles)
else:
    print("No path found.")
