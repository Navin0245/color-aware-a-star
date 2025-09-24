import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Set, Optional, Any


scenario_I = [
    ['R', 'G', 'G', 'G', 'R', 'G'],
    ['G', 'G', 'G', 'R', 'G', 'G'],
    ['G', 'G', 'R', 'H', 'G', 'G'],
    ['G', 'R', 'G', 'G', 'G', 'R'],
    ['R', 'G', 'G', 'G', 'R', 'G'],
    ['G', 'G', 'G', 'R', 'G', 'G']
]


scenario_II = [
    ['R', 'G', 'R', 'G', 'R', 'G'],
    ['G', 'R', 'G', 'R', 'G', 'R'],
    ['R', 'G', 'H', 'G', 'R', 'G'],
    ['G', 'R', 'G', 'R', 'G', 'R'],
    ['R', 'G', 'R', 'G', 'R', 'G'],
    ['G', 'R', 'G', 'R', 'G', 'R']
]


class AStarSearch:
    def __init__(
        self,
        grid: List[List[str]],
        heart_color: str,
        start: Tuple[int, int],
        agent_type: str,
    ) -> None:
        self.grid = grid
        self.heart_color = heart_color
        self.start = start
        self.agent_type = agent_type
        self.agent_color = None  # will be set by agent()

    def agent(self, color: str = "red") -> str:
        """Sets and returns the agent's color."""
        self.agent_color = color
        return self.agent_color

    def get_heart_position(self) -> Optional[Tuple[int, int]]:
        """Find the position of 'H' in the grid."""
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 'H':
                    return (i, j)
        return None

    def get_color(self, position: Tuple[int, int]) -> str:
        """Return color name based on cell content at position."""
        color_map = {'G': 'green', 'R': 'red', 'H': self.heart_color}
        row, col = position
        cell = self.grid[row][col]
        return color_map.get(cell, 'unknown')

    def start_color(self) -> Dict[Tuple[int, int], str]:
        """Return the starting position mapped to its color."""
        position = self.start
        return {position: self.get_color(position)}

    def get_neighbours(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Return valid neighboring cell coordinates (up, down, left, right)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        row, col = position
        neighbours = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]):
                neighbours.append((r, c))
        return neighbours

    def path_cost(self, position: Tuple[int, int]) -> int:
        """Calculate cost contribution of moving onto a specific cell."""
        cell_color = self.get_color(position)
        if self.agent_type == 'R1':
            return 10 if cell_color == 'green' else -10 if cell_color == 'red' else 0
        elif self.agent_type == 'G1':
            return -10 if cell_color == 'green' else 10 if cell_color == 'red' else 0
        return 0

    def transition_cost(self) -> int:
        """Cost to move from one cell to an adjacent cell (uniform)."""
        return 1

    def manhattan_distance(self, position: Tuple[int, int]) -> int:
        """Calculate Manhattan distance from position to heart."""
        heart_position = self.get_heart_position()
        if heart_position is None:
            return 0
        return abs(position[0] - heart_position[0]) + abs(position[1] - heart_position[1])

    def color_penalty(self, position: Tuple[int, int]) -> int:
        """Penalty or bonus if cell color matches or differs from heart color."""
        heart_position = self.get_heart_position()
        if heart_position is None:
            return 0
        if self.get_color(position) == self.get_color(heart_position):
            return -5
        else:
            return 5

    def heuristic_value(self, position: Tuple[int, int]) -> int:
        """Heuristic combining Manhattan distance and color penalty."""
        return self.manhattan_distance(position) + self.color_penalty(position)

    def goal_test(self, position: Tuple[int, int]) -> bool:
        """Check if position is the goal (heart)."""
        return position == self.get_heart_position()

    def search(self) -> Tuple[List[Tuple[int, int]], float, Set[Tuple[int, int]], Dict]:
        """Perform A* search and return path, cost, explored and open sets."""
        goal = self.get_heart_position()
        if goal is None:
            print("No heart position ('H') found in grid.")
            return [], float('inf'), set(), {}

        open_list: Dict[Tuple[int, int], float] = {}
        closed_list: Set[Tuple[int, int]] = set()
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {self.start: 0}
        current = self.start

        while True:
            if self.goal_test(current):
                break

            closed_list.add(current)
            neighbours = self.get_neighbours(current)
            cost_map: Dict[Tuple[int, int], float] = {}

            for neighbour in neighbours:
                if neighbour in closed_list:
                    continue

                transition = self.transition_cost()
                path_c = self.path_cost(neighbour)
                heuristic = self.heuristic_value(neighbour)
                total_g = g_score[current] + transition + path_c

                if neighbour not in g_score or total_g < g_score[neighbour]:
                    g_score[neighbour] = total_g
                    f_cost = total_g + heuristic
                    cost_map[neighbour] = f_cost
                    came_from[neighbour] = current

            if not cost_map:
                print("No path found!")
                return [], float('inf'), closed_list, open_list

            # Select neighbour with the lowest f-cost
            current = min(cost_map, key=cost_map.get)

        # Reconstruct path from goal to start
        path = []
        node = goal
        while node in came_from:
            path.append(node)
            node = came_from[node]
        path.append(self.start)
        path.reverse()

        return path, g_score[goal], closed_list, open_list

    def visualize_grid(self) -> None:
        """Visualize the grid and the path found using matplotlib."""
        color_map = {'G': 'green', 'R': 'red', 'H': self.heart_color}
        fig, ax = plt.subplots()

        path, _, _, _ = self.search()
        goal = self.get_heart_position()

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = color_map.get(cell, 'gray')
                rect = plt.Rectangle((j, i), 1, 1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)

                pos = (i, j)
                if pos == goal:
                    ax.text(j + 0.5, i + 0.5, 'H', color='black', ha='center', va='center', fontsize=12)
                elif pos in path:
                    ax.text(j + 0.5, i + 0.5, '*', color='black', ha='center', va='center', fontsize=20)

        ax.set_xlim(0, len(self.grid[0]))
        ax.set_ylim(0, len(self.grid))
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')
        plt.show()


# Instantiate and run search on scenario_II
a_star = AStarSearch(grid=scenario_II, agent_type="R1", start=(5, 5), heart_color="red")
path, score, closed_list, open_list = a_star.search()
a_star.visualize_grid()

print(f"Path:-> {path}")
print(f"Length of Path:-> {len(path)}")
print(f"Total Cost:-> {score}")
print(f"Open List:-> {open_list}")
print(f"Closed List:-> {closed_list}")
