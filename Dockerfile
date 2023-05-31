FROM python:3.8-slim-buster

# Expose the Streamlit port
EXPOSE 8501

WORKDIR /app

# Install system level dependencies
RUN apt-get update && apt-get install apt-transport-https ffmpeg libsm6 libxext6 -y
RUN apt-get update && apt-get install -y libdmtx0b

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application files
COPY . .

# Start the Streamlit server
CMD ["streamlit", "run", "Main.py"]
