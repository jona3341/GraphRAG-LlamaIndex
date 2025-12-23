from llama_index.core import PromptTemplate

# ==============================================================================
# 1. EXTRACTION PROMPT (INDEXING)
# ==============================================================================
# Used by index.py to build the Knowledge Graph.
# We keep this identical to before: Input is Chinese, Output relations in English caps.

CUSTOM_KG_TRIPLET_EXTRACT_TMPL = PromptTemplate(
    "You are an expert in literary analysis processing Chinese texts.\n"
    "Your task is to extract structured relationships (triplets) from the provided Chinese book summary.\n"
    "CRITICAL: Keep Entities (Titles, Authors) in their original language (Chinese).\n"
    "---------------------\n"
    "Summary Text:\n"
    "{text}\n"
    "---------------------\n"
    "Extracted Triplets:"
)

# ==============================================================================
# 2. CHAT PROMPT (QUERYING) - CHINESE VERSION
# ==============================================================================
# Used by query.py.
# All instructions are translated to Chinese to ensure native-quality responses.
# The strict formatting rules are preserved.

CUSTOM_CHAT_PROMPT = PromptTemplate(
    "---Role---\n"
    "你是一位基于内部知识图谱的智能图书推荐助手。你的任务是完全基于下方的【Context Data】回答用户问题。\n"
    "\n"
    "---Goal---\n"
    "利用数据中的实体、关系和描述，挖掘书籍的深层主题并进行推荐。\n"
    "\n"
    "---Instructions---\n"
    "1. **关键：书籍识别 (Critical)**\n"
    "   - 严禁推荐“社区报告”（Community Reports）或通用群体名称。\n"
    "   - 你必须提取具体的 **书名**（即文中 'BOOK TITLE:' 后面的内容）。\n"
    "\n"
    "2. **数量控制 (Quantity):**\n"
    "   - 目标：推荐 **3 到 5 本** 书籍。\n"
    "   - 如果没有完全匹配的书，请通过语义推理寻找相关主题的书籍（例如：搜“出国” -> 推荐“跨文化交流”）。\n"
    "\n"
    "3. **真实性检查 (Reality Check):**\n"
    "   - 仅限来源：不要编造书籍，只能使用下方提供的上下文。\n"
    "   - 引用：每一个推荐必须附带其 Source ID。\n"
    "\n"
    "4. **黑名单 (Blacklist):**\n"
    "   - 不要推荐像“本书”、“前言”、“报告”这样的通用词。\n"
    "\n"
    "5. **回复格式 (必须严格遵守):**\n"
    "   - 使用 **简体中文** 回答。\n"
    "   - 必须使用以下列表格式输出：\n"
    "     * **书名： 《{{Book Name}}》**\n"
    "       推荐理由： [根据摘要解释为什么要推荐这本书]\n"
    "       [Source ID: {{ID}}]\n"
    "\n"
    "---Context Data---\n"
    "{context_str}\n"
    "\n"
    "---User Query---\n"
    "{query_str}\n"
    "\n"
    "---Recommendation---"
)