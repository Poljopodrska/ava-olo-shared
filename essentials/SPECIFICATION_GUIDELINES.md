# AVA OLO Specification Guidelines
*For Web-based Claude to write feature specifications*

## Communication Protocol for Web-based Claude

### Clarification Process
When receiving instructions, web-based Claude should:

1. **Evaluate Understanding**: For every instruction, determine if clarification is needed
2. **Ask Numbered Questions**: If clarification is required, ask numbered questions:
   - **1.** [First question]
   - **2.** [Second question]
   - etc.

3. **Use Lettered Options** (preferred): When possible, provide multiple choice answers:
   - **Question 1:** Which deployment approach should we use?
     - **a)** ECS deployment with rolling updates
     - **b)** App Runner deployment with instant scaling
     - **c)** Lambda-based serverless approach

4. **Avoid Unnecessary Questions**: If the instruction is clear, proceed without inventing questions

### Task Assignment Priority

**ABSOLUTE PRIORITY: Claude Code (c.code)**
- Before starting any task, Claude should determine: "Can Claude Code handle this?"
- If YES → **c.code has absolute priority**
- Claude Code is capable of:
  - TypeScript/JavaScript development
  - File manipulation and code generation
  - Database operations and API development
  - Testing and deployment verification
  - Git operations and version control

**FALLBACK: Human**
- Only assign tasks to human when c.code genuinely cannot handle them
- Examples of human-only tasks:
  - External service setup requiring manual verification
  - Business decisions requiring domain expertise
  - Physical hardware configurations
  - Third-party account setups requiring manual approval

### Communication Flow
1. Receive instruction
2. Ask clarifying questions (if needed, using numbered/lettered format)
3. **WAIT for all answers before proceeding**
4. Once all questions are answered, determine if c.code can handle the task
5. If YES: Create TS (Task Specification) for c.code
6. If NO: Document why and assign to human

**IMPORTANT**: Do NOT write a TS until all clarifying questions have been answered. First clarify, then specify.

---

## 📝 MANDATORY GIT PUSH REQUIREMENT

**EVERY Task Specification MUST include Git push commands in the implementation.**

This is MANDATORY to ensure:
- All changes are deployed automatically via GitHub Actions
- No manual deployments bypass Git (security requirement)
- Bulgarian mango farmers get updates immediately
- All deployments are traceable to Git commits

**Standard Git Push Block (include in EVERY TS):**
```bash
# After implementing all changes:
git add -A
git commit -m "feat: [brief description of what was implemented]"
git push origin main

# Verify deployment triggered:
echo "Check GitHub Actions for deployment status"
```

## Standard Abbreviations Vocabulary

**Essential abbreviations for all communication:**

**TS** = **TASK SPECIFICATION FOR CLAUDE CODE**
- When you see "TS" or "ts" anywhere, it means "TASK SPECIFICATION FOR CLAUDE CODE"
- These specifications follow the template below for Claude Code to implement

**CC** = **CLAUDE CODE**  
- When you see "CC" or "cc" anywhere, it means "Claude Code"
- The CLI-based coding assistant with absolute task priority
- Example: "CC should handle this TypeScript development task"

*Both web-based Claude and Claude Code must recognize these abbreviations*

## The 5-Step Recipe

1. **STATE THE GOAL** - One clear sentence
2. **APPLY MANGO RULE** - Explain for Bulgarian mango farmer
3. **DEFINE SUCCESS** - Measurable outcomes
4. **LIST REQUIREMENTS** - Specific, constitutional
5. **PROVIDE CONTEXT** - Current state, integrations
6. **GIVE IMPLEMENTATION GUIDANCE** - Concrete steps, specific approaches

## Specification Template (TS Format)

