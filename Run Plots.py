import subprocess
from tqdm import tqdm
datasets = {
    'Karate': [0.75, 0.5, 0.625],
    'Books': [0.75, 0.63, 0.504],
    'Blogs': [0.75, 0.606, 0.485],
    'github_male': [0.75, 0.097, 0.078]
}

for dataset, phis in tqdm(datasets.items()):
    print("----------", dataset, phis, "----------")
    for phi in phis:
        subprocess.run(['python3', 'Make Plots.py', str(phi), dataset])
        subprocess.run(['python3', 'Make Plots Different Gammas.py', str(phi), dataset])
        # subprocess.run(['python3', 'Make Plots Weights.py', str(phi), dataset])