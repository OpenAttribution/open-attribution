ARG ubuntu_release=22.04
ARG python_version=3.11.7
FROM ubuntu:${ubuntu_release} as base
FROM python:${python_version}

# Create and activate a Python virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"



# Set the working directory
WORKDIR /app


# Copy only the necessary files to the working directory
COPY . /app/
# Install the requirements
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the app with the Litestar CLI
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]


