# Use an official lightweight Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy app directory
COPY ./app /app

# install additional dependencies in docker base image
RUN apt-get update && apt-get install --no-install-recommends -y \
    wget \
    tar \
    xz-utils \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libasound2 \
    libnss3 \
    libglib2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and extract Firefox 139 (Linux 64-bit) into /app/firefox139Linux
#  RUN wget -O firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-142.0.1&os=linux64&lang=en-US" && \
#      mkdir -p /firefox139Linux && \
#      tar -xjf firefox.tar.bz2 -C /firefox139Linux && \
#      rm firefox.tar.bz2
RUN wget -O firefox.tar.xz "https://download.mozilla.org/?product=firefox-142.0.1&os=linux64&lang=en-US" && \
    mkdir -p /app/firefox_browser_binary && \
    tar -xf firefox.tar.xz -C /app/firefox_browser_binary && \
    rm firefox.tar.xz



# Install Selenium
RUN pip3 install -r requirements.txt

# Run the script
CMD ["python", "YT_Summarizer_Final_with_tracking.py"]
