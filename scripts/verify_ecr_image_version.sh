#!/bin/bash
# scripts/verify_ecr_image_version.sh

echo "🔍 Verifying ECR Image Version"
echo "=============================="

# 1. Pull the latest image locally to check
echo "Logging into ECR..."
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 127679825789.dkr.ecr.us-east-1.amazonaws.com

# 2. Pull the latest image
echo "Pulling latest image..."
docker pull 127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:latest

# 3. Run the image and check version
echo "Checking version in image..."
docker run --rm \
  127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:latest \
  python -c "import main; print(f'VERSION IN IMAGE: {main.VERSION}')"

# 4. Also check by starting the container and hitting version endpoint
echo "Starting container to test..."
docker run -d --name version-test -p 8001:8000 \
  127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:latest

sleep 5
curl http://localhost:8001/version
docker stop version-test && docker rm version-test