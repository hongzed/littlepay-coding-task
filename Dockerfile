# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only necessary files first (for better Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Run the app
CMD ["streamlit", "run", "app.py"]
