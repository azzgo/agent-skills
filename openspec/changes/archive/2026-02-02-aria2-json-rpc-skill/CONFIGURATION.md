# Configuration Guide - aria2 JSON-RPC Skill

## 📁 Configuration Location

**Only one location**: `skills/aria2-json-rpc/config.json`

This avoids conflicts with aria2's own configuration files:
- ❌ NOT `.aria2rc` (may conflict with aria2 config)
- ❌ NOT `~/.aria2/` (aria2 default config directory)
- ❌ NOT `/etc/aria2/` (aria2 system config)
- ✅ ONLY `skills/aria2-json-rpc/config.json`

---

## 🔧 Configuration Sources (Simplified)

Only **two** sources are supported:

### 1. JSON Config File

**Location**: `skills/aria2-json-rpc/config.json`

**Example**:
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "my-secret-token",
  "secure": false,
  "timeout": 30000
}
```

**Fields**:
- `host` (string, required): Aria2 RPC host address
- `port` (number, required): Aria2 RPC port
- `secret` (string|null, optional): RPC secret token (null = no auth)
- `secure` (boolean, optional): Use HTTPS (default: false)
- `timeout` (number, optional): Request timeout in milliseconds (default: 30000)

### 2. Environment Variables

```bash
export ARIA2_RPC_HOST=localhost
export ARIA2_RPC_PORT=6800
export ARIA2_RPC_SECRET=my-secret-token
export ARIA2_RPC_SECURE=false
```

**Priority**: Environment variables > config.json > defaults

---

## ✅ Configuration Validation

**Validation happens before EVERY RPC call**:

### 1. Configuration Loading Check
- Verify config.json exists and is valid JSON
- Verify environment variables are properly formatted
- Apply priority: env vars > config.json > defaults

### 2. Required Fields Check
- `host` must be a non-empty string
- `port` must be a valid number (1-65535)

### 3. Format Validation
- `host`: Must be a valid hostname or IP address
- `port`: Must be numeric, between 1-65535
- `secret`: String or null (null = no authentication)
- `secure`: Boolean (true/false)
- `timeout`: Positive number in milliseconds

### 4. Connection Test
- Attempt to connect to aria2 endpoint
- Verify aria2 is responsive
- Verify authentication (if secret is configured)
- Only proceed with RPC call if validation passes

### 5. Error Messages

**Invalid JSON**:
```
Error: Configuration file parsing failed
Location: skills/aria2-json-rpc/config.json
Reason: Unexpected token } in JSON at position 42
```

**Missing Required Fields**:
```
Error: Configuration validation failed
Missing required fields: host, port
Example valid config:
{
  "host": "localhost",
  "port": 6800
}
```

**Connection Test Failed**:
```
Error: Unable to connect to aria2
Host: localhost
Port: 6800
Reason: Connection refused
Please ensure aria2 daemon is running with RPC enabled:
  aria2c --enable-rpc --rpc-listen-all=true=true
```

---

## 🚀 First-Time Setup

When no configuration is found, the skill provides interactive guidance:

```
🚀 aria2 JSON-RPC Skill 初始化
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

检测到这是第一次使用 aria2 skill。

请提供 aria2 RPC 配置信息：
1. aria2 主机地址 [默认: localhost]: 192.168.1.100
2. aria2 RPC 端口 [默认: 6800]: 6800
3. RPC 密钥（可选，直接回车跳过）: my-secret-token
4. 使用 HTTPS? [y/N]: n

✅ 配置已保存到: skills/aria2-json-rpc/config.json
🔗 正在测试连接...
✅ 连接成功！现在可以使用 aria2 skill 了。
```

---

## 🔄 Configuration Reload

### Automatic Reload
- When `config.json` is modified, skill detects and reloads
- Applies new configuration without disconnecting (if possible)

### Manual Reload
```
$ opencode "重载 aria2 配置"
✅ 配置已从 config.json 重载
✅ 连接测试成功
```

### Reload Error Handling
- If new config is invalid, keep previous valid config
- Provide error details for fixing the invalid config

---

## 📋 Configuration Examples

### Example 1: Local aria2 (No Authentication)
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false
}
```

### Example 2: Remote aria2 with Authentication
```json
{
  "host": "192.168.1.100",
  "port": 6800,
  "secret": "my-secret-token",
  "secure": false
}
```

### Example 3: aria2 over HTTPS
```json
{
  "host": "aria2.example.com",
  "port": 443,
  "secret": "my-secret-token",
  "secure": true
}
```

### Example 4: Custom Timeout
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false,
  "timeout": 60000
}
```

---

## 🚫 What is NOT Supported

To avoid complexity and conflicts:

- ❌ INI format (.aria2.conf)
- ❌ YAML format
- ❌ TOML format
- ❌ .env files
- ❌ User global config (~/.aria2/config.json)
- ❌ System config (/etc/aria2/)
- ❌ Multiple config file formats (priority resolution)
- ❌ Config files outside skill directory

---

## 🔐 Security Best Practices

1. **Never commit config.json to git**
   ```bash
   echo "skills/aria2-json-rpc/config.json" >> .gitignore
   ```

2. **Use environment variables for secrets**
   ```bash
   export ARIA2_RPC_SECRET=my-secret-token
   # In config.json, use null
   "secret": null
   ```

3. **Set proper file permissions**
   ```bash
   chmod 600 skills/aria2-json-rpc/config.json
   ```

4. **Use HTTPS for remote aria2**
   ```json
   {
     "host": "aria2.example.com",
     "secure": true
   }
   ```

---

## 📝 Configuration File Format

**Strict JSON format only**:

✅ **Valid**:
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false
}
```

❌ **Invalid** (trailing comma):
```json
{
  "host": "localhost",
  "port": 6800,
}
```

❌ **Invalid** (comments not supported):
```json
{
  "host": "localhost", // This is invalid JSON
  "port": 6800
}
```

❌ **Invalid** (single quotes):
```json
{
  'host': 'localhost',
  'port': 6800
}
```

---

## 🎯 Quick Start

### Method 1: Interactive Setup
```bash
# First use - skill will prompt for configuration
$ opencode "下载 https://example.com/file.iso"
# Follow interactive prompts, config saved to skills/aria2-json-rpc/config.json
```

### Method 2: Manual Config
```bash
# Create config file manually
cat > skills/aria2-json-rpc/config.json <<EOF
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false
}
EOF

# Start using skill
$ opencode "下载 https://example.com/file.iso"
```

### Method 3: Environment Variables
```bash
# Set environment variables
export ARIA2_RPC_HOST=localhost
export ARIA2_RPC_PORT=6800

# Start using skill (no config file needed)
$ opencode "下载 https://example.com/file.iso"
```

---

## 🔍 Troubleshooting

### Issue: "Configuration file parsing failed"
**Solution**: Check JSON syntax using online validator or `jq`:
```bash
jq . skills/aria2-json-rpc/config.json
```

### Issue: "Unable to connect to aria2"
**Solution**:
1. Verify aria2 is running: `ps aux | grep aria2c`
2. Verify RPC is enabled: `aria2c --enable-rpc`
3. Check firewall rules
4. Verify host and port in config

### Issue: "Authentication failed"
**Solution**:
1. Verify secret matches aria2 configuration
2. Check aria2 secret in aria2.conf: `rpc-secret=my-secret-token`
3. Remove secret in config.json if aria2 has no authentication

### Issue: "Configuration validation failed"
**Solution**:
1. Ensure required fields (host, port) are present
2. Verify port is numeric and between 1-65535
3. Check data types: host=string, port=number, secret=string|null, secure=boolean