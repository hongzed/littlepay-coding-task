import pandas as pd


def load_data(file):
    """Load CSV data from a file-like object.

    Args:
        file: A file-like object containing CSV data.
    Returns:
        pd.DataFrame: DataFrame containing the loaded data.
    """

    return pd.read_csv(file)


def preprocess_data(trips, products, adjustments):
    """Preprocess the datasets to prepare for visualisation.

    Args:
        trips (pd.DataFrame): DataFrame containing trip data.
        products (pd.DataFrame): DataFrame containing product data.
        adjustments (pd.DataFrame): DataFrame containing adjustment data.

    Returns:
        pd.DataFrame: merged DataFrame with additional fields for visualisation.
    """

    # Convert date fields
    trips["tap_on_date"] = pd.to_datetime(trips["tap_on_date"], errors="coerce")
    trips["tap_off_date"] = pd.to_datetime(trips["tap_off_date"], errors="coerce")
    products["created_date"] = pd.to_datetime(products["created_date"], errors="coerce")
    products["start_date_utc"] = pd.to_datetime(
        products["start_date_utc"], errors="coerce"
    )

    # Convert bool
    adjustments["applied"] = adjustments["applied"].astype(bool)

    # Merge datasets
    merged = adjustments.merge(trips, on="trip_id", how="left")
    merged = merged.merge(
        products[["id", "capping_type"]],
        left_on="product_id",
        right_on="id",
        how="left",
    ).drop(columns=["id"])

    # Genearte a new field with date only
    merged["tap_on_day"] = merged["tap_on_date"].dt.date

    return merged
