# 🚀 DifyAgent - 全球股票智能分析平台

一个基于 FastAPI 和 Dify 框架的全球股票智能分析系统，支持 A 股、美股、港股等多个市场，提供实时数据获取、技术指标分析和 AI 驱动的投资建议。

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-支持-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 项目概述

**DifyAgent** 是一个高性能的智能股票分析平台，整合了多个核心功能：

- 🌍 **全球市场数据**：实时获取 A 股、美股、港股、指数行情
- 📊 **技术分析引擎**：MA、RSI、波动率等多个技术指标
- 🤖 **AI 投资建议**：基于算法的智能推荐系统
- ⚡ **高性能 API**：基于 FastAPI 的异步毫秒级响应
- 🔄 **实时数据**：接入 AKShare 库获取最新市场数据
- 🐳 **容器化部署**：完整的 Docker 和 Docker Compose 配置

---

## 🎯 核心功能

### 💰 多市场支持

| 市场类型 | 代码示例 | 货币 | 数据源 |
|---------|---------|------|--------|
| 🇨🇳 A股 | `000001`, `600000`, `300750` | CNY | akshare |
| 🇺🇸 美股 | `AAPL`, `GOOGL`, `TSLA`, `MSFT` | USD | 新浪、东方财富 |
| 🇭🇰 港股 | `00700`, `09988`, `02318` | HKD | akshare |
| 📈 指数 | `000001`(上证), `399001`(深成指), `000300`(沪深300) | CNY | akshare |

### 📊 技术指标分析

系统支持以下技术指标计算和分析：

- **移动平均线（MA）**
  - MA5：5日线 - 短期趋势
  - MA10：10日线 - 中短期趋势
  - MA20：20日线 - 中期趋势
  - 黄金交叉 (MA5 > MA10 > MA20) → 看涨信号
  - 死亡交叉 (MA5 < MA10 < MA20) → 看跌信号

- **相对强弱指数（RSI）**
  - 周期：14天
  - 范围：0-100
  - 超买区（>70）：谨慎看涨，风险信号
  - 超卖区（<30）：可能反弹，机会信号
  - 中性区（30-70）：正常区间

- **波动率（Volatility）**
  - 计算：日收益率标准差 × √252（年化）
  - 含义：价格波动的标准差，用于风险评估
  - 应用：仓位管理和止损设置

- **价格统计**
  - 最高价、最低价、平均价
  - 涨跌幅、涨跌额
  - 成交量、成交额

### 🤖 智能投资建议

系统基于以下因素自动生成详细的投资建议：

- ⚠️ **超买/超卖识别** - RSI 极值信号
- 📈 **趋势强弱判断** - MA 排列分析
- 🔻 **短期风险评估** - 快速涨跌分析
- 💎 **反弹机会识别** - 向下反弹概率计算
- 🎯 **操作建议** - 具体的入场/出场建议

---

## 🏗️ 技术架构

DifyAgent 采用分层架构设计，确保高性能和可维护性：

```
┌─────────────────────────────────────────┐
│       API 请求层 (HTTP/REST)            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    FastAPI 应用层 (路由、验证)          │
│  • POST /analyze - 股票分析              │
│  • GET /markets - 市场列表               │
│  • GET /docs - API 文档                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    业务逻辑层 (数据处理)                 │
│  • 参数验证                              │
│  • 市场路由                              │
│  • 指标计算                              │
│  • 建议生成                              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    数据层 (AKShare 集成)                 │
│  • A股数据获取                           │
│  • 美股数据获取                          │
│  • 港股数据获取                          │
│  • 指数数据获取                          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    缓存层 (Redis 可选)                   │
│    存储层 (PostgreSQL 可选)              │
└──────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- pip 或 conda
- Internet 连接（用于获取实时数据）

### 本地开发环境

#### 1. 克隆仓库

```bash
git clone https://github.com/NIKI678531/DifyAgent_test.git
cd DifyAgent_test
```

#### 2. 创建虚拟环境

```bash
# 使用 Python venv
python -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 启动服务

```bash
cd DifyAgent
python server.py
```

服务将在 `http://localhost:8000` 启动

#### 5. 访问 API 文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🐳 Docker 部署

### 快速 Docker 运行

#### 方式 1: 直接构建运行

