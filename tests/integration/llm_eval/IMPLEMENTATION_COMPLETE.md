# LLM 评估系统 - OpenCode 集成完成

## 实现总结

已成功为 LLM 评估系统添加了真正调用 OpenCode 的功能。系统现在支持两种模式：

### 1. **模拟模式**（Simulated Mode）
- 默认模式，无需外部依赖
- 使用规则基础的评估逻辑
- 快速执行，适合开发和 CI/CD

### 2. **OpenCode 模式**（OpenCode Mode）
- 真正调用 OpenCode API
- 实际 LLM 推理和评估
- 更准确但需要运行的 OpenCode 实例

## 新增文件

### 1. `config.yaml`
主配置文件，管理所有设置：
- 执行模式选择（simulated / opencode）
- Executor（实例1）配置
  - API 端点
  - 模型配置
  - 认证设置
- Evaluator（实例2）配置
  - API 端点
  - 模型配置
  - 评估标准权重
  - 认证设置
- Mock Server 配置
- 输出配置

### 2. `config.py`
配置管理模块：
- 配置加载和验证
- 数据类定义
- 全局配置访问

### 3. `opencode_client.py`
OpenCode API 客户端：
- `OpenCodeClient` - 基础客户端类
- `OpenCodeExecutorClient` - Executor 客户端
- `OpenCodeEvaluatorClient` - Evaluator 客户端
- HTTP 请求处理
- 认证支持
- 健康检查

### 4. `config.opencode.yaml`
OpenCode 配置示例：
- 完整的 OpenCode 集成配置
- 带详细注释
- 可直接复制使用

### 5. `OPENCODE_INTEGRATION.md`
OpenCode 集成文档：
- 详细使用说明
- API 规范
- 认证配置
- 故障排除
- Token 使用估算

## 更新文件

### 1. `executor.py`
添加 OpenCode 支持：
- `mode` 参数（simulated / opencode）
- `_execute_opencode()` - 使用 OpenCode API 执行
- `_execute_simulated()` - 原有模拟执行
- 自动模式选择
- 健康检查

### 2. `evaluator.py`
添加 OpenCode 支持：
- `mode` 参数（simulated / opencode）
- `_evaluate_opencode()` - 使用 OpenCode API 评估
- `_evaluate_simulated()` - 原有模拟评估
- 自动模式选择
- 健康检查

### 3. `test_runner.py`
集成配置系统：
- 从 `config.yaml` 加载配置
- 根据配置初始化 executor 和 evaluator
- 新增 `--config` 参数支持自定义配置文件
- 自动显示运行模式

### 4. `EXECUTION_GUIDE.md`
更新执行指南：
- 添加配置章节
- OpenCode 集成章节
- 混合模式说明
- Token 使用估算
- 配置参考

## 使用方法

### 默认模式（模拟）

```bash
cd tests/integration
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json
```

### OpenCode 模式

1. **配置 OpenCode**：

```bash
# 复制示例配置
cp llm_eval/config.opencode.yaml llm_eval/my_config.yaml

# 编辑配置文件
vim llm_eval/my_config.yaml

# 更新以下内容：
# - api_endpoint: 你的 OpenCode 地址
# - auth.token: 你的认证 token
```

2. **验证连接**：

```bash
cd tests/integration/llm_eval
python3 -c "
from config import get_config
from opencode_client import create_executor_client, create_evaluator_client

config = get_config('my_config.yaml')
executor = create_executor_client(config.executor)
evaluator = create_evaluator_client(config.evaluator)

print('Executor:', executor.health_check())
print('Evaluator:', evaluator.health_check())
"
```

3. **运行测试**：

```bash
cd tests/integration
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --config llm_eval/my_config.yaml
```

### 混合模式

可以混合使用两种模式，例如：
- Executor 使用 OpenCode（真实 LLM 推理）
- Evaluator 使用模拟（快速评估）

```yaml
executor:
  mode: opencode
  api_endpoint: http://localhost:8080
  # ...

evaluator:
  mode: simulated  # 使用模拟评估
```

优点：
- 获得真实 LLM 推理
- 评估仍然很快
- 减少 token 使用量

