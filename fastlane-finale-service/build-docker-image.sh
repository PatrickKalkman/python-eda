#!/bin/bash
VERSION="0.0.10"
APP="fastlane-finale-service"
ACCOUNT="pkalkman"
docker buildx build --platform linux/amd64,linux/arm64 -f ./Dockerfile -t $ACCOUNT/$APP:$VERSION --push .
