 jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg

# Add Docker's official GPG key
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg


# Add the repository to Apt sources
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker CE CLI, Buildx, and Compose plugin
RUN apt-get update && apt-get install -y \
    docker-ce-cli \
    docker-buildx-plugin \
    docker-compose-plugin

# Optional: Create a symbolic link if your script specifically calls 'docker-compose' 
# (Modern version is usually called via 'docker compose' without the hyphen)
# RUN ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose

USER jenkins
