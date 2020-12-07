"""
More complex visualization of acquisitions.
Testing on the first 500 rows.
"""

import pandas as pd 
import networkx as nx 
import plotly.graph_objects as go 

##########################################################################
# Define companies
##########################################################################

class Company:
    def __init__(self, object_id, name, category, status, founding_date, funding_total_usd):
        self.object_id = object_id
        self.name = name
        self.category = category
        self.status = status
        self.founding_date = founding_date
        self.funding_total_usd = funding_total_usd

    def __str__(self):
        return "<b> {} </b> \n Category: {} \n Total Funding: ${}".format(self.name, self.category, self.funding_total_usd)

    def get_object_id(self):
        return self.object_id

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_status(self):
        return self.status

    def get_founding_date(self):
        return self.founding_date

    def get_funding_total_usd(self):
        return self.funding_total_usd

def filter_by_state(acquisitions, offices, state_code):
	state_offices = offices[offices.state_code == state_code].object_id
	acquisitions = acquisitions.dropna()
	return acquisitions[acquisitions.acquiring_object_id.isin(state_offices)]

def row_to_company(row):
    """
    Takes a 1-row DataFrame from objects row and returns a Company object correspoding to that row.
    """
    return Company(object_id=row.loc[0, "id"], name=row.loc[0, "name"], category=row.loc[0, "category_code"], 
        status=row.loc[0, "status"], founding_date=row.loc[0, "founded_at"], funding_total_usd=row.loc[0, "funding_total_usd"])

def get_company(df, object_id):
    """
    Returns Company object corresponding to object_id in DataFrame df.
    """
    row = df[df["id"] == object_id]
    row = row.reset_index()
    return row_to_company(row)

##########################################################################
# Graph
##########################################################################

class VisualGraph(nx.Graph):
    def update_node_positions(self):
        """
		Updates nodes attribute with key "pos" according to spring layout.
		"""
        pos_dict = nx.spring_layout(self)
        for n, p in pos_dict.items():
            self.nodes[n]["pos"] = p
    
    def edge_hover_text(self, edge):
        """
        Return text to show on hover for a given edge.
            - df: DataFrame of company data, e.g. objects.csv
            - G: nx.Graph object
            - edge: ordered pair of object ids
        """
        source, target = edge
        attrs = self.get_edge_data(source, target)
        text = "{} acquired {} for {} {} on {}".format(target.get_name(), source.get_name(),
            str(attrs["price_amount"]), attrs["price_currency_code"], attrs["acquired_at"])
        return text

    def edge_trace(self, line_width=0.5, line_color="#888"):
        edge_x, edge_y = [], []
        edge_text = []
        for edge in self.edges():
            edge_text.append(self.edge_hover_text(edge))
            x0, y0 = self.nodes[edge[0]]["pos"]
            x1, y1 = self.nodes[edge[1]]["pos"]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
			x = edge_x, 
			y = edge_y, 
			line = dict(width = line_width, color = line_color),
			hoverinfo = "text",
			mode = "lines")
        
        edge_trace.text = edge_text

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
				colorscale = "Blues",
				reversescale = False,
				color = [],
				size = 10,
				colorbar = dict(
					thickness = 15,
					title = "Number of Acquisitions",
					xanchor = "left",
					titleside = "right"),
			line_width = 2))
		
        # Set node text
        node_text = []
        for node in self.nodes:
            node_text.append(str(node))
        node_trace.text = node_text

		# Color nodes by number of acquisitions
        node_adjacencies = []
        for node, adjacencies in enumerate(self.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))

        node_trace.marker.color = node_adjacencies
        
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

def graph_from_df(edgelist_df, node_df, source, target, attr=None):
    """
    Creates networkx Graph using edgelist_df. 
    """
    G = nx.from_pandas_edgelist(edgelist_df, source, target, edge_attr=attr, create_using=nx.DiGraph)
    G = nx.relabel_nodes(G, lambda node: get_company(node_df, node))
    G = VisualGraph(G)
    G.update_node_positions()
    return G

##########################################################################
# Execution
##########################################################################

def main():

    acquisitions = pd.read_csv("data/acquisitions.csv")
    offices = pd.read_csv("data/offices.csv")
    objects = pd.read_csv("data/objects.csv", low_memory=False)

    states = ["WA", "CA", "WY", "AL"]

    for state in states:
        acquisitions = filter_by_state(acquisitions, offices, state)
        
        G = graph_from_df(edgelist_df=acquisitions, node_df=objects, source="acquired_object_id", 
            target="acquiring_object_id", attr=["price_amount", "price_currency_code", "acquired_at"])

        fig = G.get_fig("<br>Acquisitions of {} Companies".format(state))
        fig.write_html("acquired_{}.html".format(state))

main()