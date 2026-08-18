Customer Service Agent

一个面向运营商与企业客服场景的 LLM Agent 工程实践项目。

本项目以真实客服业务为背景，目标不是简单实现一个聊天机器人，而是逐步构建一个能够：

理解用户意图
提取业务参数
维护多轮会话
检索企业知识
调用业务工具
根据工具结果继续决策
自动生成客服回复
必要时转人工

的企业级智能客服 Agent。

项目最终目标：

LLM
 ↓
Intent Understanding
 ↓
Structured Output
 ↓
Tool Calling
 ↓
RAG
 ↓
Memory
 ↓
Agent Workflow
 ↓
LangGraph
 ↓
Evaluation
 ↓
Production Engineering
1. 项目最终目标

最终构建一个具备真实业务落地能力的 Enterprise Customer Service Agent。

整体架构：

                         用户
                          |
                          v
                    +-------------+
                    |  FastAPI    |
                    |    API      |
                    +------+------+
                           |
                           v
                  +----------------+
                  |  Agent / LLM   |
                  |                |
                  | 意图理解       |
                  | 参数提取       |
                  | 决策           |
                  | 回复生成       |
                  +-------+--------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v

       Tools             RAG          Memory

          |               |               |

          v               v               v

    余额查询          企业知识库       会话状态
    订单查询          Vector DB        用户上下文
    创建工单
    转人工

                          |
                          v

                   LangGraph Workflow

                          |
                          v

                    Evaluation

                          |
                          v

                 Production Service
2. 项目业务场景

项目模拟运营商 / 企业客服常见业务。

2.1 查询账户余额

用户：

我的余额还有多少？

Agent：

理解意图
 ↓
调用 query_balance()
 ↓
返回余额信息
2.2 查询订单

用户：

我的订单现在到哪里了？

Agent：

理解订单查询需求
 ↓
调用 query_order()
 ↓
返回订单状态
2.3 企业知识问答

用户：

退款多久到账？

Agent：

用户问题
 ↓
RAG 检索知识库
 ↓
找到退款规则
 ↓
LLM 生成回答

知识库包含：

产品说明
业务规则
办理流程
常见问题
企业内部知识
2.4 创建工单

用户：

我的问题一直没有解决，帮我提交工单。

Agent：

理解用户诉求
 ↓
调用 create_ticket()
 ↓
返回工单编号
2.5 转人工

用户：

帮我转人工客服。

Agent：

判断需要人工介入
 ↓
调用 escalate_to_human()
 ↓
进入人工流程
3. Agent 最终工作流程

最终 Agent 不只是：

用户输入
    |
    v
关键词匹配
    |
    v
返回答案

而应该是：

用户问题

    |

    v

LLM 理解用户需求

    |

    v

提取 Intent 和 Parameters

    |

    v

判断下一步动作

    |
    +----------------+
    |                |
    v                v

直接回答        调用 Tool / RAG

                    |

                    v

              获取执行结果

                    |

                    v

              返回给 LLM

                    |

                    v

              生成最终回复
4. 当前项目状态
已完成
 Python 项目基础结构
 FastAPI API 服务
 Agent 基础框架
 Rule-based Intent Routing
 Customer Tools
 基础知识库
 本地 Qwen2.5-3B-Instruct 接入
 基础测试
当前阶段

正在进行：

 使用 Qwen 替代关键词判断
 LLM Intent Classification
 Structured Output
 参数提取
后续阶段
 Tool Calling
 Agent Loop
 RAG
 Embedding
 Vector Database
 Memory
 LangGraph
 Evaluation
 Docker
 CI/CD
5. 项目核心理念

本项目遵循：

学习原理
    ↓
最小实验
    ↓
接入客服 Agent
    ↓
测试验证
    ↓
工程化

不为了学习框架而学习框架。

所有技术必须回答：

这个技术在最终客服 Agent 中解决什么问题？

6. LLM 能力

LLM 是 Agent 的核心“大脑”。

当前使用：

Qwen2.5-3B-Instruct

通过 Transformers 在本地运行。

LLM 最终负责：

自然语言
    ↓
理解
    ↓
Intent 判断
    ↓
参数提取
    ↓
任务规划
    ↓
调用 Tool / RAG
    ↓
生成最终回复
7. Intent 理解

当前版本：

用户输入
    ↓
关键词匹配
    ↓
确定 Intent
    ↓
执行对应逻辑

例如：

用户：

我的余额还有多少？

当前：

balance
    ↓
query_balance()

这种方式的问题：

无法理解复杂表达
维护成本高
泛化能力差

例如：

我刚充值的钱为什么还没有到账？

关键词可能无法判断真实需求。

最终升级目标：

