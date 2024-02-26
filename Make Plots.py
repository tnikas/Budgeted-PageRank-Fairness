import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Directory paths
phi = float(sys.argv[1])  # Get phi value from command-line argument
dataset = sys.argv[2]  # Get dataset value from command-line argument

sub_directory = f'{dataset}/phi={phi}'
results_dir = 'Results'
save_directory = f'Plots/{dataset}/phi={phi}'

# Get a list of all CSV files in the subdirectory
csv_files = [f for f in os.listdir(os.path.join(os.getcwd(), sub_directory, results_dir)) if f.endswith(".csv")]

# Sort the csv_files list based on the γ values
csv_files.sort(key=lambda x: float(x.split("γ")[1].split(".csv")[0]))

# Initialize a dictionary to store the data
data = {}

# Read and process each CSV file
for csv_file in csv_files:
    # Extract the γ value from the file name
    gamma = float(csv_file.split("γ")[1].split(".csv")[0])
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(os.path.join(os.getcwd(), sub_directory, results_dir, csv_file))
    
    # Store the DataFrame in the data dictionary using γ value as key
    data[gamma] = df

# Plot the Fairness data
plt.figure(figsize=(10, 6))
marker_styles = ['s', 'o', '^', 'd', 'v']

for idx, (gamma, df) in enumerate(data.items()):
    label = csv_files[idx].replace(".csv", "")
    plt.plot(df['Nodes'], df['Fairness'], label=label, marker=marker_styles[idx % len(marker_styles)], markevery=10, linewidth=1)

plt.axhline(y=phi, color='r', linestyle='--', label='phi')
plt.xlabel('Fair Nodes')
plt.ylabel('Fairness')
plt.title('Fairness vs. Fair Nodes')
plt.legend(loc='best')
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=6)

os.makedirs(save_directory, exist_ok=True)
save_path = os.path.join(save_directory, "Fairness.png")
plt.savefig(save_path)
# plt.show()

# Plot the CostV data
plt.figure(figsize=(10, 6))

for idx, (gamma, df) in enumerate(data.items()):
    label = csv_files[idx].replace(".csv", "")
    plt.plot(df['Nodes'], df['CostV'], label=label, marker=marker_styles[idx % len(marker_styles)], markevery=10, linewidth=1)

plt.xlabel('Fair Nodes')
plt.ylabel('CostV')
plt.title('CostV vs. Fair Nodes')
plt.legend(loc='best')
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=6)

save_path = os.path.join(save_directory, "CostV.png")
plt.savefig(save_path)
# plt.show()

# Plot the CostS data
plt.figure(figsize=(10, 6))

for idx, (gamma, df) in enumerate(data.items()):
    label = csv_files[idx].replace(".csv", "")
    plt.plot(df['Nodes'], df['CostS'], label=label, marker=marker_styles[idx % len(marker_styles)], markevery=10, linewidth=1)

plt.xlabel('Fair Nodes')
plt.ylabel('CostS')
plt.title('CostS vs. Fair Nodes')
plt.legend(loc='best')
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=6)

save_path = os.path.join(save_directory, "CostS.png")
plt.savefig(save_path)
# plt.show()

double_axis_directory = os.path.join(save_directory, 'Fairness_Cost')
os.makedirs(double_axis_directory, exist_ok=True)

for gamma, df in data.items():
    # Creating the figure and axes with larger size
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotting the Fairness data on the left y-axis
    ax1.plot(df['Nodes'], df['Fairness'], color='blue')
    ax1.set_ylabel('Fairness', color='blue')

    # Creating a second y-axis
    ax2 = ax1.twinx()

    # Plotting the CostV data on the right y-axis
    ax2.plot(df['Nodes'], df['CostV'], color='red')
    ax2.set_ylabel('CostV', color='red')

    # Setting the x-axis label
    ax1.set_xlabel('Fair Nodes')

    # Adding the title
    plt.title(f'Gamma: {gamma}')

    # Save the plot
    save_path = os.path.join(double_axis_directory, f"Gamma_{gamma}.png")
    plt.savefig(save_path)

    # Display the plot
    # plt.show()
