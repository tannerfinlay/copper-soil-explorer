from pathlib import Path

import ingest as ing
import pandas as pd

TEST_DIR = Path(__file__).parent

class TestIngest:

  def test_invalid_data(self):
    testData = TEST_DIR / "mocks" / "mock_invalid_data.txt"

    expectedOutput = pd.DataFrame({
      "SiteID": ['1', '1'],
      "StateID": ["CO", "CO"],
      "Latitude": [3.0, 3.0],
      "Longitude": [4.0, 4.0],
      "Top5_Cu": [6.0, 3.0],
      "Below_Detection": [False, True]
    })
    df = ing.read_raw(testData, 12)
    
    pd.testing.assert_frame_equal(ing.clean_samples(df).reset_index(drop=True), expectedOutput)

  def test_low_detection_limit(self):
    testData = TEST_DIR / "mocks" / "mock_low_detection_data.txt"

    expectedOutput = pd.DataFrame({
      "SiteID": ['1', '1', '1', '1', '1'],
      "StateID": ["AL", "CO", "CO", "CO", "CA"],
      "Latitude": [3.0, 3.0, 3.0, 3.0, 3.0],
      "Longitude": [4.0, 4.0, 4.0, 4.0, 4.0],
      "Top5_Cu": [3.0, 6.0, 6.0, 3.0, 2.5],
      "Below_Detection": [True, False, False, True, True]
    })
    df = ing.read_raw(testData, 12)
    
    pd.testing.assert_frame_equal(ing.clean_samples(df).reset_index(drop=True), expectedOutput)

  def test_create_json_payload(self):
    testData = pd.DataFrame({
      "SiteID": ['1', '1'],
      "StateID": ["CO", "CO"],
      "Latitude": [3.0, 3.0],
      "Longitude": [4.0, 4.0],
      "Top5_Cu": [6.0, 3.0],
      "Below_Detection": [False, True]
    })

    expectedOutput = {
      "element": "cu",
      "units": "mg/kg",
      "samples": [
        {
          "id": '1',
          "state": "CO",
          "lat": 3.0,
          "lon": 4.0,
          "value": 6.0,
          "belowDetection": False
        },
        {
          "id": '1',
          "state": "CO",
          "lat": 3.0,
          "lon": 4.0,
          "value": 3.0,
          "belowDetection": True
        }
      ]
    }

    assert ing.create_json_payload(testData) == expectedOutput