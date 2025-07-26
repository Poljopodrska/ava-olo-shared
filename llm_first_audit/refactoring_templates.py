#!/usr/bin/env python3
"""
LLM-First Refactoring Templates
Common patterns for converting hardcoded business logic to LLM-based decisions
"""

class RefactoringTemplate:
    """Base class for refactoring patterns"""
    
    @classmethod
    def get_template_name(cls):
        return cls.__name__
    
    @classmethod
    def get_description(cls):
        return cls.__doc__
    
    @staticmethod
    def before_example():
        """Show the problematic code pattern"""
        raise NotImplementedError
    
    @staticmethod
    def after_example():
        """Show the LLM-first replacement"""
        raise NotImplementedError

class CountryLogicRefactor(RefactoringTemplate):
    """Convert hardcoded country-specific logic to LLM-based global logic"""
    
    @staticmethod
    def before_example():
        """❌ Constitutional Violation - Hardcoded Countries"""
        return """
        # CRITICAL VIOLATION: Hardcoded country logic
        def validate_farmer_data(country, data):
            if country == 'BG' or country == 'BULGARIA':
                # Bulgarian specific validation
                if not data.get('egn'):  # Bulgarian national ID
                    return False
                return validate_bulgarian_phone(data['phone'])
            
            elif country == 'Croatia':
                # Croatian specific validation  
                if not data.get('oib'):  # Croatian personal ID
                    return False
                return validate_croatian_postal(data['postal'])
            
            elif country == 'Serbia':
                # Serbian specific validation
                if not data.get('jmbg'):  # Serbian ID
                    return False
                return validate_serbian_format(data)
            
            else:
                # New countries require code changes!
                raise NotImplementedError(f"Country {country} not supported")
        
        # PROBLEMS:
        # 1. Violates MANGO RULE (hardcoded countries)
        # 2. Cannot add new countries without development
        # 3. Assumes developer knows all country requirements
        # 4. Blocks global expansion
        """
    
    @staticmethod
    def after_example():
        """✅ LLM-First Compliant - Global Logic"""
        return """
        # CONSTITUTIONAL COMPLIANCE: LLM-based global validation
        async def validate_farmer_data(country, data):
            prompt = f'''
            Validate farmer registration data for {country}.
            
            Data provided:
            {json.dumps(data, indent=2)}
            
            Please validate according to {country}'s requirements:
            1. National ID format and validation
            2. Phone number format  
            3. Postal code format
            4. Required fields for farmers
            5. Any country-specific regulations
            
            Return JSON with:
            {{
                "is_valid": boolean,
                "errors": [list of specific validation errors],
                "suggestions": [how to fix each error],
                "country_requirements": "explanation of {country} farmer data rules"
            }}
            '''
            
            result = await llm.generate(prompt)
            return json.loads(result)
        
        # BENEFITS:
        # 1. Supports ALL countries instantly
        # 2. No code changes for new countries
        # 3. LLM knows local requirements
        # 4. Global expansion ready
        # 5. Constitutional compliance achieved
        """

class DecisionTreeRefactor(RefactoringTemplate):
    """Convert complex if/elif decision trees to LLM evaluation"""
    
    @staticmethod
    def before_example():
        """❌ Complex hardcoded decision tree"""
        return """
        # VIOLATION: 450+ lines of hardcoded fertilizer logic
        def recommend_fertilizer(crop, soil_type, season, location, weather):
            if crop == "corn":
                if season == "spring":
                    if soil_type == "clay":
                        if weather == "dry":
                            return "NPK 15-15-15, 300kg/ha"
                        elif weather == "wet":
                            return "NPK 20-10-10, 250kg/ha"
                    elif soil_type == "sandy":
                        if weather == "dry":
                            return "NPK 10-20-20, 400kg/ha"
                        # ... 200 more conditions
                elif season == "summer":
                    # ... 100 more conditions
            elif crop == "wheat":
                # ... 150 more conditions
            # ... endless combinations
        
        # PROBLEMS:
        # 1. Unmaintainable complexity
        # 2. Cannot handle new crops without massive code changes
        # 3. Doesn't consider local expertise
        # 4. Rigid, not adaptive to conditions
        """
    
    @staticmethod
    def after_example():
        """✅ LLM-based intelligent recommendation"""
        return """
        # LLM-FIRST: Intelligent, adaptive recommendations
        async def recommend_fertilizer(crop, soil_type, season, location, weather):
            prompt = f'''
            I need fertilizer recommendations for a farmer.
            
            Crop: {crop}
            Soil type: {soil_type}
            Season: {season}
            Location: {location}
            Weather conditions: {weather}
            
            Please provide expert agricultural advice:
            1. Specific fertilizer type and NPK ratio
            2. Application rate (kg/ha)
            3. Timing recommendations
            4. Local considerations for {location}
            5. Weather-specific adjustments
            6. Cost-effective alternatives
            
            Consider local agricultural practices, soil science, and climate data.
            Format as practical farmer guidance.
            '''
            
            return await llm.generate(prompt)
        
        # BENEFITS:
        # 1. Handles ANY crop automatically
        # 2. Considers complex interactions
        # 3. Adapts to local conditions
        # 4. Incorporates latest agricultural science
        # 5. Easy to maintain and improve
        """

