import pandas as pd
import streamlit as st
from utils import load_data
from utils import preprocess_data

st.set_page_config(page_title="Capping Product Visualisation", layout="wide")

# Set the lannding page
if "page" not in st.session_state:
    st.session_state.page = "Upload & Preview"

# Set the page navigation
page = st.sidebar.radio(
    "Choose a page",
    ["Upload & Preview", "Capping Visualisation"],
    index=["Upload & Preview", "Capping Visualisation"].index(st.session_state.page),
)
st.session_state.page = page


def main():

    # Initialize session state for datasets
    if page == "Upload & Preview":
        st.header("Upload and Preview Datasets")

        trips_file = st.file_uploader("Upload Trips CSV", type="csv")
        products_file = st.file_uploader("Upload Products CSV", type="csv")
        adjustments_file = st.file_uploader("Upload Adjustments CSV", type="csv")

        if trips_file and products_file and adjustments_file:
            st.session_state.trips = load_data(trips_file)
            st.session_state.products = load_data(products_file)
            st.session_state.adjustments = load_data(adjustments_file)

            st.subheader("Trips Preview")
            st.dataframe(st.session_state.trips.head())

            st.subheader("Products Preview")
            st.dataframe(st.session_state.products.head())

            st.subheader("Adjustments Preview")
            st.dataframe(st.session_state.adjustments.head())

            st.success("Data loaded and previewed successfully.")

            st.session_state.merged = preprocess_data(
                st.session_state.trips,
                st.session_state.products,
                st.session_state.adjustments,
            )

            st.subheader("Merged Preview (after preprocessing)")
            st.dataframe(st.session_state.merged.head())

    else:
        # Render the visualisation page
        st.header("Capping Product Visualisation")

        if "merged" not in st.session_state:
            st.warning(
                "Please upload and preview the datasets first on the 'Upload & Preview' page."
            )
            return

        merged = st.session_state.merged

        st.sidebar.subheader("Filters")

        start_date = st.sidebar.date_input("Start Date", merged["tap_on_date"].min())
        end_date = st.sidebar.date_input("End Date", merged["tap_on_date"].max())

        # Convert date inputs to datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        service_filter = st.sidebar.multiselect(
            "Service Type", merged["service_type"].dropna().unique()
        )
        direction_filter = st.sidebar.multiselect(
            "Direction", merged["direction"].dropna().unique()
        )
        completion_filter = st.sidebar.multiselect(
            "Trip Completion", merged["trip_completion"].dropna().unique()
        )

        filtered = merged[
            (merged["tap_on_date"] >= start_date) & (merged["tap_on_date"] <= end_date)
        ].copy()

        if service_filter:
            filtered = filtered[filtered["service_type"].isin(service_filter)]
        if direction_filter:
            filtered = filtered[filtered["direction"].isin(direction_filter)]
        if completion_filter:
            filtered = filtered[filtered["trip_completion"].isin(completion_filter)]

        daily_stats = (
            filtered.groupby("tap_on_day")
            .agg(
                trip_count=("trip_id", "nunique"),
                total_original=("original_amount", "sum"),
                total_adjusted=("adjusted_amount", "sum"),
                total_savings=("adjustment_amount", "sum"),
            )
            .reset_index()
        )

        # 1. Transaction Volume per Day
        st.subheader("Transaction Volume per Day")
        st.bar_chart(daily_stats.set_index("tap_on_day")["trip_count"])

        # 2. Total Original, Adjusted, and Savings Amounts per Day
        st.subheader("Original vs Adjusted vs Savings (Bar Chart)")
        chart_data = daily_stats.set_index("tap_on_day")[
            ["total_original", "total_adjusted", "total_savings"]
        ]
        st.bar_chart(chart_data)

        st.subheader("Original vs Adjusted vs Savings (Line Chart)")
        st.line_chart(chart_data)

        # 3. Volume by capping type, Daily vs. Weekly product
        st.subheader("Popularity of Capping Type")
        capping_stats = (
            filtered.groupby("capping_type")["trip_id"].nunique().reset_index()
        )
        capping_stats = capping_stats.rename(columns={"trip_id": "trip_count"})
        st.bar_chart(capping_stats.set_index("capping_type")["trip_count"])


if __name__ == "__main__":
    main()