## OpenCode API 规范

系统期望的 OpenCode API 接口：

### Executor 端点

**POST** `/v1/execute`

请求：
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.7,
  "max_tokens": 4096,
  "prompt": "用户命令",
  "system_prompt": "系统提示",
  "context": {
    "test_id": "...",
    "skill_path": "...",
    "rpc_config": {...}
  },
  "enable_tracing": true
}
```

响应：
```json
{
  "response": "执行结果",
  "tracing": {
    "reasoning_chain": [...],
    "tool_calls": [...],
    "rpc_interactions": [...]
  },
  "error": null
}
```

### Evaluator 端点

**POST** `/v1/execute`

请求：
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "prompt": "包含执行记录的评估提示",
  "enable_tracing": false
}
```

响应：
```json
{
  "response": "{\"judgment\": {...}, \"criteria_scores\": {...}, ...}"
}
```

### 健康检查

**GET** `/health`

响应：`200 OK`

## 认证支持

### 无认证
```yaml
auth:
  type: none
```

### Bearer Token
```yaml
auth:
  type: bearer
  token: "your-token"
```

发送：`Authorization: Bearer your-token`

### API Key
```yaml
auth:
  type: api_key
  token: "your-api-key"
  api_key_header: "X-API-Key"
```

发送：`X-API-Key: your-api-key`

## Token 使用估算

### 每个测试
- Executor: 500-2000 tokens
- Evaluator: 800-3000 tokens
- **总计: ~1500-5000 tokens/测试**

### 完整测试套件（30 个测试）
- **总计: ~45,000-150,000 tokens**
- 成本取决于模型定价

### 成本优化建议
1. 开发时使用模拟模式
2. 仅测试特定里程碑
3. 使用混合模式
4. 修复后只运行失败的测试

## 文件结构

```
tests/integration/llm_eval/
├── config.yaml                    # 默认配置（模拟模式）
├── config.opencode.yaml           # OpenCode 配置示例
├── config.py                      # 配置管理
├── opencode_client.py             # OpenCode API 客户端
├── executor.py                    # Executor（支持 OpenCode）
├── evaluator.py                   # Evaluator（支持 OpenCode）
├── test_runner.py                 # 测试运行器（集成配置）
├── EXECUTION_GUIDE.md             # 执行指南（已更新）
├── OPENCODE_INTEGRATION.md        # OpenCode 集成文档
└── ... (其他文件)
```

## 依赖

新增 Python 包依赖（需要添加到 requirements.txt）：
- `pyyaml` - YAML 配置文件解析
- `requests` - HTTP 客户端

```bash
pip install pyyaml requests
```

## 测试

### 测试配置加载
```bash
cd tests/integration/llm_eval
python3 config.py
```

### 测试 OpenCode 客户端
```bash
python3 opencode_client.py
```

### 运行示例（模拟模式）
```bash
python3 example.py
```

## 下一步

建议的后续工作：

1. **添加更多错误处理**
   - OpenCode API 失败重试
   - 超时处理优化
   - 更详细的错误信息

2. **性能优化**
   - 并行执行多个测试
   - 缓存 OpenCode 响应
   - 连接池

3. **监控和日志**
   - 详细的 API 调用日志
   - Token 使用统计
   - 性能指标

4. **集成测试**
   - 添加 OpenCode 模式的集成测试
   - Mock OpenCode API 进行单元测试

## 总结

✅ 已完成：
- 配置文件系统（`config.yaml`）
- OpenCode API 客户端（`opencode_client.py`）
- Executor OpenCode 支持
- Evaluator OpenCode 支持
- 测试运行器集成
- 完整文档
- 示例配置

✅ 特性：
- 支持模拟和 OpenCode 两种模式
- 支持混合模式（部分使用 OpenCode）
- 灵活的认证配置
- 健康检查
- 详细的错误处理
- 完整的文档和示例

系统现在可以：
1. **开发时**：使用模拟模式快速测试
2. **生产验证时**：使用 OpenCode 模式获得真实 LLM 评估
3. **成本优化时**：使用混合模式平衡准确性和成本
