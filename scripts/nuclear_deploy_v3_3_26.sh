#!/bin/bash
# scripts/nuclear_deploy_v3_3_26.sh

echo "☢️  NUCLEAR DEPLOYMENT FORCE"
echo "==========================="

# 1. Stop all running tasks
echo "Stopping all current tasks..."
TASK_ARNS=$(aws ecs list-tasks \
  --cluster ava-olo-production \
  --service-name agricultural-core \
  --region us-east-1 \
  --query 'taskArns[]' \
  --output text)

for task in $TASK_ARNS; do
  echo "Stopping task: $task"
  aws ecs stop-task \
    --cluster ava-olo-production \
    --task $task \
    --reason "Force deployment of v3.3.26" \
    --region us-east-1
done

# 2. Update service with specific task definition
echo "Updating service with new task definition..."
aws ecs update-service \
  --cluster ava-olo-production \
  --service agricultural-core \
  --task-definition agricultural-core:9 \
  --force-new-deployment \
  --desired-count 0 \
  --region us-east-1

sleep 10

# 3. Scale back up with new task def
aws ecs update-service \
  --cluster ava-olo-production \
  --service agricultural-core \
  --desired-count 2 \
  --deployment-configuration "maximumPercent=200,minimumHealthyPercent=100" \
  --region us-east-1

echo "✅ Nuclear deployment initiated"