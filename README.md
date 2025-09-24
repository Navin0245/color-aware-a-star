# Color-Aware A* Grid Pathfinding

This project implements an A* search algorithm for grid navigation with a color-aware heuristic. It finds the optimal path to a target cell while considering cell colors that influence path cost, incorporating penalties and rewards based on agent preferences.

## Features

- Grid-based pathfinding with obstacles and special target ('H') cell.
- Manhattan distance combined with color-based penalty heuristic.
- Agent types with different cost preferences for red and green cells.
- Visualization of the grid and the path found using matplotlib.
- Easy to configure start position, grid scenarios, agent type, and target color.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `matplotlib` library for visualization

Install matplotlib via pip if you don't have it:


### Usage

1. Clone this repository:
2. Navigate to the project directory and run the script:

3. The program will perform A* search on the predefined grid and display the path grid visualization.

## Project Structure

- `scenario_I` and `scenario_II`: Example grid scenarios with different color arrangements.
- `AStarSearch` class: Core implementation of the A* search algorithm with color-aware heuristics.
- Visualization function shows the grid, heart position, and the resultant path.

## How It Works

- The agent searches from a start position to the heart cell ('H').
- Movement cost depends on cell color and agent type preferences.
- The heuristic combines Manhattan distance and a color penalty to guide search efficiently.
- Matplotlib visualizes the final path on the grid.

## Extending the Project

- Add different grid scenarios.
- Implement different heuristics or agent preferences.
- Improve visualization with open/closed sets display.
- Add user input for custom start and target settings.

## License

This project is licensed under the MIT License.

## Author

Navin0245

---

Feel free to open issues or create pull requests for improvements!

