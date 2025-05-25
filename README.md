# Capping Product Visualisation App

This Streamlit app allows you to upload and analyse transportation fare capping datasets. It provides interactive insights and visualisations related to capping products, such as daily/weekly caps and fare adjustments.

## Summary

- Upload and preview three datasets: **Trips**, **Products**, and **Adjustments**
- Interactive filters for:
  - Date range
  - Service type
  - Direction
  - Trip completion status
- Visualisations:
  - Daily transaction volume
  - Original vs Adjusted fare comparisons
  - Popularity of capping types

## Quickstart

### Prerequisites

- Python 3.8 or newer
- `pip` package manager
- Docker desktop

1. Install dependencies and run the app

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```

The app will be available at http://localhost:8501

2. Run with Docker

```bash
docker-compose up
```

Access the app at: http://localhost:8501

## Repo Structure

```bash
.
├── app.py                # Main Streamlit application
├── Dockerfile            # Docker build instructions
├── docker-compose.yml    # Docker Compose config
├── requirements.txt      # Python dependencies
└── README.md             # You're here!
```
