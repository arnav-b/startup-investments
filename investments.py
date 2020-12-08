
import pandas as pd
from pyvis import network as net

def filter_by_state(investments, offices, state_code):
	state_offices = offices[offices.state_code == state_code].object_id
	investments = investments.dropna()
	return investments[investments.funded_object_id.isin(state_offices)]

def get_state_companies(state_code):
    state_investments = (investments[investments.funded_object_id.isin(state_offices.object_id)]).reset_index()
    state_companies = state_investments.funded_object_id.unique()
    return state_companies

def get_nodes_df (nt):
    return pd.DataFrame(nt.nodes)

def get_company_names(objects, nodes_df, num_companies):
    company_names = {}
    state_objects = (objects[objects.id.isin(nodes_df.id)]).reset_index()
    for idx in range(num_companies):
        company_names[state_objects.id[idx]] = state_objects.name[idx]
    return company_names

def get_company_categories(objects, nodes_df, num_companies):
    company_categories = {}
    state_objects = (objects[objects.id.isin(nodes_df.id)]).reset_index()
    for idx in range(num_companies):
        company_categories[state_objects.id[idx]] = state_objects.category_code[idx]
    return company_categories

def get_nodes_investments(nt, num_companies, state_investments):
    for idx in range(num_companies):
        nt.add_node(state_companies[idx], color = '#1074AB')
    nodes_investments = (state_investments[state_investments.funded_object_id.isin(nodes_df.id)]).reset_index()
    return nodes_investments

def add_funds_edges(nt, nodes_investments, company_names, company_categories, state_companies, num_companies):
    # adds each funder as a node and connects an edge between company and funder
    for idx in range(len(nodes_investments)):
        nt.add_node(nodes_investments.investor_object_id[idx])
        nt.add_edge(nodes_investments.funded_object_id[idx], nodes_investments.investor_object_id[idx])
    
    # creates titles for each node when hovered over (company name, number of connections, company ca)
    for node in nt.nodes:
        if node['id'] in state_companies and node['id'] in company_names.keys():
            node['title'] = ("Company name: " + company_names[str(node['id'])] 
                            + " | Number of funders: " + str(len((nt.get_adj_list())[node['id']]))
                            + " | Category: " + company_categories[str(node['id'])])
    return nt

def create_graph(nt,state_code):
    nt.write_html(str(state_code) + "_investments.html")
    nt.show(str(state_code) + "_investments.html")

def main():
    investments = pd.read_csv("data/investments.csv")
    offices = pd.read_csv("data/offices.csv")
    objects = pd.read_csv("data/objects.csv", low_memory=False)
    nt = net.Network("1000px", "1000px")

    state_code = 'WY'

    investments = filter_by_state(investments, offices, state_code)
    state_companies = get_state_companies(state_code)
    num_companies = len(state_companies)
    nodes = get_nodes_df(nt)
    company_names = get_company_names(objects, nodes_df, num_companies)
    company_categories = get_company_categories(objects, nodes_df, num_companies)

    nodes_investments = get_nodes_investments(nt, num_companies, state_investments)

    nt = add_funds_edges(nt, nodes_investments, company_names, company_categories, state_companies, num_companies)
    
    create_graph(nt, state_code)
