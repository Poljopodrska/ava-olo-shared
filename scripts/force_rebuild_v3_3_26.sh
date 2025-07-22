#!/bin/bash
# scripts/force_rebuild_v3_3_26.sh

echo "🔨 Force Rebuilding with v3.3.26"
echo "================================"

# 1. Tag the specific commit
cd ../ava-olo-agricultural-core
git checkout 5a562ab  # The v3.3.26 commit

# 2. Verify VERSION in code
echo "Checking VERSION in main.py..."
grep "VERSION = " main.py

# 3. Build locally first to verify
echo "Building Docker image locally..."
docker build -t agricultural-core-test .

# 4. Test local build
docker run --rm agricultural-core-test python -c "import main; print(main.VERSION)"

# 5. If correct, push to ECR with specific tag
if [[ $(docker run --rm agricultural-core-test python -c "import main; print(main.VERSION)") == *"3.3.26"* ]]; then
  echo "✅ Version correct, pushing to ECR..."
  
  # Tag for ECR
  docker tag agricultural-core-test \
    127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:v3.3.26
  docker tag agricultural-core-test \
    127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:latest
  
  # Push both tags
  docker push 127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:v3.3.26
  docker push 127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:latest
  
  echo "✅ Pushed v3.3.26 to ECR"
else
  echo "❌ Version mismatch! Check main.py"
fi