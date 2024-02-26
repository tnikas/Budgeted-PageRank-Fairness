#!/usr/bin/env python
# coding: utf-8


import networkx as nx, math, sys, numpy as np, matplotlib.pyplot as plt, time, csv, os
from tqdm import tqdm
from collections import defaultdict

phi = float(sys.argv[1])
gRed = float(sys.argv[2])
gBlue = float(sys.argv[3])
difGamma = int(sys.argv[4])
whichG = str(sys.argv[5])

print("----------------------")
print(phi, gRed, gBlue, difGamma, whichG)
print("----------------------")


def read_community(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    # Extract the number of communities
    num_communities = int(lines[0].strip())

    # Process the data for each node
    for line in lines[1:]:
        node, community = map(int, line.strip().split())
        if community == 1:
            red.append(node)
        elif community == 0:
            blue.append(node)
        
def makeGraph(filename):
    with open(filename, "r") as file:
        num_nodes = int(file.readline().strip())  # Extract the number of nodes

        for line in file:
            line = line.strip()
            line = line.split("\t")
            source = int(line[0])
            target = int(line[1])
            G.add_edge(source, target)
        for node in G.nodes:
            if G.has_edge(node, node):
                G.remove_edge(node, node)
    #             print(node)


def outRB():
    for node in G.nodes:
        G.nodes[node]['outR'] = 0
        G.nodes[node]['outB'] = 0
        G.nodes[node]['outRList'] = []
        G.nodes[node]['outBList'] = []
        for n in G.neighbors(node):
            if n in red:
                G.nodes[node]['outR'] += 1
                G.nodes[node]['outRList'].append(n)
            elif n in blue:
                G.nodes[node]['outB'] += 1
                G.nodes[node]['outBList'].append(n)


def initlR():
    tmplR = []
    for node in G.nodes:
        if G.out_degree(node) != 0 and G.nodes[node]['outR'] / G.out_degree(node) < phi and G.nodes[node]['outR'] != 0:
            tmplR.append(node)
    return tmplR


def updateD(node):
    for i in G.nodes[node]['outRList']:
#         D[node][i] = (phi - (G.nodes[node]['outR'] / G.degree(node))) / G.nodes[node]['outR']
        D[node][i] = (phi/G.nodes[node]['outR']) - (1/G.out_degree(node))
    for i in G.nodes[node]['outBList']:
#         D[node][i] = ((G.nodes[node]['outR'] / G.degree(node)) - phi) / G.nodes[node]['outB']
        D[node][i] = ((1-phi)/G.nodes[node]['outB']) - (1/G.out_degree(node))



def computePPRs():
    qDict = {}
    pRlist = np.inner(Q, color)
    for node in G.nodes:
        G.nodes[node]['pR'] = pRlist[node]
        tmpDict = {}
        for n in G.nodes:
            tmpDict[n] = Q[node][n]
        qDict[node] = tmpDict
    return qDict


def cmpFormula():
    tmpGains = {}
    # ppr = computePPRs()
    pRlist = np.inner(Q, color)
    for node in G.nodes:
        G.nodes[node]['pR'] = pRlist[node]
    
    for node in lR:
        g = gamma[node][node]
        sPkR = 0
        sPkB = 0
        sPkxR = 0
        sPkxB = 0
        fTerm = g/((1-g)*(phi - (G.nodes[node]['outR'] / G.out_degree(node))))
    
        dR = 1/G.nodes[node]['outR']
        dB = 1/G.nodes[node]['outB']

        for n in G.nodes[node]['outRList']:
            sPkR += G.nodes[n]['pR']
            sPkxR += Q[n][node]
        for n in G.nodes[node]['outBList']:
            sPkB += G.nodes[n]['pR']
            sPkxB += Q[n][node]

        numerator = dR*sPkR - dB*sPkB
        denominator = fTerm-(dR*sPkxR - dB*sPkxB)
        tmpGains[node] = pr[node]*numerator/denominator
    return tmpGains



graphFile = '/out_graph.txt'
G = nx.DiGraph()
red = []
blue = []
read_community(sys.path[0] + '/out_community.txt')
nodesList = sorted(red+blue)
G.add_nodes_from(nodesList)
makeGraph(sys.path[0] + graphFile)
# G = nx.convert_node_labels_to_integers(G)

outRB()
lR = initlR()



P = nx.adjacency_matrix(G)
P = P.toarray()
row_sums = P.sum(axis=1)
P = (P / row_sums[:, np.newaxis])

where_are_NaNs = np.isnan(P)
P[where_are_NaNs] = 0

u = np.empty(len(P)) 
u.fill(1/len(P))
u = np.transpose(u)

# Handle sink nodes
d = np.zeros(len(P))

for node in G.nodes:
    if G.out_degree(node) == 0:
        d[node] = 1
P = P + np.outer(d, u)

I = np.identity(len(P))
D = np.zeros(shape=(len(P), len(P)))

# Random jump vector
v = np.empty(len(P)) 
v.fill(1/len(G.nodes))

# Vector with 1 over red nodes
color = np.zeros(len(P))
for node in red:
    color[node] = 1
    
gamma = np.zeros(len(P)) 
for node in G.nodes:
    if node in red:
        gamma[node] = gRed
    else:
        gamma[node] = gBlue
gamma = np.diag(gamma)

# intrinsic opinions
s = np.zeros(len(P))
for node in G.nodes:
    if node in red:
        s[node] = 1
    else:
        s[node] = -1



Q = (np.linalg.inv(I-((I-gamma).dot(P)))).dot(gamma)
z = Q @ s



# start_time = time.time()
results = defaultdict(lambda: {"Fairness": 0.0, "CostV": 0.0, "CostS": 0.0})

fair = np.zeros(len(P)) 

fairNodes = []
for fNodes in (range(0, len(lR) + 1)):
    # print(fNodes, "fair nodes are: ", fairNodes[:fNodes])
    Q = (np.linalg.inv(I-((I-gamma).dot(P+D)))).dot(gamma)
    zPrime = Q @ s
    c = (zPrime - z) ** 2
    results[fNodes]["CostV"] = np.sum(c)/len(G.nodes)
    # results[fNodes]["CostS"] = np.sum(c*fair)/fNodes
    results[fNodes]["CostS"] = np.sum(c*fair) / max(1, fNodes)
    pr = v.dot(Q)
    prRed = np.inner(pr, color)
    # print("PageRank allocated to red group: ", prRed)
    if len(lR) > 0:
        gains = cmpFormula()
        nFair = max(gains, key=gains.get)
        # print(nFair, gains[nFair], "-----")
        lR.remove(nFair)
        fairNodes.append(nFair)
        updateD(nFair)
        fair[nFair] = 1
    results[fNodes]["Fairness"] = prRed
# print("--- %s seconds ---" % (time.time() - start_time))


# In[13]:


data = results
keys = list(data.keys())
filtered_keys = [keys[0]] + [key for i, key in enumerate(keys[1:], start=1) if data[key]['Fairness'] >= data[keys[i-1]]['Fairness']]

results = {key: data[key] for key in filtered_keys}


# In[14]:


directory = os.getcwd()  # Replace with the desired directory path
if difGamma == 0:
    directory += '/phi=' + str(phi) + "/Results"
else:
    directory += '/phi=' + str(phi) + "/Results"+whichG+"Gammas"
# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Navigate to the directory
os.chdir(directory)


# In[15]:


if difGamma == 0:
    filename = "γ" + str(gRed) + ".csv"
else:
    filename = "γR" + str(gRed) + "_γB" + str(gBlue) + ".csv"
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Nodes", "Fairness", "CostV", "CostS"])
    for node, values in results.items():
        writer.writerow([node, values["Fairness"], values["CostV"], values["CostS"]])
