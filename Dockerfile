FROM ubuntu:latest

# Add the CURL and SUDO Commands
RUN apt-get update && \
    apt-get install -y curl sudo

# Install GitHub Actions runner
RUN mkdir actions-runner && \
    cd actions-runner && \
    curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz && \
    tar xzf ./actions-runner-linux-x64.tar.gz && \
    ./bin/installdependencies.sh

# Create a directory in the container
WORKDIR /app

# Copy the whole project manually inside the virtual environment
COPY . /app

CMD ["bash"]