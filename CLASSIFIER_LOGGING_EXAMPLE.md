# Classifier Enhanced Logging - Example Output

## What You'll See in Docker Logs

When you send a chat query like "Why did we lose money?", you'll now see **detailed decision-making logs**:

### Example 1: Simple Keyword Matching (No LLM)

```
--- CLASSIFIER: Processing 'Why did we lose money?' ---
   [Classifier] ───────────────────────────────────────────────────────────
   [Classifier] Classification Method Selection:
   [Classifier] ✗ OpenRouter API key: NOT CONFIGURED
   [Classifier] → Method: Simple keyword matching (fallback mode)
   [Classifier] → To enable LLM, set OPENROUTER_API_KEY environment variable
   [Classifier] ───────────────────────────────────────────────────────────
   [Classifier] Using simple keyword matching for: 'Why did we lose money?'
   [Classifier] Analyzing query for keyword patterns...
   [Classifier] ✓ Found 1 matching pattern(s):
   [Classifier]   [1] Insight 17: Revenue drop root cause chain
   [Classifier]       └─ Matched keywords: lose, money
   [Classifier]       └─ Reasoning: Keywords related to revenue loss or decrease
   [Classifier]
   [Classifier] ════════════════════════════════════════════════════════
   [Classifier] DECISION: Selected Insight 17
   [Classifier] Name: Revenue drop root cause chain
   [Classifier] Matched Keywords: lose, money
   [Classifier] Reasoning: Keywords related to revenue loss or decrease
   [Classifier] ════════════════════════════════════════════════════════
   [Classifier] Returning state update:
   [Classifier]   - mapped_insight_id: 17
   [Classifier]   - insight_name: Revenue drop root cause chain
   [Classifier]   - required_metrics: ['internal_revenue_drop_root_cause_chain']
```

### Example 2: With LLM (OpenRouter)

```
--- CLASSIFIER: Processing 'Why did we lose money?' ---
   [Classifier] ───────────────────────────────────────────────────────────
   [Classifier] Classification Method Selection:
   [Classifier] ✓ OpenRouter API key: CONFIGURED
   [Classifier] → Method: LLM-based classification
   [Classifier] → Model: openai/gpt-3.5-turbo
   [Classifier] ───────────────────────────────────────────────────────────
   [Classifier] Sending request to OpenRouter API...
   [Classifier] Model: openai/gpt-3.5-turbo
   [Classifier] User query: 'Why did we lose money?'
   [Classifier] Received response from LLM
   [Classifier] Raw LLM response: {"insight_id": 17, "confidence": 0.95, "reasoning": "User is asking about revenue loss..."}
   [Classifier] Parsed JSON: {'insight_id': 17, 'confidence': 0.95, 'reasoning': '...'}
   [Classifier] LLM classified as Insight 17 (confidence: 0.95)
   [Classifier] Reasoning: User is asking about revenue loss, which matches 'Revenue drop root cause chain' (Insight 17)
   [Classifier] ✓ LLM classification successful: Insight 17
   [Classifier] Returning state update:
   [Classifier]   - mapped_insight_id: 17
   [Classifier]   - insight_name: Revenue drop root cause chain
   [Classifier]   - required_metrics: [...]
```

## How to See These Logs

### Option 1: Docker (When Network Works)

```bash
# Start Docker
docker-compose up

# In another terminal, send a test query
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Why did we lose money?"}'

# Watch Docker logs
docker-compose logs -f backend
```

### Option 2: Local Development (No Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
python -m uvicorn api_server:app --reload

# In another terminal, send query
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Why did we lose money?"}'
```

### Option 3: Test Classifier Directly

```bash
# Install dependencies first
pip install -r requirements.txt

# Then run test
python3 test_classifier_logging.py
```

## What the Logs Show

✅ **Method Selection**: LLM vs Simple Matching  
✅ **Query Analysis**: What patterns were checked  
✅ **Matched Keywords**: Exact words that triggered the match  
✅ **Decision Process**: Why Insight 17 was chosen  
✅ **Final Result**: Insight ID, name, and required metrics  

## Understanding the Decision

For query: **"Why did we lose money?"**

1. **Keywords Found**: "lose", "money"
2. **Pattern Matched**: Insight 17 (Revenue drop root cause chain)
3. **Reasoning**: Keywords related to revenue loss or decrease
4. **Decision**: Selected Insight 17

The logs now show **exactly** how the classifier made its decision!