用户：

我上次充值的钱为什么还没到账？

        ↓

Qwen

        ↓

{
    "intent": "recharge",
    "parameters": {
        "issue": "recharge_not_received"
    }
}

最终：

由 LLM 理解用户，而不是依赖大量 if/else。

8. Structured Output

为了让 LLM 稳定参与 Agent 决策，需要让模型输出结构化数据。

例如：

{
  "intent": "order_query",
  "parameters": {
    "order_id": "123456"
  },
  "need_tool": true
}

Structured Output 解决：

LLM 输出格式不稳定
无法直接被程序处理
参数缺失
字段错误

后续学习：

JSON Output
JSON Schema
Structured Output
参数校验
输出异常处理

9. Tool Calling

Tool Calling 是整个 Agent 最重要的能力之一。

传统程序：

用户输入

↓

代码判断

↓

调用固定函数

↓

返回结果

Agent 模式：

用户输入

↓

LLM 理解需求

↓

决定是否需要调用工具

↓

选择 Tool

↓

传递参数

↓

获取结果

↓

继续生成回答

完整流程：

用户：

帮我查一下余额

↓

LLM

↓

判断需要调用：

query_balance()

↓

Tool 执行

↓

返回：

{
    "balance": 50
}

↓

LLM

↓

生成：

您的当前余额为 50 元。
Tool 设计原则

所有 Tool 应该保持统一结构。

例如：

{
  "success": true,
  "data": {},
  "message": "",
  "error_code": null
}

避免：

不同 Tool

↓

不同返回格式

↓

Agent 无法统一处理
当前规划 Tool

目录：

app/tools/

计划实现：

query_balance()

query_order()

create_ticket()

escalate_to_human()

未来可以连接真实业务系统：

CRM

订单系统

客户资料系统

工单系统

运营商业务系统

数据库 API
10. RAG

客服场景中，大量问题来自企业知识。

例如：

退款规则

套餐说明

产品介绍

办理流程

业务限制

常见问题

这些信息不应该全部依赖 LLM 自己记忆。

因此需要 RAG。

RAG 基本流程
企业文档

↓

Document Loader

↓

文本切分 Chunk

↓

Embedding

↓

向量数据库

↓

用户问题

↓

相似度搜索

↓

召回相关知识

↓

加入 Prompt

↓

LLM 生成回答
RAG 解决的问题
1. 降低幻觉

没有 RAG：

用户：

退款多久到账？

LLM：

根据训练数据猜测

风险：

信息过期
编造答案
不符合企业规则

有 RAG：

用户：

退款多久到账？

↓

搜索企业退款规则

↓

找到：

退款通常 3-5 个工作日

↓

LLM 根据知识回答
RAG 学习重点

后续学习：

Document Loader
Text Splitter
Chunk 策略
Embedding
Vector Database
Similarity Search
Top-K Retrieval
Reranking
Context Management
RAG Evaluation
11. Memory

真实客服不是一次问答。

用户可能连续沟通：

用户：

我的订单什么时候到？

Agent：

请提供订单号。

用户：

123456

Agent：

订单正在配送。

用户：

那预计多久到？

最后一句：

"那预计多久到？"

如果没有 Memory：

Agent 不知道：

什么订单
什么上下文
Memory 保存内容

最终需要保存：

Conversation History

Session State

User Context

Current Intent

Extracted Parameters

Tool Results

Task Status
Memory 类型
短期记忆

当前会话：

最近几轮聊天

例如：

订单号

用户问题

Agent 回复
长期记忆

用户画像：

例如：

用户 ID

历史订单

历史问题

偏好
12. Agent State

传统 Chat：

user_input -> response

简单。

但是 Agent 需要保存运行状态。

例如：

state = {
    "messages": [],

    "user_id": "",

    "session_id": "",

    "intent": "",

    "parameters": {},

    "tool_calls": [],

    "tool_results": [],

    "retrieved_documents": [],

    "response": ""
}
为什么需要 State？

因为 Agent 可能：

理解问题

↓

调用 Tool

↓

获得结果

↓

继续判断

↓

调用另一个 Tool

↓

生成回复

中间过程必须保存。

State 是后续 LangGraph 的核心。

13. LangGraph

当 Agent 复杂后：

简单代码：

if intent == "balance":

    query_balance()

elif intent == "order":

    query_order()

会越来越难维护。

LangGraph 使用 Workflow 管理 Agent。

核心概念：

State

Node

Edge

Conditional Edge

Tool Node

Agent Loop
LangGraph 工作流

