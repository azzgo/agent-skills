# OpenCode Integration - README

This directory contains configuration and code for integrating real OpenCode API with the LLM evaluation system.

## Files

- `config.yaml` - Default configuration (simulated mode)
- `config.opencode.yaml` - Example OpenCode integration configuration
- `config.py` - Configuration loader and validation
- `opencode_client.py` - OpenCode API client implementation
- `executor.py` - Executor with OpenCode support
- `evaluator.py` - Evaluator with OpenCode support

## Quick Start with OpenCode

### 1. Prerequisites

- Running OpenCode instance(s) accessible via HTTP
- API tokens/keys (if authentication required)
- Network connectivity to OpenCode endpoints

### 2. Configure OpenCode

Copy the example config:

```bash
cp config.opencode.yaml my_opencode_config.yaml
```

Edit `my_opencode_config.yaml`:

```yaml
execution_mode: opencode

executor:
  mode: opencode
  api_endpoint: http://your-opencode-host:8080  # Update this
  model:
    name: claude-3-5-sonnet-20241022
  auth:
    type: bearer
    token: "your-token"  # Update this

evaluator:
  mode: opencode
  api_endpoint: http://your-opencode-host:8081  # Update this
  model:
    name: claude-3-5-sonnet-20241022
  auth:
    type: bearer
    token: "your-token"  # Update this
```

### 3. Test Connectivity

```bash
python3 -c "
from config import get_config
from opencode_client import create_executor_client, create_evaluator_client

config = get_config('my_opencode_config.yaml')

executor = create_executor_client(config.executor)
evaluator = create_evaluator_client(config.evaluator)

print('Executor health:', executor.health_check())
print('Evaluator health:', evaluator.health_check())
"
```

### 4. Run Tests

```bash
cd tests/integration
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --config llm_eval/my_opencode_config.yaml
```

## Configuration Options

### Execution Modes

1. **simulated** (default):
   - No external dependencies
   - Fast, rule-based evaluation
   - Good for development/CI

2. **opencode**:
   - Real OpenCode API calls
   - Actual LLM reasoning and evaluation
   - Higher accuracy but slower and uses tokens

### Mixed Mode

You can use different modes for executor and evaluator:

```yaml
executor:
  mode: opencode  # Real LLM execution

evaluator:
  mode: simulated  # Fast rule-based evaluation
```

Benefits:
- Real LLM reasoning but fast evaluation
- Lower token usage
- Good for development

## OpenCode API Specification

### Executor Endpoint

**POST** `/v1/execute`

Request:
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.7,
  "max_tokens": 4096,
  "prompt": "user command",
  "system_prompt": "skill context and instructions",
  "context": {
    "test_id": "milestone1_add_uri_001",
    "skill_path": "/path/to/skill",
    "rpc_config": {"host": "localhost", "port": 6800}
  },
  "enable_tracing": true
}
```

Response:
```json
{
  "response": "execution result",
  "tracing": {
    "reasoning_chain": [
      {"step": 1, "thought": "...", "tool_called": {...}}
    ],
    "tool_calls": [
      {"tool": "bash", "command": "...", "output": "..."}
    ],
    "rpc_interactions": [
      {"method": "aria2.addUri", "request": {...}, "response": {...}}
    ]
  },
  "error": null
}
```

### Evaluator Endpoint

**POST** `/v1/execute`

Request:
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.3,
  "max_tokens": 4096,
  "prompt": "evaluation prompt with execution record",
  "enable_tracing": false
}
```

Response:
```json
{
  "response": "{\"judgment\": {...}, \"criteria_scores\": {...}, ...}"
}
```

The response should contain a JSON string with evaluation results.

### Health Check

**GET** `/health`

Response: `200 OK` if healthy

## Authentication

### No Authentication

```yaml
auth:
  type: none
```

### Bearer Token

```yaml
auth:
  type: bearer
  token: "your-bearer-token"
```

Sends: `Authorization: Bearer your-bearer-token`

### API Key

```yaml
auth:
  type: api_key
  token: "your-api-key"
  api_key_header: "X-API-Key"
```

Sends: `X-API-Key: your-api-key`

## Token Usage

### Estimated per Test

- Executor: 500-2000 tokens
- Evaluator: 800-3000 tokens
- **Total: ~1500-5000 tokens/test**

### Full Suite (30 tests)

- **Total: ~45,000-150,000 tokens**
- Cost depends on model pricing

### Cost Optimization

1. Use simulated mode for development
2. Test specific milestones only
3. Use mixed mode (OpenCode executor + simulated evaluator)
4. Run failed tests only

## Troubleshooting

### Connection Refused

```
ConnectionError: Failed to connect to OpenCode API at http://localhost:8080
```

**Solutions:**
- Verify OpenCode is running
- Check endpoint URL in config
- Verify network connectivity
- Check firewall rules

### Authentication Failed

```
OpenCode API returned error: 401 Unauthorized
```

**Solutions:**
- Verify auth token is correct
- Check auth type (bearer vs api_key)
- Verify token hasn't expired

### Timeout

```
OpenCode API request timed out after 60s
```

**Solutions:**
- Increase timeout in config
- Check OpenCode performance
- Verify model is loaded

### Health Check Fails

```
Health check: False
```

**Solutions:**
- Verify OpenCode `/health` endpoint exists
- Check OpenCode logs
- Try accessing endpoint manually: `curl http://localhost:8080/health`

## Examples

### Full OpenCode Mode

```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --config llm_eval/config.opencode.yaml
```

### Mixed Mode (OpenCode Executor Only)

```bash
# Edit config to set:
# executor.mode: opencode
# evaluator.mode: simulated

python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --config llm_eval/mixed_config.yaml
```

### Single Milestone with OpenCode

```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --milestone "Milestone 1" \
  --config llm_eval/config.opencode.yaml
```

## Development

### Testing OpenCode Client

```bash
cd tests/integration/llm_eval
python3 opencode_client.py
```

### Testing Configuration

```bash
python3 config.py
```

## See Also

- `EXECUTION_GUIDE.md` - General execution guide
- `README.md` - Complete documentation
- `IMPLEMENTATION_SUMMARY.md` - Architecture details
