# Network Analysis - Football Passing Network

## Overview
This project performs **network analysis** on football passing data to derive meaningful insights into team dynamics and player roles. By treating passes as edges and players as nodes, we can analyze the overall structure, centrality, and distribution of passes within the network.

## Project Setup
Follow these steps to set up and run the project:

1. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

Once the setup is complete, you can run the analysis scripts provided in the project.

---

## Analysis
The project includes various analyses to explore the passing network structure:

### 1. **Community Detection**
- Identifies groups of players who frequently pass to each other.
- Useful for understanding sub-groups or clusters within the team.

### 2. **Degree Centrality**
- Measures the number of connections each player has.
- Players with high degree centrality are central to the flow of passes.

### 3. **Closeness Centrality**
- Determines how quickly a player can reach others in the network.
- Indicates the players with high positional influence.

### 4. **Betweenness Centrality**
- Identifies players who act as bridges between different clusters.
- These players are critical for maintaining network connectivity.

### 5. **Clustering Coefficient**
- Measures the tendency of players to form tight-knit groups.
- A higher coefficient indicates strong local connections.

---

## Exploratory Data Analysis (EDA)
The following techniques are used to explore and visualize the network:

### 1. **Graph Density**
- Calculates the ratio of actual edges to possible edges.
- Provides insight into the overall connectedness of the network.

### 2. **Heat Map of Passes**
- Visualizes the frequency and intensity of passes between players.
- Highlights key passing routes and connections.

### 3. **Passing Graph Visualization**
- Displays the football passing network as a graph.
- Nodes represent players, and edges represent passes between them.

### 4. **Number of Edges in the Network**
- Retrieves the total number of passes (edges) in the network.
- Indicates overall passing activity.

### 5. **Degree Distribution**
- Plots the distribution of player connections.
- Helps to identify hubs and peripheral players.

### 6. **Average Degree**
- Calculates the mean number of passes per player.
- Reflects the overall activity level of the team.

---

## Visualizations
This project includes intuitive and interactive visualizations:
- **Passing Networks:** Node-link diagrams to showcase player connections.
- **Heat Maps:** Visual heat maps for identifying strong passing links.
- **Centrality Maps:** Highlights key players based on centrality measures.

---

## Results & Insights
- Discover **key players** who influence passing networks.
- Identify **clusters** or sub-teams based on passing behavior.
- Analyze overall team cohesion through network density and clustering metrics.
- Evaluate player roles (e.g., playmakers, bridges) using centrality measures.

---

## Tools & Libraries
The project utilizes the following tools and libraries:
- **NetworkX** - For network creation and analysis.
- **Matplotlib** - For graph and data visualizations.
- **Pandas** - For data handling and preprocessing.
- **Seaborn** - For heatmap visualizations.
- **Python** - Core programming language.

---

## Future Scope
- Extend the analysis to multiple matches to identify trends over time.
- Add positional data to improve spatial analysis of the passing network.
- Incorporate player performance metrics to enhance insights.
- Automate report generation with interactive dashboards.