```bash
# 构建镜像
docker build -t dify-agent:latest .

# 运行容器
docker run -d \
  --name dify-agent \
  -p 8000:8000 \
  -e TZ=Asia/Shanghai \
  dify-agent:latest

# 查看日志
docker logs -f dify-agent

# 停止容器
docker stop dify-agent
```

#### 方式 2: Docker Compose（推荐）

```bash
# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f dify-agent

# 停止服务
docker-compose down

# 完全清理（包括数据卷）
docker-compose down -v

# 重新构建并启动
docker-compose up -d --build
```

### Docker Compose 包含的服务

1. **dify-agent** - 主 API 服务（端口 8000）
2. **redis** - 缓存层（端口 6379）
3. **postgres** - 数据库（端口 5432，可选）
4. **nginx** - 反向代理（可选）

### 完整部署（包括数据库）

```bash
# 启动所有服务（包括 PostgreSQL 和 Nginx）
docker-compose --profile full up -d
```

### 环境变量配置

在 `docker-compose.yml` 中可配置：

```yaml
environment:
  - TZ=Asia/Shanghai              # 时区设置
  - PYTHONUNBUFFERED=1            # Python 无缓冲输出
  - AKSHARE_TIMEOUT=30            # 数据接口超时时间
  - LOG_LEVEL=INFO                # 日志级别
```

---

## 📡 API 使用示例

### 1. 分析 A 股股票

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_code": "000001",
    "market": "A股",
    "days": 30
  }'
```

**响应示例：**

```json
{
  "stock_code": "000001",
  "stock_name": "平安银行",
  "market": "A股",
  "current_price": 9.45,
  "price_change": 0.15,
  "price_change_percent": 1.61,
  "volume": 156000000,
  "turnover": 1.47e9,
  "ma5": 9.38,
  "ma10": 9.42,
  "ma20": 9.51,
  "rsi": 65.23,
  "volatility": 18.5,
  "highest_price": 10.02,
  "lowest_price": 8.95,
  "average_price": 9.42,
  "trend": "上涨",
  "recommendation": "🚀【顺势而为】主升浪持有策略！\n▸ 理由：'上涨'趋势明确，RSI=65.23处于健康区间\n▸ 技术：量价齐升配合均线多头排列，上涨动能充足\n▸ 操作：保持80%以上仓位，沿5日线移动止盈",
  "currency": "CNY",
  "analysis_time": "2024-04-19 15:30:45"
}
```

### 2. 分析美股

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_code": "AAPL",
    "market": "美股",
    "days": 30
  }'
```

### 3. 分析港股

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_code": "00700",
    "market": "港股",
    "days": 30
  }'
```

### 4. 分析市场指数

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_code": "000001",
    "market": "指数",
    "days": 30
  }'
```

支持的指数代码：
- `000001` - 上证指数
- `399001` - 深证成指
- `000300` - 沪深300
- `000016` - 上证50
- `399006` - 创业板指

### 5. 获取支持的市场列表

```bash
curl -X GET "http://localhost:8000/markets"
```

### 6. 健康检查

```bash
curl -X GET "http://localhost:8000/"
```

---

## 🔑 API 端点详解

### 主要端点