目标：

                  START

                    |

                    v

              +-----------+
              |   Agent   |
              +-----+-----+

                    |

        +-----------+-----------+

        |                       |

        v                       v

      Tool                    RAG

        |                       |

        +-----------+-----------+

                    |

                    v

              Tool Result

                    |

                    v

              Agent 判断

                    |

          +---------+---------+

          |                   |

          v                   v

       Continue             END

LangGraph 解决的问题
Agent 流程可视化
状态管理
多步骤任务
条件分支
Human Handoff
Debug
14. Human Handoff

智能客服不是所有问题都应该自动解决。

优秀 Agent 必须知道：

什么时候应该停止。

转人工场景

例如：

用户主动要求
我要人工客服
AI 多次失败
用户：

重复描述问题

↓

AI 连续无法解决
高风险业务

例如：

账户安全

投诉升级

重大故障
Tool 失败

例如：

CRM 查询失败

订单系统异常

最终流程：

AI 可以解决

        ↓

自动处理

AI 无法解决

        ↓

转人工
15. Evaluation

一个真正的 Agent 不能靠感觉评价。

需要建立量化指标。

Intent Accuracy

判断：

用户真实意图

VS

Agent 判断意图

例如：

100 个测试问题：

正确 95 个

Intent Accuracy：

95%

Tool Selection Accuracy

判断：

应该调用：

query_order()

但是 Agent 调用了：

query_balance()

属于错误。

Tool Argument Accuracy

例如：

用户：

查询订单 123456

Agent：

{
 "order_id":"123456"
}

正确。

RAG Evaluation

关注：

是否召回正确文档
是否遗漏关键知识
是否引入无关信息
Answer Quality

评价：

正确性
完整性
是否幻觉
是否符合客服语气
Task Completion Rate

例如：

测试 100 个任务：

成功完成 90 个。

那么：

Task Completion Rate = 90%
16. 工程化

最终目标：

不是一个只能本地运行的 Demo。

而是：

生产级 AI 应用

需要逐步加入：

FastAPI

配置管理

日志系统

异常处理

Retry

Timeout

Docker

CI/CD

Monitoring

Security

Rate Limit

最终架构：
Client
↓
API Gateway
↓
FastAPI
↓
Agent Service
↓
LLM
↓
RAG / Tools
↓
Business Systems

17. 项目目录

当前项目结构：

customer-service-agent/
│
├── app/
│   │
│   ├── agent/
│   │   └── customer_agent.py
│   │
│   ├── api/
│   │   └── server.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── llm/
│   │   └── qwen_client.py
│   │
│   ├── rag/
│   │   └── knowledge_base.py
│   │
│   └── tools/
│       └── customer_tools.py
│
├── data/
│   └── knowledge/
│       └── faqs.txt
│
├── tests/
│   ├── test_customer_agent.py
│   └── test_customer_api.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

随着项目演进，最终目录目标：

app/
│
├── agent/
│
├── api/
│
├── config/
│
├── llm/
│
├── rag/
│   ├── loader/
│   ├── splitter/
│   ├── embedding/
│   ├── retriever/
│   └── pipeline/
│
├── memory/
│
├── tools/
│
├── workflow/
│
├── evaluation/
│
└── services/
18. API

当前项目使用 FastAPI。

Health Check

接口：

GET /health

用途：

服务状态检查
部署健康检测
Chat API

接口：

POST /api/chat

请求：

{
  "message": "查询我的余额"
}

未来支持：

{
  "session_id": "session-001",
  "user_id": "user-001",
  "message": "帮我查一下订单"
}

响应：

{
  "success": true,
  "session_id": "session-001",
  "intent": "order_query",
  "message": "您的订单正在配送中。",
  "tool_calls": [],
  "sources": []
}
19. 本地运行
创建虚拟环境
python -m venv venv
激活虚拟环境

Windows PowerShell：

.\venv\Scripts\Activate.ps1
安装依赖
pip install -r requirements.txt
启动服务
uvicorn app.api.server:app --reload

访问：

http://127.0.0.1:8000

FastAPI 文档：

http://127.0.0.1:8000/docs

运行测试：

python -m unittest discover tests
20. 技术栈
技术	用途
Python	核心开发语言
FastAPI	AI 应用 API 服务
Transformers	LLM 推理
Qwen2.5-3B-Instruct	本地大语言模型
Prompt Engineering	控制 LLM 行为
Structured Output	结构化输出
Tool Calling	Agent 工具调用
RAG	企业知识库问答
Embedding	文本向量化
Vector Database	语义检索
LangGraph	Agent Workflow
unittest	自动化测试
Git	版本管理
GitHub	项目托管
Docker	容器化部署
21. 项目开发路线

项目按照阶段持续开发。

Phase 1：基础 Agent

状态：

已完成

