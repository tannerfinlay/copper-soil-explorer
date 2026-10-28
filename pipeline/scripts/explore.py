from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    # Saves the current directory so running this script always uses correct path.
    CURR_DIR = Path(__file__).resolve().parent
    DATA_FILE_NAME = "samples_cu.csv"
    DATA_FILE_INPUT_PATH = CURR_DIR / ".." / ".." / "data" / DATA_FILE_NAME
    OUTPUT_FIGURE_PATH = CURR_DIR / ".." / "figures" / "cu_histograms.png"
    df = pd.read_csv(DATA_FILE_INPUT_PATH)

    # Going to plot copper
    data_column = df["Top5_Cu"]
    print(df["Top5_Cu"].describe())

    # Create window
    plt.figure(figsize=(12, 5))

    # Plot 1 (left): Top5_Cu
    plt.subplot(1, 2, 1)
    plt.hist(data_column)
    plt.title("Top5_Cu")
    plt.xlabel("Values (mg/kg)")
    plt.ylabel("Frequency")

    # Plot 2 (right): log10(Top5_Cu)
    plt.subplot(1, 2, 2)
    plt.hist(np.log10(data_column))
    plt.title("log10(Top5_Cu)")
    plt.xlabel("Values (mg/kg)")
    plt.ylabel("Frequency")

    # Save plots
    plt.savefig(OUTPUT_FIGURE_PATH)


if __name__ == "__main__":
    main()
