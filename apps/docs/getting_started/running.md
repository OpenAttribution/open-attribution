If you're testing or developing make sure to start environments:
`sudo ./launcher.sh`


## Docker: Running OpenAttribution

Follow these steps to start locally:

```sh
# Get the code
git clone --depth 1 https://github.com/OpenAttribution/open-attribution

# Go to the docker folder
cd open-attribution/docker

# Copy the fake env vars
cp .env.example .env

# Pull the latest images
docker compose pull

# Start the services (in detached mode)
docker compose up -d

```