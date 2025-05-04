# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    cmake \
    g++ \
    make \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install dlib
RUN pip install --no-cache-dir dlib

# Copy application code
COPY . /app/

# Expose Streamlit port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "IPP.py", "--server.port=8501", "--server.address=0.0.0.0"]
