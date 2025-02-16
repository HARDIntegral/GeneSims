# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /src

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

ENV FLASK_APP=src/gene_sim.py

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