**Format**: Always provide the complete TS in a code block (using triple backticks ```) so it can be easily copied with the copy button. This makes it convenient for users to copy the entire specification with a single click.

```
TS - TASK SPECIFICATION FOR CLAUDE CODE
FEATURE: [Name]
MANGO TEST: [How it works for Bulgarian mango farmer]

GOAL:
- [One sentence objective]

SUCCESS CRITERIA:
- [ ] [Measurable outcome]
- [ ] [User can do X]
- [ ] Version deployed and verified
- [ ] Deployment integrity confirmed (/api/deployment/verify returns valid: true)
- [ ] Visual deployment health GREEN (/api/deployment/health)
- [ ] All tests pass before deployment
- [ ] SYSTEM_CHANGELOG.md updated with entry including verification status

REQUIREMENTS:
1. [Functional - what it does]
2. [Technical - how it works, LLM-first]
3. [User - farmer experience]

CONTEXT:
- Current: [What exists now]
- Database: [Check DATABASE_SCHEMA.md for current tables]
- Integration: [Which modules/APIs - consider CAVA for conversation flows]
- Example: [Concrete use case]

IMPLEMENTATION APPROACH (Required):
- [Specific technical steps to implement]
- [Concrete file paths and module structure]
- [Example code snippets or patterns]
- [Integration points and API endpoints]
- Note: Claude Code should discuss any implementation challenges

MANDATORY - Git Push & Deploy:
```bash
# After implementing all changes:
git add -A
git commit -m "feat: [brief description of what was implemented]"
git push origin main

# Verify deployment triggered:
# Agricultural: https://github.com/Poljopodrska/ava-olo-agricultural-core/actions
# Monitoring: https://github.com/Poljopodrska/ava-olo-monitoring-dashboards/actions
```
```

## Good vs Bad Specifications

### ❌ BAD:
"Add crop disease detection for US corn farmers"
- Hardcoded to US
- Specific crop
- No success criteria

### ✅ GOOD:
"Farmers photograph any crop, AI identifies diseases in their language"
- Works globally
- Any crop
- Clear success metric

## Constitutional Alignment Checklist
- [ ] Works for any crop (not hardcoded)
- [ ] Works in any country (global-first)
- [ ] Uses LLM for intelligence
- [ ] Leverages CAVA for conversation handling
- [ ] Respects farmer privacy
- [ ] Includes version expectation
- [ ] Constitutional compliance ≥90% required
- [ ] Must test before deployment

## Example: Soil Analysis Feature

```
TS - TASK SPECIFICATION FOR CLAUDE CODE
FEATURE: AI Soil Test Interpreter
MANGO TEST: Bulgarian mango farmer uploads lab PDF, gets advice in Bulgarian

GOAL:
- Transform technical soil reports into farmer-friendly recommendations

SUCCESS CRITERIA:
- [ ] Farmer uploads any lab format (PDF/image)
- [ ] Receives explanation in their language
- [ ] Gets specific actions for their crop
- [ ] Version 2.1.0 deployed and verified
- [ ] Deployment integrity confirmed (/api/deployment/verify returns valid: true)
- [ ] Visual deployment health GREEN (/api/deployment/health)
- [ ] All tests pass before deployment
- [ ] SYSTEM_CHANGELOG.md updated with entry including verification status

REQUIREMENTS:
1. LLM interprets any soil test format
2. PostgreSQL stores results with encryption
3. WhatsApp delivers recommendations

CONTEXT:
- Current: Farmers don't understand lab reports
- Integration: Lab API, WhatsApp Bot, LLM Service
- Example: "Your mangoes need iron. Add 50g/tree of chelated iron before flowering"

IMPLEMENTATION APPROACH (Required):
- Create soil_interpreter module in /modules/soil_interpreter/
- Add POST /api/v1/soil/analyze endpoint accepting multipart file upload
- Use GPT-4 Vision API for image/PDF analysis with OCR fallback
- Store results in farmer_soil_tests table with columns: id, farmer_id, test_data, interpretation, created_at
- Integration: Call CAVA service for conversational follow-up questions
- Example: `soil_service.interpret(file, farmer_id)` returns structured interpretation
- Note: Claude Code should discuss if technical constraints require adjustments

MANDATORY - Git Push & Deploy:
```bash
# After implementing all changes:
git add -A
git commit -m "feat: soil analysis interpreter with AI recommendations"
git push origin main

# Verify deployment triggered:
# Agricultural: https://github.com/Poljopodrska/ava-olo-agricultural-core/actions
# Monitoring: https://github.com/Poljopodrska/ava-olo-monitoring-dashboards/actions
```
```

## Database Schema Reference
- **DATABASE_SCHEMA.md** - Auto-updated every 15 minutes
- Always check current schema before designing features
- Contains all tables, columns, types, and relationships
- Use for understanding what data is available

## Remember
- Specifications should include both WHAT and HOW
- Provide concrete implementation steps
- Be specific about technical approaches
- Always think globally (MANGO RULE)
- Include deployment version expectations
- MUST include diary update as success criteria
- Check DATABASE_SCHEMA.md for current structure
- Consider CAVA for any conversation/interaction features
- Claude Code should feel empowered to discuss implementation challenges