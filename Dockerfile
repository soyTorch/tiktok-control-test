FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    udev \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
