import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

phi = float(sys.argv[1])  # Get phi value from command-line argument
dataset = sys.argv[2]  # Get dataset value from command-line argument

# Directory paths
save_directory = f'Plots/{dataset}/phi={phi}'
os.makedirs(save_directory, exist_ok=True)

subdirectory_red = os.path.join(dataset, 'phi=' + str(phi), 'ResultsRedGammas')
subdirectory_blue = os.path.join(dataset, 'phi=' + str(phi), 'ResultsBlueGammas')

# Create a new directory called "Different Gammas" inside the main save directory
save_directory_diffgammas = os.path.join(save_directory, 'Different Gammas')
os.makedirs(save_directory_diffgammas, exist_ok=True)

# Get a list of all CSV files in the red subdirectory
file_list_red = [file for file in os.listdir(os.path.join(os.getcwd(), subdirectory_red)) if file.endswith('.csv')]
file_list_red.sort(key=lambda x: float(x.split('γR')[1].split('_')[0]) if 'γR' in x else float('inf'))

# Get a list of all CSV files in the blue subdirectory
file_list_blue = [file for file in os.listdir(os.path.join(os.getcwd(), subdirectory_blue)) if file.endswith('.csv')]
file_list_blue.sort(key=lambda x: float(x.split('γB')[1].split('.csv')[0]) if 'γB' in x else float('inf'))

# Initialize lists to store data and legends
data_red = []
data_blue = []
legends_red = []
legends_blue = []

# Define marker styles
marker_styles = ['s', 'o', '^', 'd', 'v']

# Read CSV files and extract data for red gammas
for idx, file in enumerate(file_list_red):
    file_path = os.path.join(os.getcwd(), subdirectory_red, file)
    df = pd.read_csv(file_path)
    data_red.append(df[['Fairness', 'CostV', 'CostS']])
    legends_red.append(file.replace('.csv', ''))

# Read CSV files and extract data for blue gammas
for idx, file in enumerate(file_list_blue):
    file_path = os.path.join(os.getcwd(), subdirectory_blue, file)
    df = pd.read_csv(file_path)
    data_blue.append(df[['Fairness', 'CostV', 'CostS']])
    legends_blue.append(file.replace('.csv', ''))

# Plot the data for red gammas
for i, column in enumerate(['Fairness', 'CostV', 'CostS']):
    plt.figure(figsize=(10, 6))
    for idx, d in enumerate(data_red):
        marker_style = marker_styles[idx % len(marker_styles)]
        plt.plot(d[column], label=legends_red[idx], marker=marker_style, markevery=10)
    if column == 'Fairness':
        plt.axhline(y=phi, color='r', linestyle='--', label=f'phi = {phi}')
    plt.xlabel('Nodes')
    plt.ylabel(column)
    plt.title(f'{dataset} - gRed Increases - {column}')
    plt.legend(loc='best')
    save_path_red = os.path.join(save_directory_diffgammas, f'Red_{column}.png')
    plt.savefig(save_path_red)
    # plt.show()

# Plot the data for blue gammas
for i, column in enumerate(['Fairness', 'CostV', 'CostS']):
    plt.figure(figsize=(10, 6))
    for idx, d in enumerate(data_blue):
        marker_style = marker_styles[idx % len(marker_styles)]
        plt.plot(d[column], label=legends_blue[idx], marker=marker_style, markevery=10)
    if column == 'Fairness':
        plt.axhline(y=phi, color='r', linestyle='--', label=f'phi = {phi}')
    plt.xlabel('Nodes')
    plt.ylabel(column)
    plt.title(f'{dataset} - gBlue Increases - {column}')
    plt.legend(loc='best')
    save_path_blue = os.path.join(save_directory_diffgammas, f'Blue_{column}.png')
    plt.savefig(save_path_blue)
    # plt.show()
