# 🔴 AVA OLO COMMIT MESSAGE STANDARD 🔴

## MANDATORY FORMAT: `vX.X.X - Description`

### ✅ CORRECT Examples:
```bash
v3.5.0 - Add farmer registration validation
v3.5.1 - Fix database connection timeout issue  
v3.6.0 - Implement crop rotation tracking feature
v4.0.0 - Major refactor of authentication system
```

### ❌ WRONG Examples:
```bash
Fix database bug                    # NO VERSION NUMBER
3.5.1 - Add feature                # MISSING 'v' PREFIX
v3.5 - Update code                 # INCOMPLETE VERSION (needs v3.5.0)
Update farmer registration         # NO VERSION AT ALL
feat: add new dashboard           # WRONG FORMAT
```

## WHY VERSION NUMBERS ARE MANDATORY

1. **Tracking**: Every change is trackable to a specific version
2. **Rollback**: Easy to identify and rollback to specific versions
3. **Deployment**: Automated systems rely on version numbers
4. **History**: Clear progression of changes over time

## VERSION NUMBERING RULES

### Format: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v**X**.0.0): Breaking changes, major features
- **MINOR** (v3.**X**.0): New features, backwards compatible
- **PATCH** (v3.5.**X**): Bug fixes, small improvements

### Examples:
- `v3.5.0` → `v3.5.1`: Bug fix (increment PATCH)
- `v3.5.1` → `v3.6.0`: New feature (increment MINOR, reset PATCH)
- `v3.6.0` → `v4.0.0`: Breaking change (increment MAJOR, reset others)

## GIT HOOKS ENFORCEMENT

Git hooks are configured to **AUTOMATICALLY REJECT** commits without proper format:

```bash
$ git commit -m "Fix bug"
❌ ERROR: Commit message must follow format: vX.X.X - Description
Example: v3.5.2 - Complete protection system implementation

$ git commit -m "v3.5.2 - Fix database query error"
✅ Commit message format validated: v3.5.2
```

## QUICK REFERENCE

Before committing, ask yourself:
1. Does my message start with `vX.X.X`?
2. Is there a space, dash, space after the version?
3. Is the description at least 10 characters?
4. Am I incrementing from the last version?

## SETUP GIT HOOKS

To enable automatic validation:
```bash
# In any AVA OLO repository:
./setup_git_hooks.sh

# Or manually:
git config core.hooksPath .githooks
```

---

**Remember**: The Bulgarian mango farmer's code deserves proper versioning! 🥭