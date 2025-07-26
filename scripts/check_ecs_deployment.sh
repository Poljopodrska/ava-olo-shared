#!/bin/bash
echo "Checking ECS deployment status..."
echo "================================="

# Check service status
aws ecs describe-services \
  --cluster ava-olo-production \
  --services ava-agricultural-task \
  --query 'services[0].{Status:status,DesiredCount:desiredCount,RunningCount:runningCount,PendingCount:pendingCount,Deployments:deployments[*].{Status:status,TaskDef:taskDefinition,DesiredCount:desiredCount,RunningCount:runningCount}}' \
  --output json | jq .

echo -e "\nChecking latest task definition..."
LATEST_TASK=$(aws ecs describe-services --cluster ava-olo-production --services ava-agricultural-task --query 'services[0].taskDefinition' --output text)
echo "Latest task definition: $LATEST_TASK"

echo -e "\nChecking CodeBuild status..."
aws codebuild list-builds-for-project \
  --project-name ava-olo-agricultural-core-build \
  --max-items 1 \
  --query 'ids[0]' \
  --output text | xargs -I {} aws codebuild batch-get-builds --ids {} --query 'builds[0].{Status:buildStatus,StartTime:startTime}' --output json | jq .