"""
Graph visualization of acquisitions.
"""

import pandas as pd
import plotly.graph_objects as go
import networkx as nx 

def add_edge(graph, edge, edge_x, edge_y):
	"""
	Add coordinates of edge to edge_x and edge_y
	"""
	x0, y0 = graph.nodes[edge[0]]["pos"]
	x1, y1 = graph.nodes[edge[1]]["pos"]
	edge_x.extend([x0, x1, None])
	edge_y.extend([y0, y1, None])

def create_edge_trace(graph):
	"""
	Create all edges as disconnected lines.
	"""
	edge_x, edge_y = [], []
	for edge in graph.edges():
		add_edge(graph, edge, edge_x, edge_y)	
	 
	edge_trace = go.Scatter(
		x = [],
		y = [],
		line = dict(width=0.5, color = "#888"),
		hoverinfo = "text",
		mode = "lines")
	
	return edge_trace	

def create_node_trace(graph):
	"""
	Creates all nodes as scatter traces.
	"""
	node_x, node_y = [], []
	for node in graph.nodes():
		x, y = graph.nodes[node]["pos"]
		node_x.append(x)
		node_y.append(y)
	
	node_trace = go.scatter(
		x = node_x, y = node_y,
		mode = "markers",
		hoverinfo = "text",
		marker = dict(
			showscale = True,
			colorscale = "YlOrRd",
			reversescale = True,
			color = [],
			size = 10,
			colorbar = dict(
				thickness = 15,
				title = "Number of Acquisitions",
				xanchor = "left",
				titleslide = "right"),
		line_width = 2))
	
	return node_trace

def color_nodes(graph):
	"""
	Color nodes by number of acquisitions.
	"""
	pass

def run():
	acquisitions = pd.read_csv("data/acquisitions.csv")
	acquisitions = acquisitions.head(200)

	G = nx.from_pandas_edgelist(acquisitions, "acquired_object_id", "acquiring_object_id",
		["price_amount", "price_currency_code", "acquired_at"])

	pos_dict = nx.spring_layout(G)
	for n, p in pos_dict.items():
		G.nodes[n]["pos"] = p
	
	edge_trace = create_edge_trace(G)
	node_trace = create_node_trace(G)
	
	fig = go.Figure(data = [edge_trace, node_trace],
		layout = go.Layout(
			title = "<br>Acquisitions",
			titlefont_size = 16,
			showlegend = False,
			hovermode = "closest",
			margin = dict(b=20, l=5, r=5, t=40),
			xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

	fig.write_html("acquisitions.html")

run()