完成：

 Python 项目结构
 FastAPI
 Agent 基础结构
 Rule-based Intent Routing
 Customer Tools
 基础 Knowledge Base
 本地 Qwen 接入
 基础测试
Phase 2：LLM Agent

当前阶段。

目标：

使用 LLM 替代规则判断。

任务：

 Qwen Intent Classification
 Prompt Engineering
 Structured Output
 JSON Schema
 参数提取
 LLM Decision
Phase 3：Tool Calling

目标：

让 Agent 自主选择工具。

任务：

 Tool Schema
 Function Calling
 Tool Selection
 Tool Arguments
 Tool Result
 LLM + Tool Loop
 Tool Error Handling
Phase 4：RAG

目标：

实现企业知识库问答。

任务：

 Document Loader
 Chunking
 Embedding
 Vector Database
 Semantic Search
 Top-K Retrieval
 Reranking
 RAG Generation
 Retrieval Evaluation
Phase 5：Memory

目标：

支持真实多轮客服。

任务：

 Message History
 Session State
 Short-term Memory
 User Context
 Multi-turn Conversation
 Context Management
Phase 6：LangGraph Agent

目标：

构建可控 Agent Workflow。

任务：

 State
 Node
 Edge
 Conditional Routing
 Tool Node
 RAG Node
 Agent Loop
 Human Handoff
Phase 7：Evaluation

目标：

建立 Agent 质量评估体系。

任务：

 Intent Accuracy
 Structured Output Accuracy
 Tool Selection Accuracy
 Tool Argument Accuracy
 RAG Recall
 RAG Precision
 Answer Quality
 Task Completion Rate
 Human Handoff Accuracy
Phase 8：工程化

目标：

达到生产部署能力。

任务：

 Logging
 Error Handling
 Retry
 Timeout
 Configuration Management
 Docker
 CI/CD
 Monitoring
 Security
 Rate Limiting
22. 学习原则

本项目采用：

学习知识
    ↓
最小实验
    ↓
接入客服 Agent
    ↓
测试验证
    ↓
工程化

不为了学习框架而学习框架。

所有技术必须回答：

这个技术在最终客服 Agent 中解决什么问题？

例如：

学习 Embedding

不是为了记住：

Embedding = 向量

而是为了实现：

用户问题

↓

Embedding

↓

知识库搜索

↓

找到相关企业知识

↓

LLM 回答
学习 Tool Calling

不是为了知道 API 格式。

而是为了实现：

用户：

查询余额

↓

LLM

↓

query_balance()

↓

返回结果

↓

客服回复
学习 Memory

不是为了学习 Memory API。

而是为了实现：

用户：

我的订单什么时候到？

Agent：

请提供订单号。

用户：

123456。

Agent：

订单正在配送。

用户：

预计多久？
学习 LangGraph

不是为了学习框架。

而是为了组织：

Agent

↓

Tool

↓

Tool Result

↓

RAG

↓

Agent

↓

Human Handoff

形成可维护 Workflow。

23. 最终项目能力

项目完成后，希望具备：

                  Customer Service Agent

                           |

        +------------------+------------------+

        |                  |                  |

        v                  v                  v

       LLM              Tools               RAG

        |                  |                  |

        |          +-------+-------+          |

        |          |       |       |          |

        |          v       v       v          |

        |        余额    订单    工单          |

        |                                      |

        |                              Embedding

        |                                      |

        +--------------------------------------+

                           |

                         Memory

                           |

                       LangGraph

                           |

                      Evaluation

                           |

                         API

                           |

                      Deployment

最终重点不是：

会调用大模型 API

而是：

懂业务

+

懂 LLM

+

懂 Agent

+

懂 RAG

+

懂 Tool

+

懂 Workflow

+

懂 Evaluation

+

懂工程化
24. 最终学习目标

通过这个项目，最终具备：

需求分析

↓

业务建模

↓

Agent Architecture Design

↓

LLM 接入

↓

Prompt Design

↓

Structured Output

↓

Tool Calling

↓

RAG

↓

Memory

↓

Agent Workflow

↓

Evaluation

↓

API

↓

Docker

↓

Deployment

↓

Monitoring

最终目标：

能够独立设计、开发、调试和交付一个具备真实业务落地能力的 AI Agent 应用。

25. 项目定位

这是一个持续迭代的：

Enterprise Customer Service Agent

项目。

最终希望体现的不只是：

会 Python

会调用大模型 API

会使用 LangChain / LangGraph

而是：

懂业务

+

懂 LLM

+

懂 Agent

+

懂 RAG

+

懂 Tool

+

懂 Workflow

+

懂 Evaluation

+

懂工程化

最终形成完整能力：

AI Agent 应用开发与交付能力。