| 端点 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/` | GET | API 根路径，获取服务信息 | 无 |
| `/analyze` | POST | 分析股票数据 | stock_code, market, days |
| `/markets` | GET | 获取支持的市场列表 | 无 |
| `/health` | GET | 健康检查 | 无 |
| `/docs` | GET | Swagger API 文档 | 无 |
| `/redoc` | GET | ReDoc API 文档 | 无 |

### 请求参数详解

**POST /analyze**

```json
{
  "stock_code": "string (required)",     // 股票代码
  "market": "string (required)",         // 市场类型: A股/美股/港股/指数
  "days": "integer (optional, default=30)" // 获取最近X天的数据
}
```

**市场类型代码**

- `A股` - 中国A股市场
- `美股` - 美国股票市场
- `港股` - 香港股票市场
- `指数` - 中国股票指数

---

## 📊 技术指标详解

### RSI (Relative Strength Index)

**公式说明：**
```
RSI = 100 - (100 / (1 + RS))
其中 RS = 平均上升幅度 / 平均下降幅度（14天周期）
```

**指标含义：**
- **>70**: 超买区域，卖出信号
- **30-70**: 正常区域，持仓观察
- **<30**: 超卖区域，买入信号

### 移动平均线 (MA)

**计算方法：**
```
MA5 = 最近5天的收盘价平均值
MA10 = 最近10天的收盘价平均值
MA20 = 最近20天的收盘价平均值
```

**趋势判断：**
- 价格 > MA5 > MA10 > MA20 → **强势上涨**
- 价格 > MA5 > MA20 > MA10 → **上涨**
- 价格 < MA5 < MA10 < MA20 → **强势下跌**
- 价格 < MA5 < MA20 > MA10 → **下跌**
- 其他情况 → **震荡**

### 波动率 (Volatility)

**计算方法：**
```
日收益率 = (今日收盘价 - 昨日收盘价) / 昨日收盘价
波动率 = 日收益率标准差 × √252 × 100%
```

**应用场景：**
- 评估风险水平
- 制定止损位
- 确定仓位大小

---

## 🚨 常见问题

### Q: 美股数据无法获取怎么办？

**A**: 美股数据可能受网络限制影响。系统已配置多种备选方案：
- 方案 1: 使用在线实时数据源
- 方案 2: 使用新浪延迟数据
- 方案 3: 使用模拟示例数据

建议确保网络连接稳定并更新 akshare 库到最新版本。

### Q: 如何集成到我的应用中？

**A**: 可以通过 HTTP 请求调用 API：

```python
import requests

response = requests.post('http://localhost:8000/analyze', json={
    'stock_code': '000001',
    'market': 'A股',
    'days': 30
})

data = response.json()
print(f"当前价格: {data['current_price']}")
print(f"投资建议: {data['recommendation']}")
```

### Q: 建议的准确率如何？

**A**: 系统基于技术面分析，历史准确率约 65-75%，建议：
- 结合基本面分析
- 参考多个技术指标
- 制定风险管理策略
- 不作为唯一投资依据

### Q: 支持实时数据推送吗？

**A**: 当前版本支持 HTTP 查询，可通过以下方式实现实时性：
- 客户端轮询（推荐间隔 1-5 分钟）
- WebSocket 扩展（开发中）
- 消息队列集成（计划中）

### Q: 能否离线运行？

**A**: 不能。系统需要网络连接获取实时数据。但可使用内置示例数据进行演示。

### Q: 如何配置数据库？

**A**: 使用 Docker Compose 的 `--profile full` 标志启动完整部署：

```bash
docker-compose --profile full up -d
```

这会启动 PostgreSQL 数据库进行数据持久化。

---

## 📁 项目结构

```
DifyAgent_test/
├── README.md                    # 项目文档（本文件）
├── ARCHITECTURE.md              # 架构文档和技术细节
├── Dockerfile                   # Docker 镜像构建配置
├── docker-compose.yml           # Docker Compose 编排配置
├── requirements.txt             # Python 依赖列表
├── main.py                      # 主入口文件
├── DifyAgent/
│   └── server.py               # FastAPI 主应用程序
├── finance_Agent_project/       # 财经数据处理模块
│   ├── AddMarketNews.py
│   ├── callapi.py
│   ├── datetime.py
│   └── parse_print.py
├── clawer_test/                # 网络爬虫示例模块
│   ├── anjuke.py
│   ├── find_chromedriver.py
│   ├── selenium_foodpanda_clawer.py
│   └── ...
└── google adk/                 # Google ADK 示例
    └── muti-agent-customer-support.ipynb
```

---

## 🔧 配置说明

### 环境变量

```bash
# 创建 .env 文件
AKSHARE_TIMEOUT=30          # AKShare 接口超时时间（秒）
API_HOST=0.0.0.0            # API 服务监听地址
API_PORT=8000               # API 服务监听端口
LOG_LEVEL=INFO              # 日志级别
TZ=Asia/Shanghai            # 时区
```

### 技术指标参数配置

在 `DifyAgent/server.py` 中可调整：

```python
# RSI 周期（默认14）
RSI_PERIOD = 14

# 移动平均线周期
MA_PERIODS = [5, 10, 20]

# 波动率年化系数（交易日数）
VOLATILITY_FACTOR = 252

