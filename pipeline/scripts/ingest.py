# This is script parses the USGS appendix data and exports it
# to csv and json payload as samples_cu.

import json
import logging
from pathlib import Path

import pandas as pd

# Logging function
logger = logging.getLogger(__name__)

def main():
  logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
  # Saves the current directory so running this script always uses correct path.
  CURR_DIR = Path(__file__).resolve().parent

  # Raw geochemical and mineralogical data for samples of surface soils collected from a depth of 0 to 5 centimeters in the conterminous United States.
  RAW_DATA_FILE_NAME = "Appendix_2b_Top5_18Sept2013.txt"
  RAW_DATA_FILE_INPUT_PATH = CURR_DIR / ".." / ".." / "data" / "raw" / RAW_DATA_FILE_NAME

  # Csv output to generate
  CSV_OUTPUT_PATH = CURR_DIR / ".." / ".." / "data" / "samples_cu.csv"

  # Json output to generate
  JSON_OUTPUT_PATH = CURR_DIR / ".." / ".." / "data" / "samples_cu.json"

  # Skips the commentary and legend information at the top.
  LINES_TO_SKIP = 12

  logger.info('Parsing %s', RAW_DATA_FILE_NAME)

  df = read_raw(RAW_DATA_FILE_INPUT_PATH, LINES_TO_SKIP)
  total_rows_read = len(df)
  logger.info('Read %d rows', total_rows_read)
  cleanDf = clean_samples(df)
  logger.info('Dropped %d invalid rows', total_rows_read - len(cleanDf))
  # Output csv
  cleanDf.to_csv(CSV_OUTPUT_PATH, index=False)

  # Output json
  json_output = create_json_payload(cleanDf)

  # Write to json output
  with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=4)

  logger.info('Finished generating data/samples_cu.csv and data/samples_cu.json')

# Creates the pandas dataframe for the provided data, tab-delimited.
def read_raw(path, linesToSkip) -> pd.DataFrame:
  df = pd.read_csv(path, sep='\t', skiprows=linesToSkip,)
  # Drops second row (units)
  df = df.drop(index=0)
  return df

# Drops invalid rows, unit row, unwanted headers.
def clean_samples(df) -> pd.DataFrame:


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

  below_detection_count = (df['Below_Detection'] == True).sum()
  logger.info('%d rows below detection limits, values set to half the limit', below_detection_count)

  # Convert all numerical values
  df['SiteID'] = df['SiteID'].astype(str)
  df[['Latitude', 'Longitude', 'Top5_Cu']] = df[['Latitude', 'Longitude', 'Top5_Cu']].astype(float)

  return df

def create_json_payload(df) -> dict:
  # Rename columns to js camelcase
  new_df = df.rename(columns={'SiteID': 'id', 'StateID': 'state', 'Latitude': 'lat', 'Longitude': 'lon', 'Top5_Cu': 'value', 'Below_Detection': 'belowDetection'})

  # Create list of dicts
  list_of_dicts = new_df.to_dict(orient='records')

  # Wrap sample data with header information
  return {
    "element": "cu",
    "units": "mg/kg",
    "samples": list_of_dicts
  }

if __name__ == "__main__":
  main()
