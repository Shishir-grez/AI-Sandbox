# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to prevent prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean
