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
import acquisitions

class Company:
    def __init__(self, object_id, name, category, status, founding_date, funding_total_usd):
        self.object_id = object_id
        self.name = name
        self.category = category
        self.status = status
        self.founding_date = founding_date
        self.funding_total_usd = funding_total_usd

    def __str__(self):
        return self.name

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

class Fund:
    def __init__(self, object_id, name, funding_date, raised_amount, raised_currency_code):
        self.object_id = object_id
        self.name = name 
        self.funding_date = funding_date
        self.raised_amount = raised_amount
        self.raised_currency_code = raised_currency_code

    def __str__(self):
	    return self.object_id, self.name
	
    def get_object_id(self):
	    return self.object_id

    def get_name(self):
        return self.name

    def get_funding_date(self):
        return self.funding_date
        
    def get_raised_amount(self):
        return self.raised_amount

    def get_raised_currency_code(self):
        return self.raised_currency_code

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
    # When full df isn't loaded some rows will not be in the df
    if len(row) == 0:
        print("row is empty df")
        return None
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
        - df: DataFrame of company data
        - graph: nx.Graph object
        - edge: ordered pair of object ids
    """
    source, target = edge
    attrs = graph.get_edge_data(source, target)
    text = "{} acquired {} for {} {} on {}".format(get_company(df, target).get_name(), get_company(df, source).get_name(),
        str(attrs["price_amount"]), attrs["price_currency_code"], attrs["acquired_at"])
    return text

##########################################################################
# Testing

def graph_from_df(df, source, target, attr=None):
	"""
	Creates graph using edgelist in df. 
	"""
	graph = nx.from_pandas_edgelist(df, source, target, edge_attr=attr, create_using=nx.DiGraph)
    
	return graph        

acquisitions = pd.read_csv("data/acquisitions.csv", nrows=100)
objects = pd.read_csv("data/objects.csv", nrows=3000)
graph = graph_from_df(df=acquisitions, source="acquired_object_id", target="acquiring_object_id", 
    attr=["price_amount", "price_currency_code", "acquired_at"])

print(graph.nodes)

# for edge in list(graph.edges())[:10]:
#     print(edge_hover_text(objects, graph, edge))
# edge = ("c:10", "c:11")
# print(acquisitions.columns)
# row = objects[objects.id == "c:11"]
# print(row)
# print(row.loc[0, "category_code"])
# print(get_company(objects, "c:11"))
# print(edge_hover_text(objects, graph, edge))
# print(get_company(df, "c:1"))