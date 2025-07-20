# AVA OLO Specification Guidelines
*For Web-based Claude to write feature specifications*

## Important Abbreviation
**TS = TASK SPECIFICATION FOR CLAUDE CODE**
- When you see "TS" anywhere, it means "TASK SPECIFICATION FOR CLAUDE CODE"
- These specifications follow the template below for Claude Code to implement

## The 5-Step Recipe

1. **STATE THE GOAL** - One clear sentence
2. **APPLY MANGO RULE** - Explain for Bulgarian mango farmer
3. **DEFINE SUCCESS** - Measurable outcomes
4. **LIST REQUIREMENTS** - Specific, constitutional
5. **PROVIDE CONTEXT** - Current state, integrations
6. **GIVE IMPLEMENTATION GUIDANCE** - Concrete steps, specific approaches

## Specification Template (TS Format)

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