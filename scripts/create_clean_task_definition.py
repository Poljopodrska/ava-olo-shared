# scripts/create_clean_task_definition.py
import boto3
import json

def create_clean_task_def():
    """Create task definition without secrets issues"""
    
    ecs = boto3.client('ecs', region_name='us-east-1')
    
    # Get current task def as template
    current = ecs.describe_task_definition(
        taskDefinition='agricultural-core'
    )['taskDefinition']
    
    # Clean task definition
    new_task_def = {
        "family": "agricultural-core",
        "taskRoleArn": current.get('taskRoleArn'),
        "executionRoleArn": current.get('executionRoleArn'),
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE"],
        "cpu": "1024",
        "memory": "2048",
        "containerDefinitions": [{
            "name": "agricultural-core",
            "image": "127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo/agricultural-core:v3.3.26",
            "portMappings": [{
                "containerPort": 8000,
                "protocol": "tcp"
            }],
            "essential": True,
            "environment": [
                {"name": "PORT", "value": "8000"},
                {"name": "ENVIRONMENT", "value": "production"},
                {"name": "SERVICE_NAME", "value": "agricultural-core"}
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/agricultural-core",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs"
                }
            },
            "healthCheck": {
                "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
                "interval": 30,
                "timeout": 5,
                "retries": 3,
                "startPeriod": 60
            }
        }]
    }
    
    # Register new task definition
    response = ecs.register_task_definition(**new_task_def)
    new_revision = response['taskDefinition']['revision']
    
    print(f"✅ Created clean task definition revision: {new_revision}")
    return f"agricultural-core:{new_revision}"

if __name__ == "__main__":
    create_clean_task_def()