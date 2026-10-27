from pathlib import Path
import parse_raw_data as prd
import pandas as pd

TEST_DIR = Path(__file__).parent

class TestParseRawData:

  def test_invalid_data(self):
    testData = TEST_DIR / "mocks" / "mock_invalid_data.txt"
    expectedOutput = pd.DataFrame({
      "SiteID": [1, 1],
      "StateID": ["CO", "CO"],
      "Latitude": [3.0, 3.0],
      "Longitude": [4.0, 4.0],
      "Top5_Cu": [6.0, 3.0],
      "Below_Detection": [False, True]
    })
    df = prd.read_raw(testData, 12)
    
    pd.testing.assert_frame_equal(prd.clean_samples(df).reset_index(drop=True), expectedOutput)

  def test_low_detection_limit(self):
    testData = TEST_DIR / "mocks" / "mock_low_detection_data.txt"
    expectedOutput = pd.DataFrame({
      "SiteID": [1, 1, 1, 1, 1],
      "StateID": ["AL", "CO", "CO", "CO", "CA"],
      "Latitude": [3.0, 3.0, 3.0, 3.0, 3.0],
      "Longitude": [4.0, 4.0, 4.0, 4.0, 4.0],
      "Top5_Cu": [3.0, 6.0, 6.0, 3.0, 2.5],
      "Below_Detection": [True, False, False, True, True]
    })
    df = prd.read_raw(testData, 12)
    
    pd.testing.assert_frame_equal(prd.clean_samples(df).reset_index(drop=True), expectedOutput)