#!/bin/bash
set -e
sudo chmod -R a+rw /dev/bus/usb
sudo adb kill-server || true
docker compose up -d --build
