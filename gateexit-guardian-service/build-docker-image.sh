#!/bin/bash
VERSION="0.0.2"
APP="gateexit-guardian-service"
ACCOUNT="pkalkman"
docker buildx build --platform linux/amd64,linux/arm64 -f ./Dockerfile -t $ACCOUNT/$APP:$VERSION --push .