class ValidationRefactor(RefactoringTemplate):
    """Convert hardcoded validation rules to LLM understanding"""
    
    @staticmethod
    def before_example():
        """❌ Hardcoded validation dictionaries"""
        return """
        # VIOLATION: Hardcoded validation rules for every country
        VALIDATION_RULES = {
            'Bulgaria': {
                'phone': r'^\+359[0-9]{8}$',
                'postal': r'^[0-9]{4}$',
                'national_id': r'^[0-9]{10}$',
                'farm_size': {'min': 0.1, 'max': 10000},
                'crops': ['wheat', 'corn', 'sunflower', 'vineyard']
            },
            'Croatia': {
                'phone': r'^\+385[0-9]{8,9}$',
                'postal': r'^[0-9]{5}$',
                'national_id': r'^[0-9]{11}$',
                'farm_size': {'min': 0.5, 'max': 5000},
                'crops': ['wheat', 'corn', 'olive', 'vineyard']
            },
            # ... 50+ more countries
        }
        
        def validate_field(country, field_name, value):
            rules = VALIDATION_RULES.get(country)
            if not rules:
                raise ValueError(f"Country {country} not supported")
            
            # Rigid rule matching
            if field_name == 'phone':
                return bool(re.match(rules['phone'], value))
            # ... more hardcoded checks
        
        # PROBLEMS:
        # 1. Requires maintaining rules for every country
        # 2. Cannot handle edge cases or variations
        # 3. Outdated rules break validation
        # 4. No contextual understanding
        """
    
    @staticmethod
    def after_example():
        """✅ LLM-based intelligent validation"""
        return """
        # LLM-FIRST: Intelligent, context-aware validation
        async def validate_field(country, field_name, value, context=None):
            prompt = f'''
            Validate this farmer data field for {country}:
            
            Field: {field_name}
            Value: {value}
            Context: {context}
            
            Please validate according to {country} standards:
            1. Is the format correct?
            2. Are there any regional variations?
            3. Could this be a valid alternative format?
            4. What would be the correct format if invalid?
            
            Consider local customs, data entry variations, and practical usage.
            
            Return JSON:
            {{
                "is_valid": boolean,
                "confidence": 0-100,
                "explanation": "why valid or invalid",
                "suggestions": "how to correct if needed",
                "alternative_formats": ["other acceptable formats"]
            }}
            '''
            
            result = await llm.generate(prompt)
            return json.loads(result)
        
        # BENEFITS:
        # 1. Handles ANY country automatically
        # 2. Understands context and variations
        # 3. Provides helpful suggestions
        # 4. Adapts to changing standards
        # 5. Human-like validation intelligence
        """

class RecommendationRefactor(RefactoringTemplate):
    """Convert hardcoded recommendation engines to LLM creativity"""
    
    @staticmethod
    def before_example():
        """❌ Hardcoded recommendation logic"""
        return """
        # VIOLATION: Rigid recommendation system
        def recommend_crops(location, soil_data, farmer_experience, market_data):
            recommendations = []
            
            # Hardcoded location-based recommendations
            if location.country == "Bulgaria":
                if soil_data['ph'] > 7:
                    recommendations.append("sunflower")
                if soil_data['nitrogen'] < 50:
                    recommendations.append("wheat")
                # ... hardcoded rules
            
            elif location.country == "Croatia":
                if location.coastal:
                    recommendations.append("olive")
                if soil_data['moisture'] > 60:
                    recommendations.append("corn")
                # ... more hardcoded rules
            
            # Filter by experience level (more hardcoded rules)
            if farmer_experience < 2:
                recommendations = [crop for crop in recommendations 
                                 if crop in BEGINNER_CROPS]
            
            return recommendations[:3]  # Arbitrary limit
        
        # PROBLEMS:
        # 1. Cannot consider complex interactions
        # 2. Misses creative opportunities
        # 3. Doesn't adapt to market changes
        # 4. Ignores farmer preferences
        """
    
    @staticmethod
    def after_example():
        """✅ LLM-based intelligent recommendations"""
        return """
        # LLM-FIRST: Intelligent, adaptive recommendations
        async def recommend_crops(location, soil_data, farmer_data, preferences):
            prompt = f'''
            I need crop recommendations for a farmer.
            
            Location: {location}
            Soil analysis: {json.dumps(soil_data, indent=2)}
            Farmer profile: {json.dumps(farmer_data, indent=2)}
            Preferences: {json.dumps(preferences, indent=2)}
            
            Please provide expert agricultural recommendations considering:
            1. Local climate and growing conditions
            2. Soil suitability and requirements
            3. Farmer experience and resources
            4. Market opportunities and demand
            5. Risk factors and mitigation
            6. Sustainable farming practices
            7. Seasonal timing and planning
            
            Provide 3-5 detailed recommendations with:
            - Crop name and variety
            - Why it's suitable for this farmer
            - Expected yield and profit potential
            - Growing requirements and challenges
            - Market and timing considerations
            
            Make recommendations practical and actionable.
            '''
            
            result = await llm.generate(prompt)
            return parse_recommendations(result)
        
        # BENEFITS:
        # 1. Considers ALL relevant factors
        # 2. Adapts to unique situations
        # 3. Provides detailed reasoning
        # 4. Incorporates latest agricultural knowledge
        # 5. Personalized to each farmer
        """

