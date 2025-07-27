# PTP (Peter's Tasks Protocol) Examples
*Sequential human task workflows with report-back structure*

## PTP Example 1: AWS Service Setup

```
PTP - PETER'S TASKS PROTOCOL
OBJECTIVE: Set up new AWS RDS read replica
TOTAL TASKS: 3

TASK 1: Create RDS Read Replica
- [ ] Log into AWS Console
- [ ] Navigate to RDS
- [ ] Select production database
- [ ] Actions → Create read replica
- [ ] Choose same region
- [ ] Name: farmer-crm-read-replica
REPORT BACK: "Read replica created, endpoint: [URL]"

WAIT FOR: Confirmation with endpoint URL

TASK 2: Update Security Groups
- [ ] Go to EC2 → Security Groups
- [ ] Find replica security group
- [ ] Add inbound rule for ECS services
- [ ] Save changes
REPORT BACK: "Security group updated"

WAIT FOR: "Security group updated"

TASK 3: Test Connection
- [ ] I'll provide test code
- [ ] Run from your local environment
- [ ] Verify connection successful
REPORT BACK: "Connection test: [success/failed with error]"

COMPLETION VERIFICATION:
- [ ] Read replica accessible
- [ ] Security configured
- [ ] Connection verified
```

## PTP Example 2: Third-party Registration

```
PTP - PETER'S TASKS PROTOCOL  
OBJECTIVE: Register for OpenWeather API
TOTAL TASKS: 2

TASK 1: Create Account
- [ ] Go to openweathermap.org/api
- [ ] Click "Sign Up"
- [ ] Use company email
- [ ] Verify email
REPORT BACK: "Account created and verified"

WAIT FOR: "Account created"

TASK 2: Get API Key
- [ ] Log into dashboard
- [ ] Navigate to API keys
- [ ] Generate new key named "AVA-OLO"
- [ ] Copy key (keep secure)
REPORT BACK: "API key obtained"

COMPLETION: I'll create TS for CC to integrate the key
```

## PTP Example 3: Domain Configuration

```
PTP - PETER'S TASKS PROTOCOL
OBJECTIVE: Configure new domain for AVA OLO
TOTAL TASKS: 4

TASK 1: Purchase Domain
- [ ] Go to domain registrar
- [ ] Search for ava-olo.com
- [ ] Purchase if available
- [ ] Set auto-renewal
REPORT BACK: "Domain purchased: [domain name]"

WAIT FOR: Domain confirmation

TASK 2: Point to AWS Route 53
- [ ] Get nameservers from Route 53
- [ ] Update at registrar
- [ ] Wait for propagation
REPORT BACK: "Nameservers updated"

WAIT FOR: "Nameservers updated"

TASK 3: Create SSL Certificate
- [ ] AWS Certificate Manager
- [ ] Request certificate
- [ ] Validate via DNS
- [ ] Note ARN
REPORT BACK: "SSL cert created, ARN: [arn]"

WAIT FOR: Certificate ARN

TASK 4: Update ALB
- [ ] Add certificate to ALB
- [ ] Create routing rules
- [ ] Test HTTPS access
REPORT BACK: "HTTPS working on [domain]"

COMPLETION VERIFICATION:
- [ ] Domain accessible via HTTPS
- [ ] SSL certificate valid
- [ ] Routing configured
```

## PTP Example 4: Local Development Setup

```
PTP - PETER'S TASKS PROTOCOL
OBJECTIVE: Set up local development environment
TOTAL TASKS: 3

TASK 1: Install Prerequisites
- [ ] Install Docker Desktop
- [ ] Install Node.js 18+
- [ ] Install AWS CLI
- [ ] Install Git
REPORT BACK: "All tools installed"

WAIT FOR: Installation confirmation

TASK 2: Clone and Configure
- [ ] Clone repository
- [ ] Copy .env.example to .env
- [ ] Add AWS credentials
- [ ] Run npm install
REPORT BACK: "Repository configured"

WAIT FOR: "Repository configured"

TASK 3: Start Services
- [ ] Run docker-compose up
- [ ] Check localhost:3000
- [ ] Verify API at localhost:8080
REPORT BACK: "Services running, accessible at [URLs]"

COMPLETION: Ready for local development
```

## PTP Best Practices

### 1. Clear Task Boundaries
Each task should be:
- Self-contained
- Have clear completion criteria
- Not depend on Claude Code actions

### 2. Specific Report Format
Always specify what to report:
- ❌ "Let me know when done"
- ✅ "Report back with: endpoint URL"

### 3. Sequential Dependencies
- Task 2 should only start after Task 1 complete
- Use "WAIT FOR" to enforce sequence
- Don't skip ahead

### 4. Verification Steps
Final task or completion should verify:
- All objectives met
- System functioning
- Ready for next phase

## When to Use PTP vs TS

### Use PTP When:
- Human needs to use external websites
- Manual account creation required
- Physical access needed
- Approval workflows involved
- Sequential human actions required

### Use TS When:
- Code implementation needed
- File changes required
- Automated tasks possible
- No human intervention needed

### Combined Workflow:
1. PTP for human setup tasks
2. Human completes and reports
3. TS for CC to implement integration
4. CC completes implementation

## Template Generator

```python
def generate_ptp(objective, tasks):
    """Generate PTP template"""
    template = f"""
PTP - PETER'S TASKS PROTOCOL
OBJECTIVE: {objective}
TOTAL TASKS: {len(tasks)}
"""
    
    for i, task in enumerate(tasks, 1):
        template += f"""
TASK {i}: {task['name']}
{chr(10).join(f"- [ ] {step}" for step in task['steps'])}
REPORT BACK: "{task['report']}"

WAIT FOR: {task['wait_for']}
"""
    
    template += """
COMPLETION VERIFICATION:
- [ ] All tasks reported complete
- [ ] System functioning as expected
- [ ] Documentation updated
"""
    return template
```

## Quick Reference

- **PTP** = Sequential human tasks
- **Report back** = Confirmation message
- **WAIT FOR** = Don't proceed until confirmed
- **Completion** = All tasks verified done

Remember: PTP ensures proper sequencing of human actions with clear checkpoints!