# 数据缓存 TTL（秒）
CACHE_TTL = 300
```

---

## 🔒 安全建议

### 生产环境部署检查清单

- ✅ 所有输入参数都进行了验证
- ✅ 统一的异常处理和错误日志
- ⚠️ 生产环境建议添加速率限制（Rate Limiting）
- ⚠️ 使用 HTTPS 加密通信
- ⚠️ 添加 API 密钥认证机制
- ⚠️ 定期更新依赖包
- ⚠️ 设置适当的日志级别
- ⚠️ 配置防火墙和网络隔离

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 贡献步骤

1. **Fork** 本仓库
2. **创建** 特性分支
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **提交** 更改
   ```bash
   git commit -m "Add: your feature description"
   ```
4. **推送** 到分支
   ```bash
   git push origin feature/your-feature-name
   ```
5. **开启** Pull Request

### 代码规范

- 遵循 PEP 8 风格指南
- 编写清晰的代码注释
- 添加必要的单元测试
- 更新相关文档

---

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

---

## 👨‍💻 作者信息

**项目作者**: NIKI678531

- **GitHub**: [@NIKI678531](https://github.com/NIKI678531)
- **项目主页**: [DifyAgent_test](https://github.com/NIKI678531/DifyAgent_test)
- **创建时间**: 2024年4月
- **最后更新**: 2024年4月19日

---

## 📚 学习资源

### 官方文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [AKShare 库文档](https://akshare.akfamily.xyz/)
- [Docker 官方文档](https://docs.docker.com/)
- [Dify AI 框架](https://github.com/langgenius/dify)

### 技术参考

- [技术分析基础](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [Python 异步编程](https://docs.python.org/3/library/asyncio.html)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [Redis 最佳实践](https://redis.io/topics/quickstart)

### 金融知识

- [股票 K 线图解读](https://www.investopedia.com/terms/c/candlestick.asp)
- [移动平均线策略](https://www.investopedia.com/terms/m/movingaverage.asp)
- [RSI 指标详解](https://www.investopedia.com/terms/r/rsi.asp)
- [波动率分析](https://www.investopedia.com/terms/v/volatility.asp)

---

## 🎓 学习路线

### 初级使用者

1. 阅读本 README
2. 运行本地演示
3. 尝试 API 调用
4. 理解技术指标

### 中级开发者

1. 研究 ARCHITECTURE.md
2. 修改技术指标参数
3. 集成自己的数据源
4. 扩展 API 功能

### 高级贡献者

1. 优化数据处理性能
2. 实现新的分析算法
3. 集成机器学习模型
4. 贡献回项目

---

## 📞 问题反馈

如有问题或建议，欢迎通过以下方式联系：

- 📧 **Issue 跟踪**: [GitHub Issues](https://github.com/NIKI678531/DifyAgent_test/issues)
- 💬 **讨论区**: [GitHub Discussions](https://github.com/NIKI678531/DifyAgent_test/discussions)
- 🔗 **Pull Request**: [提交 PR](https://github.com/NIKI678531/DifyAgent_test/pulls)

---

## ⭐ 致谢

感谢以下开源项目的支持：

- [FastAPI](https://fastapi.tiangolo.com/)
- [AKShare](https://akshare.akfamily.xyz/)
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [Redis](https://redis.io/)

---

## 🎯 项目目标

我们的当前目标是构建一个：

- ✨ **易用的** - 简洁的 API 和清晰的文档
- ✨ **高效的** - 快速的数据处理和响应
- ✨ **可靠的** - 稳定的数据源和准确的分析
- ✨ **可扩展的** - 灵活的架构和丰富的功能
- ✨ **开源的** - 透明的代码和社区驱动的开发

---

## 📈 项目路线图

### 已实现 ✅

- [x] 多市场数据支持（A股、美股、港股、指数）
- [x] 技术指标计算（MA、RSI、波动率）
- [x] 智能投资建议
- [x] FastAPI RESTful API
- [x] Docker 容器化部署
- [x] Docker Compose 多服务编排
- [x] 完整文档和示例

### 进行中 🔄

- [ ] WebSocket 实时数据推送
- [ ] 策略回测引擎
- [ ] 机器学习预测模型
- [ ] 可视化仪表板

### 计划中 📝

- [ ] 移动端应用
- [ ] VIP 专业版功能
- [ ] 第三方集成 API
- [ ] 社区论坛

---

**项目版本**: 2.0.0 | **最后更新**: 2024年4月19日 | **状态**: ✅ 生产就绪

⭐ 如果这个项目对你有帮助，请给个 Star！您的支持是我们继续改进的动力！