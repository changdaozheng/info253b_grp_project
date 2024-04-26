#!/bin/bash

IMAGE_NAME="info253bgrp"
TAG="latest"

docker build -t ${IMAGE_NAME}:${TAG} .