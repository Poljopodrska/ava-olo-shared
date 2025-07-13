# 📝 New Feature Template

Use this template when adding ANY new feature to AVA OLO. Every feature must pass constitutional review!

## 🏛️ Constitutional Checklist

Before writing any code, verify your feature passes these tests:

### 1. 🥭 MANGO RULE Compliance
- [ ] Feature works for Bulgarian mango farmers
- [ ] Feature works for ALL crops (exotic included)
- [ ] Feature works in ALL countries
- [ ] No geographic discrimination
- [ ] No crop-specific hardcoding

### 2. 🧠 LLM-FIRST Verification  
- [ ] Core logic uses LLM, not hardcoded rules
- [ ] Decisions are AI-driven, not predetermined
- [ ] Flexible enough for unknown scenarios
- [ ] No fixed business logic

### 3. 🔒 Privacy Impact Assessment
- [ ] No farmer personal data sent to external APIs
- [ ] All data stays within our infrastructure
- [ ] Proper anonymization before LLM calls
- [ ] GDPR compliant data handling

### 4. 🧩 Module Independence
- [ ] Feature can work if other services are down
- [ ] No direct imports between services
- [ ] Uses API calls for cross-service communication
- [ ] Graceful degradation on failures

### 5. 🌍 Localization Ready
- [ ] Supports all 50+ languages
- [ ] Handles minority farmers (Hungarian in Croatia)
- [ ] Smart country detection works
- [ ] Cultural context considered

## 📋 Feature Planning Template

```markdown
# Feature Name: [Your Feature Name]

## Overview
**Purpose**: [What problem does this solve for farmers?]
**Constitutional Compliance**: [How does it follow our principles?]
**MANGO TEST**: [How would Bulgarian mango farmer use this?]

## User Stories
1. As a [type of farmer], I want to [action] so that [benefit]
2. As a minority farmer, I want to [action] in my language
3. As a farmer with exotic crops, I want [feature] to work

## Technical Approach
- **LLM Integration**: [How will AI make decisions?]
- **Database**: [What new data needed? No hardcoded values!]
- **API Endpoints**: [New endpoints following constitutional patterns]
- **Privacy**: [How is farmer data protected?]

## Success Criteria
- [ ] Works for mango farmers in cold climates
- [ ] Supports 50+ languages
- [ ] No hardcoded crop/country logic
- [ ] Performance under 3 seconds
- [ ] Handles errors gracefully
```

## 🛠️ Implementation Template

### Step 1: Create Feature Module

