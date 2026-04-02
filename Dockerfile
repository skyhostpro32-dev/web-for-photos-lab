FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for faster builds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port (optional but good practice)
EXPOSE 8501

# Start Streamlit using Render's dynamic PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
