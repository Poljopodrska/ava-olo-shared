# 🚀 AVA OLO Standard Git Push Procedure
*Ensuring Bulgarian mango farmer's code reaches production consistently*

## ✅ ALWAYS Use This Method

### Quick Push (Recommended)
```bash
./push.sh v3.5.3 "Fix dashboard display issue"
```

### Full Push Script
```bash
./git-push.sh v3.5.3 "Fix dashboard display issue"
```

## 🔄 What the Scripts Do

### 1. **Safety Checks**
- ✅ Verifies you're on main branch
- ✅ Pulls latest changes to prevent conflicts
- ✅ Shows what will be committed

### 2. **Standard Process**
- ✅ Stages all changes (`git add -A`)
- ✅ Commits with proper format (`vX.X.X - Description`)
- ✅ Pushes with automatic retry logic

### 3. **Error Handling**
- ✅ Clear error messages for common issues
- ✅ Helpful troubleshooting suggestions
- ✅ Automatic retry on network failures (up to 3 attempts)

### 4. **Post-Push Verification**
- ✅ Provides GitHub Actions link
- ✅ Suggests next steps for verification
- ✅ Updates local git tags

## 📋 Usage Examples

### Simple Changes
```bash
./push.sh v3.5.4 "Add farmer phone validation"
./push.sh v3.5.5 "Fix weather API integration"
./push.sh v3.5.6 "Update dashboard styling"
```

### Feature Releases
```bash
./push.sh v3.6.0 "Major feature: Crop rotation tracking system"
./push.sh v3.7.0 "Add WhatsApp integration for farmer notifications"
./push.sh v4.0.0 "Complete UI redesign with improved mobile support"
```

### Bug Fixes
```bash
./push.sh v3.5.7 "Fix registration form validation bug"
./push.sh v3.5.8 "Resolve database connection timeout issue"
./push.sh v3.5.9 "Emergency fix for CAVA conversation memory"
```

## 🚨 Common Issues & Solutions

### ❌ "Not on main branch"
```bash
# Solution:
git checkout main
./push.sh v3.5.3 "Your description"
```

### ❌ "Pull failed - resolve conflicts"
```bash
# Solution:
git status                    # See conflicted files
# Edit files to resolve conflicts
git add [resolved_files]
git commit -m "Resolve merge conflicts"
./push.sh v3.5.3 "Your description"
```

### ❌ "Invalid version format"
```bash
# Wrong:
./push.sh 3.5.3 "Description"        # Missing 'v'
./push.sh v3.5 "Description"         # Missing patch number

# Correct:
./push.sh v3.5.3 "Description"       # ✅ Proper format
```

### ❌ "Description too short"
```bash
# Wrong:
./push.sh v3.5.3 "Fix bug"          # Only 7 characters

# Correct:
./push.sh v3.5.3 "Fix registration validation bug"  # ✅ 10+ characters
```

### ❌ "Push failed after 3 attempts"
```bash
# Check network connection
ping github.com

# Check git credentials
git config --list | grep user

# Try manual push to see detailed error
git push origin main
```

## 🛡️ Protection System Integration

The git push scripts work seamlessly with the protection system:

### Git Hooks Integration
- ✅ Automatically validates commit message format
- ✅ Runs constitutional compliance checks
- ✅ Verifies no design changes without approval

### Version Protection
- ✅ Prevents duplicate version numbers
- ✅ Enforces semantic versioning format
- ✅ Updates version tracking automatically

### Error Prevention
- ✅ Prevents pushing broken features
- ✅ Blocks unauthorized design changes
- ✅ Ensures changelog is updated

## 📝 Never Do This

### ❌ Manual Git Commands (Inconsistent)
```bash
# Don't do this - no safety checks
git add .
git commit -m "fix"
git push
```

### ❌ Force Push (Dangerous)
```bash
# NEVER do this - breaks protection
git push --force
git push --force-with-lease
```

### ❌ Multi-Step Manual Process
```bash
# Don't do this - error prone
git checkout main
git pull
git add .
git commit -m "some change"
git push
# (Missing validation, retry logic, error handling)
```

### ❌ Wrong Version Format
```bash
# Wrong formats:
./push.sh 3.5.3 "Description"        # Missing 'v'
./push.sh v3.5.3.1 "Description"     # Too many numbers
./push.sh v3.5 "Description"         # Missing patch version
./push.sh latest "Description"       # Not a version number
```

## 🔧 Script Locations

### Main Repository Root
- `git-push.sh` - Full featured push script with all safety checks
- `push.sh` - Simplified wrapper for daily use

### What Each Script Contains
- **git-push.sh**: Complete 300+ line script with comprehensive error handling
- **push.sh**: Simple 20-line wrapper that calls git-push.sh

## 🎯 Benefits of Standardized Process

### ✅ Consistency
- Same process every time
- No manual steps to forget
- Standardized commit messages

### ✅ Safety
- Automatic conflict prevention
- Validation before push
- Clear error messages

### ✅ Reliability
- Retry logic for network issues
- Protection system integration
- Post-push verification

### ✅ Efficiency
- One command deployment
- No manual staging or formatting
- Automatic next-step suggestions

## 🏛️ Constitutional Compliance

This standardized procedure enforces:

- **Principle 1**: Mango rule - same process for all developers
- **Principle 3**: Version visibility - all commits properly versioned
- **Principle 15**: Protection against breaking changes

## 🔍 Troubleshooting Checklist

If push fails, check:

1. **Branch**: Are you on main?
   ```bash
   git branch --show-current
   ```

2. **Network**: Can you reach GitHub?
   ```bash
   ping github.com
   ```

3. **Credentials**: Are they configured?
   ```bash
   git config --list | grep user
   ```

4. **Conflicts**: Any merge conflicts?
   ```bash
   git status
   ```

5. **Protection**: Any hook failures?
   ```bash
   # Check last commit message format
   git log -1 --pretty=%s
   ```

## 📚 Related Documentation

- [Complete Protection System](/NO_STEPS_BACK_PROTECTION_GUIDE.md)
- [Environment Variables](/ava-olo-shared/essentials/ENVIRONMENT_VARIABLES.md)
- [Constitutional Principles](/ava-olo-shared/essentials/AVA_OLO_CONSTITUTION.md)

---

**🥭 Remember**: Always use the standardized scripts. The Bulgarian mango farmer's code deserves consistent, reliable deployment! 🥭

**Last Updated**: 2025-07-27  
**Version**: v3.5.3  
**Status**: ✅ Active and enforced