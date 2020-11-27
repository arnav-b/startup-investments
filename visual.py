"""
More complex visualization of acquisitions.
Testing on the first 500 rows.
Final output: graph of company acquisitions with the following traits:
    - Filterable by company category
    - Edges labeled with date of acquisition, direction, and amount paid upon hover
    - Nodes are companies, labeled with company name, location, and date of creation
    - Nodes colored as follows: blue(?) if acquired at any point, otherwise colored on red-yellow scale by number of acquisitions
Subproblems:
    - Match company IDs to companies (in separate files)
    - How to get edge labels
    - Label nodes
    - Custom node coloring
    - Graph filtering
"""

import pandas as pd 
import networkx as nx 
import plotly.graph_objects as go 
import objects
import acquisitions

def row_to_company(row):
    """
    Takes a 1-row DataFrame from objects row and returns a Company object correspoding to that row.
    """
    return objects.Company(object_id=row.loc[0, "id"], name=row.loc[0, "name"], category=row.loc[0, "category_code"], 
        status=row.loc[0, "status"], founding_date=row.loc[0, "founded_at"], funding_total_usd=row.loc[0, "funding_total_usd"])

def get_company(df, object_id):
    """
    Returns Company object corresponding to object_id in DataFrame df.
    """
    row = df[df["id"] == object_id]
    return row_to_company(row)

def node_hover_text(node):
    """
    Return text to show on hover for a given node.
    """
    return "<b>" + node.get_name() + "</b>" + "\n" + "Category: " + node.get_category() + "\n" + "Total Funding: $" + \
            str(node.get_funding_total_usd())

def edge_hover_text(df, graph, edge):
    """
    Return text to show on hover for a given edge.
    """
    source, target = edge[0:2]
    attrs = graph.get_edge_data(source, target)
    text = get_company(df, target).get_name() + " acquired " + get_company(df, source).get_name() + " for " + str(attrs["price_amt"]) + \
        attrs["price_currency_code"] + " on " + attrs["acquired_at"]
    return text

##########################################################################
# Testing

def graph_from_csv(df, source, target, attr=None):
	"""
	Creates graph using edgelist stored as .csv at filename.
	
	filename: string, path to file
	numrows: int, number of rows to read
	source: valid column name for source node
	target: valid column name for acquired node
	attr: list of valid column names to be added as edge attributes 
	"""
	graph = nx.from_pandas_edgelist(df, source, target, edge_attr=attr, create_using=nx.DiGraph)

	return graph        

df = pd.read_csv("data/acquisitions.csv", nrows=100)
graph = graph_from_csv(df=df, source="acquired_object_id", target="acquiring_object_id", 
    attr=["price_amount", "price_currency_code", "acquired_at"])

# print(graph.edges)
edge = ("c:10", "c:11")
# print(edge_hover_text(df, graph, edge))
print(df[df["id"] == "c:10"])
# print(get_company(pd.read_csv("data/objects.csv", nrows=500), "c:10"))