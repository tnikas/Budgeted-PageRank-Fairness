import subprocess

# Define the parameter values
phi_values = [0.75, 0.625, 0.5]
g_values = [0.05, 0.15, 0.3, 0.45, 0.6, 0.75]
difGammas = [0, 1]
whichG = ["Red", "Blue"]

# Loop through the parameter combinations
for phi in phi_values:
    for difGamma in difGammas:
        if difGamma == 0:
            for g in g_values:
                gRed = g
                gBlue = g
                # Call the Dynamic Formula script with the current parameters
                subprocess.run(['python3', 'Dynamic Formula.py', str(phi), str(gRed), str(gBlue), str(difGamma), "None"])
        elif difGamma == 1:
            for wg in whichG:
                for g in g_values:
                    if wg == "Red":
                        gRed = g
                        gBlue = 0.15
                    elif wg == "Blue":
                        gRed = 0.15
                        gBlue = g
                    # Call the Dynamic Formula script with the current parameters
                    subprocess.run(['python3', 'Dynamic Formula.py', str(phi), str(gRed), str(gBlue), str(difGamma), wg])
