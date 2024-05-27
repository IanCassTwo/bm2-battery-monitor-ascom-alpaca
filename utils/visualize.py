import csv
import matplotlib.pyplot as plt
import sys
from datetime import datetime

def plot_from_csv(filename, output_file=None):
    # Initialize lists to store the data
    timestamps = []
    voltages = []

    # Read the CSV file
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        # Skip the header
        next(csv_reader)
        for row in csv_reader:
            if not row:
                continue
            try:
                timestamp = float(row[0])
                voltage = float(row[1])

                if voltage == 0:
                    continue

                timestamps.append(timestamp)
                voltages.append(voltage)

            except ValueError:
                # Skip lines with invalid data
                continue

    # Convert timestamps to datetime objects for subtitle
    start_time = datetime.utcfromtimestamp(timestamps[0]).strftime('%Y/%m/%d %H:%M')
    end_time = datetime.utcfromtimestamp(timestamps[-1]).strftime('%Y/%m/%d %H:%M')

    # Initialize the figure
    plt.figure()

    # Plot the data
    plt.plot(timestamps, voltages, label='Voltage over Time')

    # Add labels and a legend
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.title(f'Voltage vs. Time\nStart Time: {start_time}  End Time: {end_time}')
    plt.grid(True)
    plt.legend()
    plt.xticks([])

    # Save the plot to disk if output_file is provided
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <filename> [output_file]")
        sys.exit(1)
    filename = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    plot_from_csv(filename, output_file)
