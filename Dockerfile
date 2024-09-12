
# Use Python 3.10 as the base image:
FROM python:3.10-slim

# Set the working directory inside the container:
WORKDIR /app/pyblog

# Copy the "requirements.txt" file into the container:
COPY requirements.txt requirements.txt

# Install all the dependencies in the "requirements.txt" file:
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container:
COPY . .

# Make the startup script executable:
RUN chmod +x start.sh

# Expose port 5000:
EXPOSE 5000

# Run the startup script:
CMD ["./start.sh"]


