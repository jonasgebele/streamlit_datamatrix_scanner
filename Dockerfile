FROM python:3.9

# Install system level dependencies
RUN apt-get update -y
RUN apt-get install -y libdmtx0a

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application files
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Start the Streamlit server
CMD ["streamlit", "run", "Main.py"]
