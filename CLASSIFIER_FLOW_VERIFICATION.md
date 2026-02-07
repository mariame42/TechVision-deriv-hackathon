# Classifier Flow Verification

## Flow Diagram

```
User Query (Frontend)
    ↓
API Server (/api/chat/query)
    ↓
Creates State: {request_type: "chat_query", user_query: "..."}
    ↓
LangGraph Workflow.invoke(state)
    ↓
Dispatcher Node → Routes to "classifier" (because request_type == "chat_query")
    ↓
Classifier Node (node_classifier)
    ↓
├─ Gets user_query from state ✓
├─ Checks for OPENROUTER_API_KEY ✓
├─ If key exists:
│   └─ Calls _classify_intent_llm()
│       ├─ Sends query to OpenRouter API ✓
│       ├─ Receives JSON: {insight_id, confidence, reasoning} ✓
│       └─ Returns insight_id (1-18) ✓
└─ If no key:
    └─ Calls _classify_intent_simple() (keyword matching)
    ↓
Returns State Update:
{
    mapped_insight_id: <1-18>,
    insight_name: "<name>",
    required_metrics: [<list of metrics>]
}
    ↓
Next Node: Hybrid Fetcher (uses required_metrics)
```

## Verification Checklist

### ✅ Step 1: Message Received
**Location:** `api_server.py:149`
```python
user_query: request.user_query  # ✓ Gets message from API request
```

### ✅ Step 2: State Created
**Location:** `api_server.py:146-159`
```python
state: AgentState = {
    "request_type": "chat_query",  # ✓ Correct type
    "user_query": request.user_query,  # ✓ Message included
    ...
}
```

### ✅ Step 3: Workflow Routes to Classifier
**Location:** `src/graph/workflow.py:45-47`
```python
def route_request(state: AgentState) -> str:
    return "batch_loader" if state["request_type"] == "dashboard_load" else "classifier"
    # ✓ Routes to "classifier" for chat_query
```

### ✅ Step 4: Classifier Gets Message
**Location:** `src/nodes/classifier.py:28`
```python
query = state.get("user_query", "")  # ✓ Extracts message from state
```

### ✅ Step 5: Checks for LLM
**Location:** `src/nodes/classifier.py:34`
```python
if settings.openrouter_api_key:  # ✓ Checks if API key exists
```

### ✅ Step 6: Sends to LLM (if key exists)
**Location:** `src/nodes/classifier.py:121-129`
```python
response = client.chat.completions.create(
    model=settings.llm_model or "openai/gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},  # ✓ System prompt with all insights
        {"role": "user", "content": user_prompt}  # ✓ User's query
    ],
    response_format={"type": "json_object"},  # ✓ Forces JSON output
)
```

### ✅ Step 7: Parses LLM Response
**Location:** `src/nodes/classifier.py:132-133`
```python
content = response.choices[0].message.content  # ✓ Gets response
result = json.loads(content)  # ✓ Parses JSON
insight_id = result.get("insight_id", 1)  # ✓ Extracts insight_id
```

### ✅ Step 8: Returns State Update
**Location:** `src/nodes/classifier.py:65-69`
```python
return {
    "mapped_insight_id": insight_id,  # ✓ Returns insight ID
    "insight_name": name,  # ✓ Returns insight name
    "required_metrics": required_metrics,  # ✓ Returns metrics list
}
```

## How to Test

### Option 1: Check Logs
When you send a chat query, you should see these logs:

```
--- CLASSIFIER: Processing 'Why did we lose money?' ---
   [Classifier] OpenRouter API key found, using LLM classification
   [Classifier] Sending request to OpenRouter API...
   [Classifier] Model: openai/gpt-3.5-turbo
   [Classifier] User query: 'Why did we lose money?'
   [Classifier] Received response from LLM
   [Classifier] Raw LLM response: {"insight_id": 17, "confidence": 0.95, ...}
   [Classifier] Parsed JSON: {'insight_id': 17, 'confidence': 0.95, ...}
   [Classifier] LLM classified as Insight 17 (confidence: 0.95)
   [Classifier] Returning state update:
   [Classifier]   - mapped_insight_id: 17
   [Classifier]   - insight_name: Revenue drop root cause chain
   [Classifier]   - required_metrics: [...]
```

### Option 2: Test via API
```bash
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Why did we lose money today?"}'
```

Check the backend logs for the classifier output.

### Option 3: Check Environment
```bash
# Check if OpenRouter key is set
echo $OPENROUTER_API_KEY

# Or check in Python
python3 -c "from src.config.settings import get_settings; s = get_settings(); print('API Key:', 'SET' if s.openrouter_api_key else 'NOT SET')"
```

## Common Issues

### Issue 1: Classifier Not Being Called
**Symptom:** No "--- CLASSIFIER: Processing..." log
**Check:**
- Is `request_type` set to `"chat_query"`? (not `"dashboard_load"`)
- Is the workflow routing correctly?

### Issue 2: LLM Not Being Called
**Symptom:** See "No OpenRouter API key found" log
**Fix:**
```bash
export OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### Issue 3: LLM Returns Invalid JSON
**Symptom:** "Failed to parse LLM JSON response" error
**Check:**
- Model supports JSON mode (most do)
- Response format is correct

### Issue 4: Wrong Insight ID
**Symptom:** Returns insight_id outside 1-18 range
**Fix:** Already handled - defaults to 1 if invalid

## Expected Behavior

✅ **With OpenRouter API Key:**
- Uses LLM classification
- Sends query to OpenRouter
- Gets structured JSON response
- Returns insight_id, name, and metrics

✅ **Without OpenRouter API Key:**
- Uses simple keyword matching
- Still returns valid insight_id
- System continues to work

## Verification Commands

```bash
# 1. Check if classifier is in workflow
grep -r "node_classifier" src/graph/workflow.py

# 2. Check if classifier gets user_query
grep -A 5 "user_query" src/nodes/classifier.py

# 3. Check if LLM is called
grep -A 10 "openrouter_api_key" src/nodes/classifier.py

# 4. Check return values
grep -A 5 "mapped_insight_id" src/nodes/classifier.py
```