```python
# features/your_feature_name.py
"""
[Feature Name] - Constitutional Implementation

Purpose: [Brief description]
Constitutional Compliance: 
- MANGO RULE: ✓ Works for any crop/country
- LLM-FIRST: ✓ AI-driven logic
- PRIVACY-FIRST: ✓ No personal data exposed
"""

from typing import Dict, Any, Optional
import logging
from constitutional_base import ConstitutionalFeature

logger = logging.getLogger(__name__)

class YourFeatureName(ConstitutionalFeature):
    """
    [Feature description]
    
    Constitutional guarantees:
    1. Works for ALL farmers globally
    2. Supports ALL crops (including exotic)
    3. Respects privacy
    4. Uses LLM for intelligence
    """
    
    def __init__(self):
        super().__init__()
        self.validate_constitutional_compliance()
    
    async def process_request(self, 
                            request: Dict[str, Any],
                            context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process farmer request constitutionally
        
        Args:
            request: Farmer's request (any language)
            context: Farmer context (location, crops, etc.)
            
        Returns:
            Constitutional response
        """
        # Step 1: Detect language and country
        farmer_context = await self.detect_farmer_context(
            phone_number=request.get('phone_number'),
            language_override=request.get('language')
        )
        
        # Step 2: Process with LLM (no hardcoding!)
        llm_prompt = self._build_universal_prompt(request, farmer_context)
        llm_response = await self.llm.process(llm_prompt)
        
        # Step 3: Ensure privacy compliance
        safe_response = self.anonymize_response(llm_response)
        
        # Step 4: Format for farmer's language
        final_response = await self.format_for_farmer(
            safe_response, 
            farmer_context['language']
        )
        
        return {
            "success": True,
            "response": final_response,
            "constitutional_compliance": True,
            "feature": self.__class__.__name__,
            "metadata": {
                "language_used": farmer_context['language'],
                "country_detected": farmer_context['country'],
                "mango_rule_passed": True
            }
        }
    
    def _build_universal_prompt(self, 
                              request: Dict,
                              context: Dict) -> str:
        """
        Build LLM prompt that works universally
        NO HARDCODED LOGIC!
        """
        return f"""
        Process this agricultural request:
        
        Request: {request['query']}
        Farmer Context:
        - Country: {context['country']}
        - Language: {context['language']}
        - Current Crops: {context.get('crops', 'Unknown')}
        
        Requirements:
        1. Work for ANY crop (including mangoes in cold climates)
        2. Provide practical advice for the farmer's situation
        3. Consider local conditions but don't discriminate
        4. Respond appropriately for the farmer's context
        
        Generate helpful agricultural guidance.
        """
    
    def validate_constitutional_compliance(self):
        """
        Self-check for constitutional compliance
        """
        violations = []
        
        # Check for hardcoded crops
        source = inspect.getsource(self.__class__)
        hardcoded_crops = ['tomato', 'corn', 'wheat', 'potato']
        for crop in hardcoded_crops:
            if f"'{crop}'" in source or f'"{crop}"' in source:
                violations.append(f"Hardcoded crop found: {crop}")
        
        # Check for country discrimination
        if 'if country ==' in source or 'if country in' in source:
            violations.append("Country-specific logic detected")
        
        if violations:
            raise ConstitutionalViolation(
                f"Feature violates constitution: {violations}"
            )
```

### Step 2: Add API Endpoint

```python
# api/endpoints/your_feature.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class FeatureRequest(BaseModel):
    """Universal request format"""
    query: str
    farmer_id: Optional[int] = None
    language: Optional[str] = None
    phone_number: Optional[str] = None
    context: Optional[dict] = None

@router.post("/api/v1/your-feature")
async def process_feature_request(request: FeatureRequest):
    """
    Process [feature name] request constitutionally
    
    Features:
    - Works for any crop (✓ Mango in Bulgaria)
    - Works for any language (✓ 50+ supported)
    - Works for any country (✓ No discrimination)
    - Privacy compliant (✓ No personal data exposed)
    """
    try:
        feature = YourFeatureName()
        result = await feature.process_request(
            request.dict(),
            context=await get_farmer_context(request.farmer_id)
        )
        
        return {
            "success": True,
            "data": result,
            "constitutional_compliance": True,
            "api_version": "v1"
        }
        
    except Exception as e:
        # Even errors are constitutional
        logger.error(f"Feature error: {e}")
        return {
            "success": False,
            "error": "Service temporarily unavailable",
            "fallback": get_constitutional_fallback(request.language),
            "constitutional_compliance": True
        }
```

### Step 3: Add Database Support (If Needed)

```python
# database/migrations/add_your_feature.sql
-- Constitutional database changes
-- No hardcoded defaults that discriminate!

-- Good: Flexible schema that works globally
CREATE TABLE IF NOT EXISTS feature_data (
    id SERIAL PRIMARY KEY,
    farmer_id INTEGER REFERENCES farmers(id),
    feature_type VARCHAR(100),  -- Any feature type
    data JSONB,  -- Flexible data storage
    language VARCHAR(10),  -- Farmer's language
    country_code VARCHAR(3),  -- Auto-detected
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- No hardcoded constraints on values!
    -- No DEFAULT 'Croatia' or similar
);

-- Add indexes for performance
CREATE INDEX idx_feature_farmer ON feature_data(farmer_id);
CREATE INDEX idx_feature_type ON feature_data(feature_type);
CREATE INDEX idx_feature_country ON feature_data(country_code);

-- Add to farmer's view
CREATE OR REPLACE VIEW farmer_features AS
SELECT 
    f.*,
    fd.feature_type,
    fd.data,
    -- Smart localization
    COALESCE(f.preferred_language, clm.primary_language) as display_language
FROM farmers f
LEFT JOIN feature_data fd ON f.id = fd.farmer_id
LEFT JOIN country_language_mapping clm ON f.country_code = clm.country_code;

COMMENT ON TABLE feature_data IS 'Constitutional feature storage - works for any feature type globally';
```

