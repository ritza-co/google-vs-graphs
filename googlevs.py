# https://medium.com/applied-data-science/the-google-vs-trick-618c8fd5359f
# this doesn't have all the functionality described there (e.g. 'ego radiuses', but just explores one keyword a few levels deep.
# copy the output into a copy of the relevant data sheets at 
# https://app.flourish.studio/visualisation/2947914/edit


import requests
import re
import urllib.parse
import json

import time
import random
from collections import defaultdict

# SEED = input("Enter a seed word: ")

def get_auto_suggestions(searchterm):
    autocomplete_url = "http://suggestqueries.google.com/complete/search?&output=toolbar&gl=us&hl=en&q="
    enc = urllib.parse.quote(searchterm)
    autocomplete_url += searchterm
    xml_response = requests.get(autocomplete_url).text
    suggestion_search = re.findall(r'data="(.+?)"', xml_response)
    suggestions = []
    for match in suggestion_search:
        suggestions.append(match)
    return suggestions


def clean_suggestions(suggestions, searchterm):
    cleaned = []

    for suggestion in suggestions:
        if len(cleaned) >= 5:
            break
        if suggestion.count("vs") > 1:
            continue
        if suggestion.count(searchterm) > 1:
            continue
        if any([x in suggestion for x in cleaned]):
            continue
        try:
            suggestion = suggestion.split(searchterm + " vs")[1]
            if suggestion:
                cleaned.append(suggestion.strip())
        except Exception as e:
            continue
    return cleaned

def build_graph(seed, depth=5):
    done = set()
    frontier = [seed]
    edges = []
    nodes = {}
    while depth > 0 and frontier:
        term = frontier.pop(0)
        if term not in done:
            done.add(term)
        else:
            continue

        nodes[term] = depth
        depth -= 1

        suggestions = get_auto_suggestions(term + " vs ")
        clean = clean_suggestions(suggestions, term)

        # first results have higher score, so go backwards
        for score, result in enumerate(clean[::-1]):
            edges.append((term, result, score+1))
        frontier.extend(clean)
        time.sleep(random.randrange(5)/10)

    for edge in edges:
        frm, to = edge[0], edge[1]
        if frm not in nodes:
            nodes[frm] = 1

        if to not in nodes:
            nodes[to] = 1
    return edges, nodes
    
def get_d3_json(seed):
    edges, nodes = build_graph(seed,10)
    
    name_id = {}
    d3nodes = []
    d3edges = []
    # node = 
    # {id: 0, name: name, value: 4, group: 2}
    for i, node in enumerate(nodes):
        d3node = {
            "id": i,
            "name": node,
            "value": nodes[node] * 20,
            "group": nodes[node]
        }
        d3nodes.append(d3node)
        name_id[node] = i
        
    for edge in edges:
        d3edge = {
            "source": name_id[edge[0]],
            "target": name_id[edge[1]]
        }
        d3edges.append(d3edge)
        
    d3nodesedges = {
        "nodes": d3nodes,
        "links": d3edges
    }
    return d3nodesedges
    
    
