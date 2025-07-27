# Web Claude Upload Instructions

## Essential Files to Upload to Web Claude

Upload these 10 essential files when starting a new chat session:

### Core System Files (Always Upload)
1. **AVA_OLO_CONSTITUTION.md** - Core principles (15 constitutional rules)
2. **IMPLEMENTATION_GUIDELINES.md** - Implementation rules for Claude Code
3. **SPECIFICATION_GUIDELINES.md** - How to write task specifications
4. **QUICK_START.md** - System overview and key concepts
5. **SYSTEM_CHANGELOG.md** - Recent changes and version history

### Technical Reference Files (Upload as needed)
6. **CAVA_TECHNICAL_SPECIFICATION.md** - CAVA conversation system
7. **DATABASE_SCHEMA.md** - Current database structure
8. **MANGO_RULE_CLARIFICATION.md** - Universal thinking (Bulgarian mango farmer)
9. **ENVIRONMENT_VARIABLES.md** - Complete environment variables guide
10. **GIT_PUSH_STANDARD.md** - Standardized deployment procedures

## Upload Order

### For All Tasks
1. **QUICK_START.md** - System overview first
2. **SYSTEM_CHANGELOG.md** - Check recent changes
3. **AVA_OLO_CONSTITUTION.md** - Core principles
4. **IMPLEMENTATION_GUIDELINES.md** - How to implement

### For Specific Tasks
- **Environment issues**: Add **ENVIRONMENT_VARIABLES.md**
- **Deployment issues**: Add **GIT_PUSH_STANDARD.md**
- **CAVA/Chat features**: Add **CAVA_TECHNICAL_SPECIFICATION.md**
- **Database work**: Add **DATABASE_SCHEMA.md**

## Quick Copy Command

From this directory, you can select all files at once:
- Select all `.md` files except this README
- Drag and drop into Web Claude

## Important Notes

- These files are automatically synced from main essentials folder
- Always use files from THIS folder for Web Claude uploads
- Do NOT upload files from other locations (may be outdated)
- Last updated: 2025-07-27 09:23:59

## File Status

Successfully copied: 10 files
Missing files: 0 files

## 🚨 Critical Files for Claude Code

### Environment Variables Issues
If Claude Code says "environment variable not found":
- Upload **ENVIRONMENT_VARIABLES.md** 
- Shows that ALL variables ARE set in AWS ECS
- Provides proper access patterns

### Deployment Issues  
If you need consistent git push procedure:
- Upload **GIT_PUSH_STANDARD.md**
- Shows standardized scripts: `./push.sh v3.5.3 "Description"`
- Handles retries and error messages

