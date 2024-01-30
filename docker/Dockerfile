ARG ubuntu_release=22.04
ARG python_version=3.11.7
FROM ubuntu:${ubuntu_release} as base
FROM python:${python_version}

# Create and activate a Python virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install the requirements
RUN pip install --no-cache-dir --upgrade uvicorn==0.27.0.post1 "litestar[standard]"==2.5.3 apache-superset==3.1.0 confluent_kafka==2.3.0 clickhouse_connect==0.7.0

# Copy only the necessary files to the working directory
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

RUN python /app/create_clickhouse_tables.py

# Run the app with the Litestar CLI
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]


