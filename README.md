# GraphRAG Book Recommendation System

基于 LlamaIndex 的知识图谱检索增强生成 (GraphRAG) 图书推荐系统，使用 DeepSeek LLM 和 BGE-M3 嵌入模型构建。

## 项目简介

本项目实现了一个智能图书推荐系统，通过构建知识图谱来理解书籍之间的关系和主题相似性，为用户提供精准的图书推荐。系统使用 DeepSeek 大语言模型进行关系抽取和回答生成，结合 BGE-M3 嵌入模型实现混合搜索（向量 + 图谱）。

## 主要特性

- **知识图谱构建**: 自动从图书摘要中抽取实体关系，构建结构化知识图谱
- **混合搜索**: 结合向量相似度和图谱关系进行检索
- **中文支持**: 专为中文图书数据优化，支持中文查询和回答
- **DeepSeek 集成**: 使用 DeepSeek-V3 模型进行关系抽取和智能回答
- **高效索引**: 支持持久化存储，避免重复构建

## 技术栈

- **框架**: LlamaIndex
- **LLM**: DeepSeek-V3 (via OpenAI-like API)
- **嵌入模型**: BGE-M3 (BAAI/bge-m3)
- **存储**: 本地文件系统持久化
- **数据处理**: Pandas
- **开发语言**: Python 3.8+

## 环境要求

### 系统要求
- Python 3.8 或更高版本
- 至少 8GB RAM（推荐 16GB+）
- 支持 CUDA 的 GPU（可选，用于加速嵌入计算）

### API 密钥
需要获取 DeepSeek API 密钥：
1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
2. 注册账号并获取 API Key
3. 在项目根目录创建 `.env` 文件：
```
DEEPSEEK_API_KEY=your_api_key_here
```

## 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd GraphRAG-LlamaIndex
```

2. **创建虚拟环境**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirement.txt
```

4. **环境配置**
- 确保 `.env` 文件包含有效的 DeepSeek API 密钥
- 项目会自动配置 HuggingFace 镜像加速下载模型

## 数据准备

项目使用 CSV 格式的数据文件，位于 `data/clean_data_100.csv`。数据格式要求：

```csv
book_id,book_name,book_summary
0002009,铸工入门,本书结合我国铸造生产的实际情况...
```

- `book_id`: 书籍唯一标识符
- `book_name`: 书名
- `book_summary`: 书籍摘要/描述

## 使用方法

### 1. 构建知识图谱

首次运行需要构建索引（这会调用 DeepSeek API，可能需要几分钟）：

```bash
python index.py
```

构建完成后，索引会保存到 `storage_graph_csv/` 目录。

### 2. 启动推荐系统

构建索引后，启动交互式查询界面：

```bash
python query.py
```

### 3. 交互查询

系统启动后，您可以输入自然语言查询，例如：
- "推荐一些关于人工智能的书籍"
- "我想看历史类的图书"
- "推荐编程入门书籍"

系统会返回 3-5 本相关书籍的推荐，每本包含：
- 书名
- 推荐理由
- 来源 ID

## 项目结构

```
GraphRAG LlamaIndex/
├── index.py              # 知识图谱构建脚本
├── query.py              # 交互式查询界面
├── requirement.txt       # Python 依赖
├── .env                 # 环境变量配置（需要手动创建）
├── data/
│   └── clean_data_100.csv    # 图书数据
├── src/
│   ├── config.py        # 模型配置
│   ├── loader.py        # 数据加载器
│   └── prompts.py       # 自定义提示模板
└── storage_graph_csv/   # 索引存储目录（运行后生成）
```

## 配置说明

### 模型参数

在 `src/config.py` 中可以调整：
- **LLM 参数**: 温度、最大 token 数等
- **嵌入模型**: BGE-M3 模型选择
- **分块大小**: 文本分块策略

### 检索参数

在 `query.py` 中可以调整：
- `similarity_top_k`: 检索相似度最高的 k 个结果
- `max_triplets_per_chunk`: 每个文本块最多抽取的关系数

## 故障排除

### 常见问题

1. **CUDA 不可用**
   - 系统会自动回退到 CPU 模式
   - 首次运行 BGE-M3 模型下载可能较慢

2. **API 密钥错误**
   - 检查 `.env` 文件是否存在
   - 确认 DeepSeek API 密钥有效

3. **索引构建失败**
   - 检查数据文件路径是否正确
   - 确认网络连接正常（需要访问 DeepSeek API）

4. **内存不足**
   - 减小 `max_triplets_per_chunk` 参数
   - 使用更小的分块大小

### 日志调试

运行时添加详细日志：
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 性能优化

- **GPU 加速**: 确保安装了 PyTorch CUDA 版本
- **批量处理**: 调整数据加载批次大小
- **缓存优化**: 模型下载后会自动缓存

## 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

- [LlamaIndex](https://www.llamaindex.ai/) - 强大的 RAG 框架
- [DeepSeek](https://deepseek.com/) - 优秀的中文大语言模型
- [BAAI](https://www.baai.ac.cn/) - BGE-M3 嵌入模型提供者