### Step 4: Add Tests

```python
# tests/test_your_feature.py
import pytest
from features.your_feature_name import YourFeatureName

class TestYourFeatureConstitutional:
    """Test constitutional compliance of new feature"""
    
    @pytest.mark.asyncio
    async def test_mango_rule_compliance(self):
        """Test feature works for Bulgarian mango farmer"""
        feature = YourFeatureName()
        
        # Test with mango in Bulgaria
        result = await feature.process_request({
            "query": "How to use [feature] for my mango farm?",
            "context": {
                "country": "BG",
                "crops": ["mango"],
                "language": "bg"
            }
        })
        
        assert result["success"]
        assert "mango" in result["response"].lower()
        assert result["constitutional_compliance"]
        assert result["metadata"]["mango_rule_passed"]
    
    @pytest.mark.asyncio
    async def test_minority_farmer_support(self):
        """Test feature supports minority farmers"""
        feature = YourFeatureName()
        
        # Hungarian farmer in Croatia
        result = await feature.process_request({
            "query": "Hogyan használjam ezt a funkciót?",  # Hungarian
            "phone_number": "+385123456789",  # Croatian number
            "language": "hu",  # Hungarian override
            "context": {"ethnicity": "Hungarian"}
        })
        
        assert result["success"]
        assert result["metadata"]["language_used"] == "hu"
        assert result["metadata"]["country_detected"] == "HR"
    
    @pytest.mark.asyncio
    async def test_no_hardcoded_logic(self):
        """Verify no hardcoded patterns"""
        feature = YourFeatureName()
        
        # Test with unusual combinations
        unusual_scenarios = [
            ("pineapple", "Norway"),
            ("coffee", "Iceland"),
            ("coconut", "Canada"),
            ("cacao", "Russia")
        ]
        
        for crop, country in unusual_scenarios:
            result = await feature.process_request({
                "query": f"Use feature for {crop}",
                "context": {"country": country, "crops": [crop]}
            })
            
            # Must not refuse based on crop/country
            assert result["success"]
            assert "not possible" not in result["response"].lower()
            assert "cannot" not in result["response"].lower()
    
    @pytest.mark.asyncio
    async def test_privacy_compliance(self):
        """Test no personal data leaks"""
        from unittest.mock import patch
        
        feature = YourFeatureName()
        
        with patch('openai.ChatCompletion.create') as mock_llm:
            await feature.process_request({
                "query": "Help me, John Smith, ID 12345",
                "farmer_id": 12345,
                "farmer_name": "John Smith"
            })
            
            # Check no personal data in LLM calls
            for call in mock_llm.call_args_list:
                call_str = str(call)
                assert "John Smith" not in call_str
                assert "12345" not in call_str
```

## 🚀 Deployment Template

### Pre-Deployment Checklist

```yaml
# .github/workflows/constitutional-check.yml
name: Constitutional Compliance Check

on:
  pull_request:
    branches: [ main ]

jobs:
  constitutional-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Check MANGO RULE Compliance
        run: |
          python scripts/check_mango_rule.py
          
      - name: Check for Hardcoded Patterns
        run: |
          python scripts/detect_hardcoding.py
          
      - name: Verify Language Support
        run: |
          python scripts/verify_languages.py
          
      - name: Run Constitutional Tests
        run: |
          pytest tests/test_constitutional_compliance.py -v
```

