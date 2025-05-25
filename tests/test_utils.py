import os
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.utils import load_data, preprocess_data


def test_load_data(tmp_path):
    file = tmp_path / "sample.csv"
    file.write_text("a,b\n1,2\n3,4")
    df = load_data(str(file))
    assert not df.empty
    assert list(df.columns) == ["a", "b"]


def test_preprocess_data():
    trips = pd.DataFrame(
        {
            "trip_id": [1],
            "tap_on_date": ["2024-01-01"],
            "tap_off_date": ["2024-01-01"],
            "original_amount": [10],
            "adjusted_amount": [8],
            "service_type": ["bus"],
            "direction": ["north"],
            "trip_completion": ["complete"],
        }
    )

    products = pd.DataFrame(
        {
            "id": [100],
            "capping_type": ["DAILY"],
            "created_date": ["2024-01-01"],
            "start_date_utc": ["2024-01-01"],
        }
    )

    adjustments = pd.DataFrame({"trip_id": [1], "product_id": [100], "applied": [True]})

    result = preprocess_data(trips, products, adjustments)
    assert result.shape[0] == 1
