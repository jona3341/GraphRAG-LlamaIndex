from llama_index.core import PromptTemplate

# ==============================================================================
# 1. EXTRACTION PROMPT (INDEXING) - RESTE INCHANGÉ
# ==============================================================================
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
# 2. CHAT PROMPT (QUERYING) - VERSION 100% CHINOISE (FORCÉE)
# ==============================================================================
# J'ai traduit toutes les instructions systèmes en chinois.
# Cela empêche le modèle de "glisser" vers l'anglais.

CUSTOM_CHAT_PROMPT = PromptTemplate(
    "### 角色设定\n"
    "你是一位基于内部知识图谱的智能图书推荐助手。你的任务是完全基于下方的【上下文数据】（Context Data）回答用户问题。\n"
    "\n"
    "### 核心目标\n"
    "利用数据中的实体、关系和描述，挖掘书籍的深层主题并进行推荐。\n"
    "\n"
    "### 操作指令 (Instructions)\n"
    "1. **书籍识别 (关键)**\n"
    "   - 严禁推荐“社区报告”或通用群体名称。\n"
    "   - 你必须提取具体的 **书名**（即文中 'BOOK TITLE:' 后面的内容）。\n"
    "\n"
    "2. **数量控制**\n"
    "   - 目标：推荐 **3 到 5 本** 书籍。\n"
    "   - 如果没有完全匹配的书，请通过语义推理寻找相关主题的书籍。\n"
    "\n"
    "3. **真实性检查**\n"
    "   - 不要编造书籍，只能使用下方提供的上下文。\n"
    "   - 每一个推荐必须附带其 Source ID。\n"
    "\n"
    "4. **语言与格式 (强制执行)**\n"
    "   - **必须使用简体中文回答**。\n"
    "   - 即使上下文中的关系词是英文（如 'Contains'），你也要在回答中用中文表述。\n"
    "   - 必须严格遵守以下列表格式输出：\n"
    "\n"
    " 书名： 《{{Book Name}}\n"
    " 推荐理由： [用中文解释推荐理由]\n"
    " [Source ID: {{ID}}]\n"
    "\n"
    "### 上下文数据 (Context Data)\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "\n"
    "### 用户问题 (User Query)\n"
    "{query_str}\n"
    "\n"
    "### 你的推荐 (请用中文):"
)