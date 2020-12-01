"""
Graph visualization of acquisitions.
TODO: 
	Color nodes based on whether acquired first, then by number of acquisitions
	Add text: company name and category for nodes, data of acquisition/amount paid for edges
	Show change over time, possibly with animated model
"""

import pandas as pd 
import plotly.graph_objects as go 
import networkx as nx 
import time

class VisualGraph(nx.DiGraph): 
	"""
	Visual representation of networkx Graph.
	"""

	def update_node_positions(self):
		"""
		Updates nodes attribute with key "pos" according to spring layout.
		"""
		pos_dict = nx.spring_layout(self)
		for n, p in pos_dict.items():
			self.nodes[n]["pos"] = p
		
	def edge_trace(self, line_width=0.5, line_color="#888"):
		# Define positions for edges
		edge_x, edge_y = [], []
		for edge in self.edges():
			x0, y0 = self.nodes[edge[0]]["pos"]
			x1, y1 = self.nodes[edge[1]]["pos"]
			edge_x.extend([x0, x1, None])
			edge_y.extend([y0, y1, None])	

		 # Create scatter object
		edge_trace = go.Scatter(
			x = edge_x, 
			y = edge_y, 
			line = dict(width = line_width, color = line_color),
			hoverinfo = "text",
			mode = "lines")

		return edge_trace
	
	def node_trace(self):
		# Define positions for nodes
		node_x, node_y = [], []
		for node in self.nodes():
			x, y = self.nodes[node]["pos"]
			node_x.append(x)
			node_y.append(y)
		
		# Create scatter object
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
		
		# Color nodes by number of acquisitions
		node_adjacencies = []
		node_text = []
		for node, adjacencies in enumerate(self.adjacency()):
			node_adjacencies.append(len(adjacencies[1]))
			node_text.append("# of acquisitions: " + str(len(adjacencies[1])))

		node_trace.marker.color = node_adjacencies
		node_trace.text = node_text
		
		return node_trace

	def get_fig(self, fig_title):
		"""
		Create plotly Figure object titled with string fig_title.
		"""
		fig = go.Figure(data = [self.edge_trace(), self.node_trace()],
			layout = go.Layout(
				title = fig_title,
				titlefont_size = 16,
				showlegend = False,
				hovermode = "closest",
				margin = dict(b=20, l=5, r=5, t=40),
				xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
				yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
				)

		return fig

def filter_by_state(acquisitions, offices, state_code):
	state_offices = offices[offices.state_code == state_code].object_id
	acquisitions = acquisitions.dropna()
	return acquisitions[acquisitions.acquiring_object_id.isin(state_offices)]

def graph_from_edgelist(acquisitions, offices, state_code, source, target, attr=None):
	"""
	Creates graph using edgelist stored as .csv at filename.
	
	filename: string, path to file
	numrows: int, number of rows to read
	source: valid column name for source node
	target: valid column name for acquired node
	attr: list of valid column names to be added as edge attributes 
	"""
	acquisitions = pd.read_csv(acquisitions)
	offices = pd.read_csv(offices)

	acquisitions = filter_by_state(acquisitions, offices, state_code)

	graph = nx.from_pandas_edgelist(acquisitions, source, target, edge_attr=attr)
	graph = VisualGraph(graph)
	graph.update_node_positions()

	return graph

def main():
	start_time = time.time()

	graph = graph_from_edgelist(acquisitions="data/acquisitions.csv", offices="data/offices.csv", state_code="CA", source="acquired_object_id", 
	target="acquiring_object_id", attr=["price_amount", "price_currency_code", "acquired_at"])
	fig = graph.get_fig("<br>Acquisitions")
	fig.write_html("acquisitions.html")

	print("Execution time:", str(time.time() - start_time), "seconds")

if __name__ == "__main__":
	main()