class BusinessLogicRefactor(RefactoringTemplate):
    """Convert complex business rules to LLM evaluation"""
    
    @staticmethod
    def before_example():
        """❌ Complex business rule engine"""
        return """
        # VIOLATION: Hardcoded business logic
        def calculate_loan_eligibility(farmer_data, financial_data, location):
            score = 0
            
            # Credit scoring rules (100+ conditions)
            if farmer_data['experience'] > 5:
                score += 20
            if farmer_data['education'] == 'agricultural':
                score += 15
            if farmer_data['land_owned'] > 10:
                score += 25
            
            # Location-based adjustments
            if location.country == 'Bulgaria':
                if location.region == 'Plovdiv':
                    score += 10  # Good agricultural region
                if location.eu_subsidies_available:
                    score += 15
            
            # Risk factors
            if financial_data['debt_ratio'] > 0.4:
                score -= 30
            if farmer_data['crop_diversity'] < 2:
                score -= 10  # Monoculture risk
            
            # ... 200+ more hardcoded rules
            
            return {
                'eligible': score > 70,
                'score': score,
                'amount': calculate_amount(score)  # More hardcoded logic
            }
        
        # PROBLEMS:
        # 1. Cannot adapt to changing conditions
        # 2. Misses nuanced situations
        # 3. Biased toward specific scenarios
        # 4. Cannot explain decisions well
        """
    
    @staticmethod
    def after_example():
        """✅ LLM-based intelligent business decisions"""
        return """
        # LLM-FIRST: Intelligent business evaluation
        async def evaluate_loan_eligibility(farmer_data, financial_data, location):
            prompt = f'''
            Evaluate loan eligibility for this farmer:
            
            Farmer Profile:
            {json.dumps(farmer_data, indent=2)}
            
            Financial Information:
            {json.dumps(financial_data, indent=2)}
            
            Location: {location}
            
            Please provide a comprehensive evaluation considering:
            1. Farming experience and track record
            2. Financial stability and cash flow
            3. Land ownership and assets
            4. Crop diversification and risk management
            5. Local agricultural conditions and support
            6. Market access and opportunities
            7. Climate and environmental factors
            8. Government programs and subsidies available
            
            Provide detailed assessment with:
            - Risk score (1-100)
            - Loan eligibility recommendation
            - Suggested loan amount and terms
            - Key strengths and concerns
            - Recommendations for improvement
            - Supporting rationale for decision
            
            Be fair, comprehensive, and supportive of agricultural development.
            '''
            
            result = await llm.generate(prompt)
            return parse_loan_assessment(result)
        
        # BENEFITS:
        # 1. Considers ALL relevant factors holistically
        # 2. Provides clear reasoning
        # 3. Adapts to unique situations
        # 4. Fair and unbiased evaluation
        # 5. Supportive of farmer development
        """

# Template Registry
REFACTORING_TEMPLATES = [
    CountryLogicRefactor,
    DecisionTreeRefactor, 
    ValidationRefactor,
    RecommendationRefactor,
    BusinessLogicRefactor
]

def generate_refactoring_guide():
    """Generate comprehensive refactoring guide"""
    guide = "# LLM-First Refactoring Guide\n\n"
    
    for template_class in REFACTORING_TEMPLATES:
        guide += f"## {template_class.get_template_name()}\n"
        guide += f"{template_class.get_description()}\n\n"
        
        guide += "### Before (Violation)\n"
        guide += "```python\n"
        guide += template_class.before_example()
        guide += "\n```\n\n"
        
        guide += "### After (LLM-First)\n"
        guide += "```python\n"
        guide += template_class.after_example()
        guide += "\n```\n\n"
        guide += "---\n\n"
    
    return guide

if __name__ == "__main__":
    print("LLM-First Refactoring Templates")
    print("=" * 40)
    
    for template_class in REFACTORING_TEMPLATES:
        print(f"\n{template_class.get_template_name()}")
        print(f"Description: {template_class.get_description()}")
    
    # Generate full guide
    guide = generate_refactoring_guide()
    
    output_path = "/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/llm_first_audit/REFACTORING_GUIDE.md"
    with open(output_path, 'w') as f:
        f.write(guide)
    
    print(f"\nFull refactoring guide saved to: {output_path}")