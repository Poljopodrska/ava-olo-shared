# 📜 AVA OLO CONSTITUTIONAL PRINCIPLES

## CORE PHILOSOPHY
These 15 rules are MANDATORY for all development. Every decision must comply with ALL principles.

## 🆕 AMENDMENT #13 - COUNTRY-BASED LOCALIZATION
See CONSTITUTIONAL_AMENDMENT_13.md for full details. Core principle:
- WhatsApp number determines farmer's country automatically
- System localizes all responses for that specific country
- Information follows hierarchy: FARMER → COUNTRY → GLOBAL

### 🥭 MANGO RULE: Universal Scalability
- Everything must work for any crop in any country
- "Would this work for mango in Bulgaria?" is the ultimate test
- No hardcoded Croatian/regional patterns allowed
- LLM intelligence handles all language/crop variations

### 🗄️ POSTGRESQL ONLY: Single Database
- Database: farmer_crm on AWS RDS PostgreSQL
- Connection: AWS environment variables (DB_HOST, DB_NAME, etc.)
- NO SQLite, NO multiple databases, NO exceptions
- All modules use same AWS RDS connection

### 🧠 LLM-FIRST: Maximum AI Intelligence
- Minimal coding + Maximum LLM intelligence
- Let GPT-4 handle complexity, not hardcoded rules
- Trust AI over pattern matching
- Simple prompts > Complex bypass systems

### 🏗️ MODULE INDEPENDENCE: Isolated Components
- Each module must work independently
- Working on RAG cannot break database operations
- Working on UI cannot break LLM routing
- Bulletproof separation prevents cascading failures

### 🔒 PRIVACY-FIRST: Personal Data Protection
- Personal farm data NEVER goes to external APIs
- Farmer information stays internal (database/RAG only)
- External search (Perplexity) only for general knowledge
- Clean separation of personal vs public data

### ⚡ API-FIRST: Standardized Communication
- All modules communicate through standardized APIs
- No direct function imports between modules
- Clean interfaces prevent coupling disasters
- Each module has defined contracts

### 🛡️ ERROR ISOLATION: Graceful Degradation
- One module failure cannot crash the system
- Always provide fallback responses
- System stays operational even with partial failures
- User never sees "system down" messages

### 📊 TRANSPARENCY: Complete Monitoring
- All LLM decisions must be logged and explainable
- Complete audit trail for agricultural operations
- Real-time monitoring of system health
- Every operation tracked in llm_debug_log

### 🌾 FARMER-CENTRIC: Appropriate Communication
- Every response in farmer's preferred language
- Professional agricultural tone (not "overly sweet")
- Contextually appropriate communication
- Respect agricultural expertise

### 🔄 PRODUCTION-READY: Scalable Architecture
- Every component must be scalable from day one
- WhatsApp-ready design
- Multi-farmer, multi-country capable
- No "toy" implementations

### 📝 CONFIGURATION: Settings Over Hardcoding
- Country/language settings via configuration
- No hardcoded regional logic in code
- Easy expansion to new markets
- All parameters in config files

### 🧪 TEST-DRIVEN: Validation Required
- "Prosaro PHI" test must always pass
- Every change validated against core agricultural scenarios
- Performance benchmarks maintained
- Constitutional compliance verified

### 🌍 COUNTRY-AWARE LOCALIZATION: WhatsApp-Driven Intelligence
- WhatsApp number determines farmer's country (phone prefix)
- System auto-localizes for that specific country
- All responses tailored to farmer's location context
- LLM intelligence handles country-specific agricultural practices
- Information hierarchy: FARMER → COUNTRY → GLOBAL

### 🎨 DESIGN-FIRST: Constitutional Design System
- All AVA OLO features MUST follow the constitutional design template
- Brown & olive agricultural color palette (exact hex values required)
- Typography: 18px+ minimum for older farmers accessibility
- Enter key functionality mandatory on ALL inputs
- Mobile-first responsive design with constitutional badges
- Atomic structure logo implementation required
- Philosophy: Functionality ALWAYS before beauty
- ERROR-level enforcement: Build fails if design violated

### 🧠 AMENDMENT #15 - LLM-GENERATED INTELLIGENCE
- LLM generates 95%+ of business logic, database queries, and responses
- Zero custom coding for specific farming scenarios
- Universal conversation engine handles ANY crop, ANY question automatically
- System adapts to watermelon, Bulgarian mango, and unknown crops without code changes
- Constitutional directive: "If the LLM can write it, don't code it"
- Maximum AI intelligence + Minimal universal execution engines
- Revolutionary zero-code approach for agricultural conversations

## CONSTITUTIONAL COMPLIANCE CHECK
Before ANY development work:
1. Read this constitution completely
2. Ensure your approach follows ALL 15 principles
3. Test mango compliance: "Would this work in Bulgaria?"
4. Verify module independence
5. Confirm privacy protection
6. Check country-based localization works
7. Validate LLM-generated intelligence compliance (Amendment #15)

## VIOLATION CONSEQUENCES
- Constitutional violations delay deployment
- Breaks scalability to international markets
- Creates maintenance burden
- Undermines architectural integrity

REMEMBER: These principles prevent the problems you've experienced and ensure global scalability!