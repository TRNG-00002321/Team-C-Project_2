# FROM jenkins/jenkins:lts

# USER root

# RUN apt-get update && apt-get install -y \
#     ca-certificates \
#     curl \
#     gnupg

# # Add Docker's official GPG key
# RUN mkdir -p /etc/apt/keyrings
# RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg


# # Add the repository to Apt sources
# RUN echo \
#   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
#   $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
#   tee /etc/apt/sources.list.d/docker.list > /dev/null

# # Install Docker CE CLI, Buildx, and Compose plugin
# RUN apt-get update && apt-get install -y \
#     docker-ce-cli \
#     docker-buildx-plugin \
#     docker-compose-plugin

# # Optional: Create a symbolic link if your script specifically calls 'docker-compose' 
# # (Modern version is usually called via 'docker compose' without the hyphen)
# # RUN ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose

# USER jenkins

FROM jenkins/jenkins:lts

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
    docker-compose-plugin \
    wget \
    sudo
# Install dependencies
# Base dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \    
    libc-bin \
    dnsutils \
    ca-certificates \
    unzip \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libgtk-3-0 \
    curl \
    libu2f-udev \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*



# Create keyrings directory
RUN mkdir -p /etc/apt/keyrings

# Add Google Chrome signing key (modern way)
RUN wget -q -O /etc/apt/keyrings/google-chrome.gpg \
    https://dl.google.com/linux/linux_signing_key.pub

# Edge key
RUN wget -q -O /etc/apt/keyrings/microsoft-edge.gpg \
    https://packages.microsoft.com/keys/microsoft.asc

# Add Chrome repository
RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] \
    http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft-edge.gpg] \
    https://packages.microsoft.com/repos/edge stable main" \
    > /etc/apt/sources.list.d/microsoft-edge.list


# Install browsers
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    firefox-esr \
    microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

# Install matching EdgeDriver
RUN curl -Lo /tmp/edgedriver.zip "https://msedgedriver.microsoft.com/144.0.3719.82/edgedriver_linux64.zip" && \
    unzip /tmp/edgedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/msedgedriver && \
    rm -rf /tmp/edgedriver.zip

#crate volume folder
RUN mkdir -p /data && chown jenkins /data

RUN chown jenkins /data
RUN chmod -R 777 /data

USER jenkins
