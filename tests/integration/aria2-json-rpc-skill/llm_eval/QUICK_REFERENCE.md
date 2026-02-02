# LLM 评估系统 - 快速参考

## 文件概览

### 配置文件
- `config.yaml` - 默认配置（模拟模式）
- `config.opencode.yaml` - OpenCode 配置示例
- `config.py` - 配置加载器（325 行）

### 核心模块
- `opencode_client.py` - OpenCode API 客户端（435 行）
- `executor.py` - 执行器（支持模拟/OpenCode）
- `evaluator.py` - 评估器（支持模拟/OpenCode）
- `test_runner.py` - 测试运行器（集成配置）

### 文档
- `EXECUTION_GUIDE.md` - 执行指南（已更新 OpenCode 集成）
- `OPENCODE_INTEGRATION.md` - OpenCode 集成详细文档
- `IMPLEMENTATION_COMPLETE.md` - 实现总结
- `README.md` - 完整文档

## 快速开始

### 1. 模拟模式（默认，无需配置）

```bash
cd tests/integration
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json
```

### 2. OpenCode 模式

```bash
# 1. 配置
cp llm_eval/config.opencode.yaml llm_eval/my_config.yaml
vim llm_eval/my_config.yaml  # 编辑 API 端点和 token

# 2. 测试连接
cd llm_eval
python3 -c "from config import get_config; from opencode_client import create_executor_client; print(create_executor_client(get_config('my_config.yaml').executor).health_check())"

# 3. 运行测试
cd ..
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --config llm_eval/my_config.yaml
```

## 配置要点

### 模拟模式（simulated）
```yaml
execution_mode: simulated
executor:
  mode: simulated
evaluator:
  mode: simulated
```
- ✅ 快速
- ✅ 无外部依赖
- ✅ 适合开发/CI
- ❌ 规则基础评估

### OpenCode 模式（opencode）
```yaml
execution_mode: opencode
executor:
  mode: opencode
  api_endpoint: http://localhost:8080
  auth:
    type: bearer
    token: "your-token"
evaluator:
  mode: opencode
  api_endpoint: http://localhost:8081
  auth:
    type: bearer
    token: "your-token"
```
- ✅ 真实 LLM 推理
- ✅ 更准确的评估
- ❌ 需要 OpenCode 实例
- ❌ 使用 tokens（有成本）

### 混合模式（推荐）
```yaml
executor:
  mode: opencode  # 真实 LLM 推理
evaluator:
  mode: simulated  # 快速评估
```
- ✅ 真实推理
- ✅ 快速评估
- ✅ 降低成本

## 常用命令

```bash
# 运行所有测试
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json

# 运行特定里程碑
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --milestone "Milestone 1"

# 使用自定义配置
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --config my_config.yaml

# 使用已运行的 mock server
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --no-server --port 6800

# 仅生成报告
python3 -m llm_eval.report_generator results/

# 查看结果
cat results/reports/test_report.txt
cat results/reports/analysis_report.json | jq .
```

## OpenCode API 端点

### Executor
- **端点**: `POST /v1/execute`
- **功能**: 执行用户命令，获取推理追踪
- **输入**: prompt, system_prompt, context, enable_tracing
- **输出**: response, tracing (reasoning_chain, tool_calls, rpc_interactions)

### Evaluator
- **端点**: `POST /v1/execute`
- **功能**: 评估执行记录
- **输入**: prompt (包含执行记录)
- **输出**: response (JSON 格式的评估结果)

### 健康检查
- **端点**: `GET /health`
- **输出**: `200 OK`

## 认证方式

### 无认证
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
→ `Authorization: Bearer your-bearer-token`

### API Key
```yaml
auth:
  type: api_key
  token: "your-api-key"
  api_key_header: "X-API-Key"
```
→ `X-API-Key: your-api-key`

## Token 使用估算

| 场景 | Tokens/测试 | 30 测试总计 |
|------|------------|------------|
| 仅 Executor | 500-2000 | 15K-60K |
| 仅 Evaluator | 800-3000 | 24K-90K |
| **两者都用** | **1500-5000** | **45K-150K** |
| 混合模式 | 500-2000 | 15K-60K |

## 故障排除

### 连接失败
```
ConnectionError: Failed to connect to OpenCode API
```
→ 检查 OpenCode 是否运行，验证 endpoint URL

### 认证失败
```
401 Unauthorized
```
→ 验证 token，检查 auth type

### 超时
```
OpenCode API request timed out
```
→ 增加 config 中的 timeout，检查 OpenCode 性能

### 健康检查失败
```
Health check: False
```
→ 验证 `/health` 端点存在，检查 OpenCode 日志

## 依赖安装

```bash
pip install pyyaml requests
```

## 目录结构

```
tests/integration/llm_eval/
├── config.yaml                    # 默认配置
├── config.opencode.yaml           # OpenCode 示例
├── config.py                      # 配置管理
├── opencode_client.py             # API 客户端
├── executor.py                    # 执行器
├── evaluator.py                   # 评估器
├── test_runner.py                 # 运行器
├── EXECUTION_GUIDE.md             # 执行指南
├── OPENCODE_INTEGRATION.md        # 集成文档
├── IMPLEMENTATION_COMPLETE.md     # 实现总结
└── QUICK_REFERENCE.md             # 本文件
```

## 下一步

1. **开发/测试**: 使用模拟模式
2. **验证功能**: 使用混合模式（OpenCode executor + 模拟 evaluator）
3. **生产评估**: 使用完整 OpenCode 模式
4. **成本优化**: 仅对失败的测试使用 OpenCode

## 获取帮助

- 执行指南: `EXECUTION_GUIDE.md`
- OpenCode 集成: `OPENCODE_INTEGRATION.md`
- 完整文档: `README.md`
- 架构详情: `IMPLEMENTATION_SUMMARY.md`
