"""
Graph visualization of acquisitions.
"""

import pandas as pd 
import plotly.graph_objects as go 
import networkx as nx 

acquisitions = pd.read_csv("data/acquisitions.csv")
acquisitions = acquisitions.head(3000)

G = nx.from_pandas_edgelist(acquisitions, "acquired_object_id", "acquiring_object_id",
	["price_amount", "price_currency_code", "acquired_at"])

pos_dict = nx.spring_layout(G)
for n, p in pos_dict.items():
	G.nodes[n]["pos"] = p

edge_x, edge_y = [], []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]["pos"]
    x1, y1 = G.nodes[edge[1]]["pos"]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])	
	 
edge_trace = go.Scatter(
	x = [],
	y = [],
	line = dict(width=0.5, color = "#888"),
	hoverinfo = "text",
	mode = "lines")

node_x, node_y = [], []
for node in G.nodes():
	x, y = G.nodes[node]["pos"]
	node_x.append(x)
	node_y.append(y)
	
node_trace = go.Scatter(
	x = node_x, y = node_y,
	mode = "markers",
	hoverinfo = "text",
	marker = dict(
		showscale = True,
		colorscale = "YlOrRd",
		reversescale = False,
		color = [],
		size = 10,
		colorbar = dict(
			thickness = 15,
			title = "Number of Acquisitions",
			xanchor = "left",
			titleside = "right"),
	line_width = 2))

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of acquisitions: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

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