### Deployment Script

```bash
#!/bin/bash
# deploy_constitutional_feature.sh

echo "🏛️ Constitutional Feature Deployment"

# Step 1: Run constitutional checks
echo "Running constitutional compliance checks..."
python test_constitutional_compliance.py
if [ $? -ne 0 ]; then
    echo "❌ Constitutional violations detected!"
    exit 1
fi

# Step 2: Test with Bulgarian mango farmer
echo "Testing MANGO RULE compliance..."
python test_mango_rule.py
if [ $? -ne 0 ]; then
    echo "❌ MANGO RULE failed!"
    exit 1
fi

# Step 3: Deploy to AWS
echo "Deploying to AWS App Runner..."
git add .
git commit -m "Add [Feature Name] - Constitutional compliance verified 🥭"
git push origin main

echo "✅ Deployment complete - constitutionally compliant!"
```

## 📊 Monitoring Template

```python
# monitoring/constitutional_metrics.py
"""
Monitor constitutional compliance in production
"""

class ConstitutionalMonitor:
    """Monitor feature for constitutional violations"""
    
    def __init__(self, feature_name: str):
        self.feature_name = feature_name
        self.metrics = {
            "mango_rule_violations": 0,
            "privacy_violations": 0,
            "language_failures": 0,
            "hardcoded_detections": 0
        }
    
    async def check_request(self, request: dict, response: dict):
        """Check each request for compliance"""
        
        # Check MANGO RULE
        if "not supported" in response.get("response", "").lower():
            self.metrics["mango_rule_violations"] += 1
            await self.alert_violation("MANGO RULE", request, response)
        
        # Check privacy
        if self.contains_personal_data(response):
            self.metrics["privacy_violations"] += 1
            await self.alert_violation("PRIVACY", request, response)
        
        # Check language
        if request.get("language") != response.get("metadata", {}).get("language_used"):
            self.metrics["language_failures"] += 1
        
    async def alert_violation(self, violation_type: str, request: dict, response: dict):
        """Alert on constitutional violations"""
        alert = {
            "severity": "CRITICAL",
            "type": f"CONSTITUTIONAL_VIOLATION_{violation_type}",
            "feature": self.feature_name,
            "request_sample": self.anonymize_request(request),
            "response_sample": response.get("response", "")[:100],
            "timestamp": datetime.utcnow().isoformat(),
            "action_required": "Immediate investigation required"
        }
        
        # Send to monitoring system
        await send_alert(alert)
        
        # Log for audit
        logger.critical(f"Constitutional violation: {violation_type}")
```

## 🎯 Launch Checklist

Before launching your feature:

### Technical Readiness
- [ ] All constitutional tests pass
- [ ] MANGO RULE verified with edge cases
- [ ] Privacy audit completed
- [ ] 50+ languages tested
- [ ] Performance benchmarks met
- [ ] Error handling implemented
- [ ] Monitoring configured

### Documentation
- [ ] API documentation updated
- [ ] User guide created (multi-language)
- [ ] Constitutional compliance documented
- [ ] Examples for various scenarios

### Production Readiness
- [ ] AWS App Runner configuration updated
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Rollback plan prepared
- [ ] Support team briefed

### Final Constitutional Review
- [ ] Would this work for a Bulgarian mango farmer? ✓
- [ ] Is it using LLM-first approach? ✓
- [ ] Does it protect farmer privacy? ✓
- [ ] Can minority farmers use it? ✓
- [ ] No hardcoded discrimination? ✓

## 🆘 Constitutional Violations

If you discover your feature violates the constitution:

1. **STOP all development immediately**
2. **Document the violation**
3. **Plan remediation using LLM-first approach**
4. **Re-test with mango farmers**
5. **Get constitutional review before proceeding**

Remember: It's better to delay launch than violate the constitution!

---

**The MANGO RULE is supreme. Every feature must work for Bulgarian mango farmers!** 🥭