# This is script parses the USGS appendix data and exports it
# to csv at samples_cu.csv.

import pandas as pd
from pathlib import Path

def main():
  # Saves the current directory so running this script always uses correct path.
  CURR_DIR = Path(__file__).resolve().parent

  # Raw geochemical and mineralogical data for samples of surface soils collected from a depth of 0 to 5 centimeters in the conterminous United States.
  RAW_DATA_FILE_INPUT_PATH = CURR_DIR / ".." / ".." / "data" / "raw" / "Appendix_2b_Top5_18Sept2013.txt"

  # Csv output to generate
  CSV_OUTPUT_PATH = CURR_DIR / ".." / ".." / "data" / "samples_cu.csv"

  # Skips the commentary and legend information at the top.
  LINES_TO_SKIP = 12

  df = read_raw(RAW_DATA_FILE_INPUT_PATH, LINES_TO_SKIP)
  cleanDf = clean_samples(df)
  cleanDf.to_csv(CSV_OUTPUT_PATH, index=False)

def read_raw(path, linesToSkip) -> pd.DataFrame:
  # Creates the pandas dataframe for the provided data, tab-delimited.
  return pd.read_csv(path, sep='\t', skiprows=linesToSkip,)

def clean_samples(df) -> pd.DataFrame:
  # Drops second row (units)
  df = df.drop(index=0)

  # Preserve empty space data entries
  df = df.fillna("")

  # Strips out the unwanted headers, focusing on copper only.
  df = df[['SiteID', 'StateID', 'Latitude', 'Longitude', 'Top5_Cu']]

  # Filter out "N.S" rows in any column
  df = df[~df.astype(str).apply(lambda x: x.str.contains('N.S', na=False, regex=False)).any(axis=1)]

  # Handle data below the detection limit (<x)
  # If data is smaller than detection limit, estimate value at half the detection limit.
  # Add a column Below_Detection that reads true if this value was estimated.
  df['Below_Detection'] = df['Top5_Cu'].astype(str).str.startswith('<')
  # Cast to float so halving a whole number (<5 -> 2.5) fits the column.
  df['Top5_Cu'] = pd.to_numeric(df['Top5_Cu'].str.lstrip('<')).astype(float)
  df.loc[df['Below_Detection'], 'Top5_Cu'] /= 2

  # Convert all numerical values
  df['SiteID'] = df['SiteID'].astype(int)
  df[['Latitude', 'Longitude', 'Top5_Cu']] = df[['Latitude', 'Longitude', 'Top5_Cu']].astype(float)

  return df

if __name__ == "__main__":
  main()
