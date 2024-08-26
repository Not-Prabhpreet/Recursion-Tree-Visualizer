# Recursion Tree Visualizer

Recursion Tree Visualier is a web app that can help users visualize the order and return values of recursive function calls as a tree structure, helping users understand and debug recursive algorithms.

## Live Demo

Check out the live application: [Recursion Tree Visualizer](https://recursion-tree-visualizer.onrender.com/)

## Features

- Visualize recursive function calls as a tree
- Support for multiple recursive algorithms
- Interactive tree diagram
- Step-by-step execution visualization

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Visualization**: Graphviz
- **Containerization**: Docker
- **Deployment**: Render

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/recursion-tree-visualizer.git
   cd recursion-tree-visualizer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python wsgi.py
   ```

4. Open a web browser and navigate to `http://localhost:5000`

## Docker

This project is containerized using Docker. To run it using Docker:

1. Build the Docker image:
   ```
   docker build -t recursion-visualizer .
   ```

2. Run the Docker container:
   ```
   docker run -p 4000:80 recursion-visualizer
   ```

3. Access the application at `http://localhost:4000`

## Usage

1. Select a recursive algorithm from the dropdown menu
2. Enter the required input parameters
3. Click "Visualize" to generate the recursion tree
4. Use the controls to step through the recursive calls

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


Project Link: [https://github.com/Not-Prabhpreet/Recursion-Tree-Visualizer](https://github.com/Not-Prabhpreet/Recursion-Tree-Visualizer)
