# OpenRouter LLM Integration Setup

## Overview

The classifier now uses OpenRouter API to intelligently map user questions to Insight IDs (1-18) using an LLM instead of simple keyword matching.

## Setup Steps

### 1. Get OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up / Log in
3. Go to "Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-...`)

### 2. Configure Environment Variables

Add to your `.env` file (or set as environment variables):

```bash
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# LLM Model (choose from OpenRouter's available models)
LLM_MODEL=openai/gpt-3.5-turbo
# Or use other models like:
# LLM_MODEL=anthropic/claude-3-haiku
# LLM_MODEL=google/gemini-pro
# LLM_MODEL=meta-llama/llama-3-8b-instruct
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `openai>=1.12.0` - OpenAI SDK (compatible with OpenRouter)
- `langchain-openai>=0.1.0` - LangChain OpenAI integration

### 4. Test the Integration

Run your application:

```bash
python main.py
# or
python -m uvicorn api_server:app --reload
```

The classifier will automatically use OpenRouter if `OPENROUTER_API_KEY` is set.

## How It Works

1. **User asks a question** → Chat query comes in
2. **Classifier node** → Checks if `OPENROUTER_API_KEY` is configured
3. **If configured**: Calls OpenRouter API with:
   - System prompt describing all 18 insights
   - User's question
   - Requests JSON response with `insight_id`, `confidence`, `reasoning`
4. **If not configured**: Falls back to simple keyword matching
5. **Returns**: Insight ID (1-18) + required metrics

## Example Classification

**User Question:** "Why did we lose money today?"

**LLM Response:**
```json
{
  "insight_id": 17,
  "confidence": 0.95,
  "reasoning": "User is asking about revenue loss, which matches 'Revenue drop root cause chain' (Insight 17)"
}
```

## Available Models on OpenRouter

You can use any model supported by OpenRouter. Popular choices:

- `openai/gpt-3.5-turbo` - Fast, cost-effective
- `openai/gpt-4-turbo` - More accurate, slower
- `anthropic/claude-3-haiku` - Fast, good quality
- `anthropic/claude-3-sonnet` - Better quality
- `google/gemini-pro` - Good balance
- `meta-llama/llama-3-8b-instruct` - Open source option

Check [OpenRouter Models](https://openrouter.ai/models) for full list and pricing.

## Fallback Behavior

If OpenRouter API fails or is not configured:
- Automatically falls back to simple keyword matching
- No errors thrown, system continues to work
- Logs warning message

## Cost Considerations

OpenRouter charges per token. For classification:
- **Input**: ~200-300 tokens (system prompt + user question)
- **Output**: ~50-100 tokens (JSON response)
- **Cost**: Very low (typically $0.0001-0.001 per classification)

For 1000 classifications/day with GPT-3.5-turbo: ~$0.10-0.50/day

## Troubleshooting

### "LLM classification failed"
- Check `OPENROUTER_API_KEY` is set correctly
- Verify API key has credits/balance
- Check network connectivity
- Review logs for specific error

### "Invalid insight_id"
- LLM returned ID outside 1-18 range
- System automatically defaults to ID 1
- Check if insights list in prompt is correct

### "Failed to parse LLM JSON response"
- LLM didn't return valid JSON
- System falls back to keyword matching
- Try a different model or adjust temperature

## Advanced Configuration

### Custom Model Selection

Edit `.env`:
```bash
LLM_MODEL=anthropic/claude-3-sonnet
```

### Adjust Classification Temperature

Edit `src/nodes/classifier.py`, line with `temperature=0.3`:
- Lower (0.1-0.3): More consistent, deterministic
- Higher (0.7-1.0): More creative, varied responses

### Custom System Prompt

Edit the `system_prompt` in `_classify_intent_llm()` function to customize how the LLM classifies questions.

