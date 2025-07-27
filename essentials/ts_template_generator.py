#!/usr/bin/env python3
"""
Task Specification Template Generator
Automatically includes mandatory git push unless explicitly excluded
"""

def generate_ts_template(
    feature_name: str, 
    description: str, 
    goal: str,
    success_criteria: list[str],
    requirements: list[str],
    context: dict,
    implementation_approach: str,
    include_git_push: bool = True,  # Default is TRUE
    version: str = "X.X.X"
) -> str:
    """Generate a complete TS with automatic git push inclusion"""
    
    # Build success criteria
    criteria_text = "\n".join(f"- [ ] {criterion}" for criterion in success_criteria)
    
    # Build requirements
    requirements_text = "\n".join(f"{i+1}. {req}" for i, req in enumerate(requirements))
    
    # Build context
    context_text = "\n".join(f"- {key}: {value}" for key, value in context.items())
    
    template = f"""TS - TASK SPECIFICATION FOR CLAUDE CODE
FEATURE: {feature_name}
MANGO TEST: {description}

GOAL:
- {goal}

SUCCESS CRITERIA:
{criteria_text}
- [ ] Version {version} deployed and verified
- [ ] All tests pass before deployment

REQUIREMENTS:
{requirements_text}

CONTEXT:
{context_text}

IMPLEMENTATION APPROACH:
{implementation_approach}
"""
    
    # Git push is now DEFAULT - only exclude if explicitly requested
    if include_git_push:
        template += f"""
MANDATORY - Git Push & Deploy:
```bash
# After implementing all changes:
git add -A
git commit -m "v{version} - {feature_name.lower().replace(' ', '-')}"
git push origin main

# Verify deployment triggered:
# Agricultural: https://github.com/Poljopodrska/ava-olo-agricultural-core/actions
# Monitoring: https://github.com/Poljopodrska/ava-olo-monitoring-dashboards/actions
```"""
    else:
        template += """
NO GIT PUSH: This task is for local development/testing only."""
    
    return template


def generate_ptp_template(
    objective: str,
    tasks: list[dict]
) -> str:
    """Generate PTP (Peter's Tasks Protocol) template"""
    
    template = f"""PTP - PETER'S TASKS PROTOCOL
OBJECTIVE: {objective}
TOTAL TASKS: {len(tasks)}
"""
    
    for i, task in enumerate(tasks, 1):
        steps = "\n".join(f"- [ ] {step}" for step in task['steps'])
        
        template += f"""
TASK {i}: {task['name']}
{steps}
REPORT BACK: "{task['report']}"
"""
        
        if i < len(tasks):
            template += f"\nWAIT FOR: {task.get('wait_for', 'Task ' + str(i) + ' complete')}\n"
    
    template += """
COMPLETION VERIFICATION:
- [ ] All tasks reported complete
- [ ] System functioning as expected
- [ ] Documentation updated"""
    
    return template


# Example usage
if __name__ == "__main__":
    # Example TS with automatic git push
    ts_example = generate_ts_template(
        feature_name="Dashboard Performance Optimization",
        description="Bulgarian mango farmer's dashboard loads in under 2 seconds on slow connection",
        goal="Reduce dashboard load time by 50% through caching and optimization",
        success_criteria=[
            "Dashboard loads in <2 seconds on 3G connection",
            "Implements Redis caching for frequent queries",
            "Lazy loading for non-critical components"
        ],
        requirements=[
            "Use Redis for query result caching",
            "Implement React.lazy for code splitting",
            "Add performance monitoring metrics"
        ],
        context={
            "Current": "Dashboard takes 4-6 seconds to load",
            "Database": "Heavy queries on farmers table",
            "Integration": "Redis service, monitoring API"
        },
        implementation_approach="""- Add Redis caching layer in /modules/cache/
- Implement query result caching with 5-minute TTL
- Use React.lazy() for dashboard components
- Add performance.measure() for load time tracking""",
        version="3.6.0"
    )
    
    print("=== TS EXAMPLE (with automatic git push) ===")
    print(ts_example)
    print("\n" + "="*50 + "\n")
    
    # Example PTP
    ptp_example = generate_ptp_template(
        objective="Set up Stripe payment integration",
        tasks=[
            {
                "name": "Create Stripe Account",
                "steps": [
                    "Go to stripe.com",
                    "Sign up with business account",
                    "Complete verification",
                    "Enable test mode"
                ],
                "report": "Account created, in test mode",
                "wait_for": "Account confirmation"
            },
            {
                "name": "Get API Keys",
                "steps": [
                    "Navigate to Developers → API keys",
                    "Copy publishable key",
                    "Copy secret key",
                    "Store securely"
                ],
                "report": "Keys obtained and stored",
                "wait_for": "Keys confirmation"
            }
        ]
    )
    
    print("=== PTP EXAMPLE ===")
    print(ptp_example)