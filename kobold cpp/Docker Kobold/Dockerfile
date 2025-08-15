# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    aria2 \
    python3 \
    python3-pip

# Set working directory
WORKDIR /app

# Copy your application code
COPY app.py .

# Download KoboldCpp
RUN wget -O dlfile.tmp https://kcpplinux.concedo.workers.dev && \
    mv dlfile.tmp koboldcpp_linux && \
    chmod +x ./koboldcpp_linux

# Install Python dependencies (if any)
# RUN pip3 install -r requirements.txt

# Download models
RUN python3 app.py

# Expose the port your application runs on
EXPOSE 5001

# Command to run your application
CMD ["./koboldcpp_linux", "model.gguf", "--multiuser", "--usecublas", "0", "mmq", "--contextsize", "4096", "--gpulayers", "999", "--quiet", "--tensor_split", "1", "1"]
