# OpenRouter Model ID Fix

## Problem

The error `'gemini-pro is not a valid model ID'` occurs because OpenRouter requires model IDs in the format:
- ✅ `openai/gpt-3.5-turbo`
- ✅ `google/gemini-pro`
- ✅ `anthropic/claude-3-haiku`
- ❌ `gemini-pro` (missing provider prefix)

## Solution

### Option 1: Add to .env (Recommended)

Add this to your `.env` file:

```bash
LLM_MODEL=openai/gpt-3.5-turbo
```

Or use other models:
```bash
# Fast and cheap
LLM_MODEL=openai/gpt-3.5-turbo

# Better quality
LLM_MODEL=openai/gpt-4-turbo

# Google Gemini
LLM_MODEL=google/gemini-pro

# Claude (fast)
LLM_MODEL=anthropic/claude-3-haiku

# Claude (better)
LLM_MODEL=anthropic/claude-3-sonnet
```

### Option 2: Use Default (Already Fixed)

The code now defaults to `openai/gpt-3.5-turbo` which is a valid OpenRouter model ID.

## Valid OpenRouter Model Formats

All models must include the provider prefix:

- `openai/gpt-3.5-turbo`
- `openai/gpt-4-turbo`
- `google/gemini-pro`
- `google/gemini-pro-vision`
- `anthropic/claude-3-haiku`
- `anthropic/claude-3-sonnet`
- `meta-llama/llama-3-8b-instruct`

See full list: https://openrouter.ai/models

## After Fixing

1. **Add to .env** (if you want a specific model):
   ```bash
   echo "LLM_MODEL=openai/gpt-3.5-turbo" >> .env
   ```

2. **Restart Docker**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

3. **Test**: Send a query and check logs - should see:
   ```
   [Classifier] ✓ OpenRouter API key: CONFIGURED
   [Classifier] → Model: openai/gpt-3.5-turbo
   [Classifier] Sending request to OpenRouter API...
   [Classifier] Received response from LLM
   ```

## Automatic Fix

The code now automatically converts models without provider prefix:
- `gemini-pro` → `openai/gemini-pro` (with warning)
- But it's better to use the correct format: `google/gemini-pro`

