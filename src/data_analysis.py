import pandas as pd
import matplotlib.pyplot as plt

# Load the simulation results
df = pd.read_csv("simulation_results.csv")

# Filter out the averages row if it exists
df = df[df["winner"] != "Average"]

# Ensure total_stuck_events is treated as integers
df["total_stuck_events"] = df["total_stuck_events"].astype(int)

# Create the histogram for total_stuck_events
bins_stuck = range(int(df["total_stuck_events"].min()), int(df["total_stuck_events"].max()) + 2)  # Integer bins
plt.hist(df["total_stuck_events"], bins=bins_stuck, edgecolor='black', align='left')

# Add labels and title for total stuck events
plt.xlabel("Total Stuck Events")
plt.ylabel("Frequency")
plt.title("Histogram of Total Stuck Events in Simulated Games")

# Display the histogram for total stuck events
plt.show()

# Create the histogram for average rounds between stuck events
if "average_rounds_between_stuck" in df.columns:
    plt.hist(df["average_rounds_between_stuck"], bins=10, edgecolor='black')

    # Add labels and title for average rounds between stuck events
    plt.xlabel("Average Rounds Between Stuck Events")
    plt.ylabel("Frequency")
    plt.title("Histogram of Average Rounds Between Stuck Events")

    # Display the histogram for average rounds between stuck events
    plt.show()
