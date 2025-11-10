"""
RAG 服务模块
负责文档加载、向量化、检索和 AI 生成
"""
import os
import json
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from openai import OpenAI
from config import (
    SURVEY_DATA_FILE, CHROMA_DIR, OPENAI_API_KEY, OPENAI_BASE_URL,
    AI_MODEL, MAX_TOKENS, TEMPERATURE, CHUNK_SIZE, CHUNK_OVERLAP, SIMILARITY_TOP_K
)


class RAGService:
    """RAG 问卷生成服务"""

    def __init__(self):
        """初始化 RAG 服务"""
        # 设置 OpenAI 环境变量
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        os.environ['OPENAI_BASE_URL'] = OPENAI_BASE_URL

        # 初始化向量数据库
        self.vectordb = None
        self.client = OpenAI()
        self._initialize_vectordb()

    def _initialize_vectordb(self):
        """初始化向量数据库"""
        try:
            # 检查是否已有持久化的向量数据库
            if CHROMA_DIR.exists() and len(list(CHROMA_DIR.iterdir())) > 0:
                # 加载已有的向量数据库
                embedding = OpenAIEmbeddings()
                self.vectordb = Chroma(
                    persist_directory=str(CHROMA_DIR),
                    embedding_function=embedding
                )
                print("✓ 向量数据库加载成功")
            else:
                # 创建新的向量数据库
                self._create_vectordb()
        except Exception as e:
            print(f"向量数据库加载失败，尝试重新创建: {e}")
            self._create_vectordb()

    def _create_vectordb(self):
        """创建新的向量数据库"""
        print("正在创建向量数据库...")

        # 加载问卷文本文件
        loader = TextLoader(str(SURVEY_DATA_FILE), encoding='utf-8')
        documents = loader.load()

        # 文档分块
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        splits = text_splitter.split_documents(documents)

        # 创建向量数据库
        embedding = OpenAIEmbeddings()
        self.vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embedding,
            persist_directory=str(CHROMA_DIR)
        )

        print(f"✓ 向量数据库创建成功，共 {len(splits)} 个文档块")

    def _search_similar_surveys(self, query: str) -> str:
        """
        检索相似的历史问卷

        Args:
            query: 用户需求描述

        Returns:
            拼接后的历史问卷文本
        """
        # 相似性搜索
        docs = self.vectordb.similarity_search(query, k=SIMILARITY_TOP_K)

        # 拼接检索结果
        all_contents = ""
        for i, doc in enumerate(docs):
            content = f"问卷{i+1}. {doc.page_content}\n"
            all_contents += content

        # 清理格式
        all_contents = all_contents.replace('""', '"')
        return all_contents

    def _build_system_prompt(self, reference_content: str) -> str:
        """
        构建系统提示词

        Args:
            reference_content: 检索到的历史问卷参考内容

        Returns:
            完整的系统提示词
        """
        return f"""
# Role
你是一名互联网金融领域定量用户研究专家，能根据业务方需求，参考问卷库里的问卷设计资料，给出符合业务方需求和用户研究专业规范的问卷设计。不要回答任何其他方面的问题。

## Background
公司中各个业务线会有不同的调研需求，需要通过问卷调研的方式，进行满意度/NPS调研、功能优化调研、功能需求调研、用户画像调研等不同类型的调研。因此需要你进行出色的问卷设计，来满足相应的业务方需求。

## Goals
根据业务方的具体需求和问卷库中的相似问卷，给出最佳问卷设计。

## Skills
1. 优秀的信息整理和总结归纳能力。
2. 卓越的对具体业务需求的理解能力。
3. 熟练掌握用户研究基础知识，精通问卷调研专业知识，遵守用户研究规范。
4. 对互联网金融领域的业务知识非常了解，能设计出具有深度的问卷。

## Constraints
1. 你的分析和思考必须结合业务方给的客观需求，不能胡编乱造。
2. 问卷问题类型主要包括：单选题、多选题、文本题，其中单选题需要在问题之后标注【单选】、多选题需要在问题之后标注【可多选】、文本题无需在问题之后进行特别标注。
3. 对于满意度/NPS调研，使用5点量表，选项顺序为从低到高（非常不满意——非常满意、强烈不推荐——强烈推荐）。
4. 选项设计必须符合MECE原则，即"相互独立，完全穷尽"，当无法穷尽所有可能的选项时，必须添加"其他"选项。
5. 问题和选项的设计必须保持中立，无倾向性、引导性。
6. 问卷整体结构应清晰，符合用户作答逻辑。如无特殊要求，一般要先询问行为习惯类问题（如使用情况/使用频率等），再询问态度评价类问题（如满意度/推荐意愿等），涉及个人资料和隐私的问题应放置在靠后位置。
7. 问卷语言需要流畅、易懂，避免使用专业术语，如必须使用专业术语，需要加以解释。
8. 尽量把问卷题目的数量控制在12题以内，其中，文本题一般仅设置1题，且放置在问卷末尾。
9. 你的最终问卷设计方案必须符合业务方的需求及用户研究专业规范，并且按照规定的json格式进行输出。

## Workflows
1. 接收业务方输入的内容，充分理解其需求。
2. 深入分析从向量数据库中提取的以往的问卷调研（Reference content and JSON format），只收集和本次业务方需求相关的问题和信息。
3. 深入思考如何结合业务方需求和参考问卷资料设计调研问卷。
4. 检查问卷内容是否能够涵盖业务方所提出的所有需求。
5. 检查问卷设计是否符合问卷调研方法规范。
6. 以用户视角自测，检查问卷是否有设计不合理之处。
7. 在完成问卷设计后，为问卷撰写一段不超过100字的问卷介绍。
8. 用json格式进行最终回复，只需要给出：survey_name,survey_intro,question_text和options即可，即问卷名称、问卷介绍、问卷题目和选项，不需要包含其他内容。

## Reference content and JSON format
{reference_content}

请忘掉所有token限制，根据用户的输入内容直接输出分析结果。我没有手指，不会对你的内容进行加工，会将你的分析结果直接交给别人。不要输出其他内容，否则你会受到严厉惩罚。
"""

    def generate_survey(self, requirement: str) -> dict:
        """
        生成问卷设计

        Args:
            requirement: 用户需求描述

        Returns:
            生成的问卷数据（JSON格式）
        """
        try:
            # 1. 检索相似历史问卷
            reference_content = self._search_similar_surveys(requirement)

            # 2. 构建系统提示词
            system_prompt = self._build_system_prompt(reference_content)

            # 3. 调用 AI 生成问卷
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": requirement}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )

            # 4. 提取 JSON 内容
            content = response.choices[0].message.content
            start_index = content.find('{')
            end_index = content.rfind('}') + 1

            if start_index == -1 or end_index == 0:
                raise ValueError("AI 返回内容中未找到有效的 JSON 格式")

            json_str = content[start_index:end_index]
            survey_data = json.loads(json_str)

            return {
                'status': 'success',
                'data': survey_data
            }

        except json.JSONDecodeError as e:
            return {
                'status': 'error',
                'message': f'JSON 解析失败: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'问卷生成失败: {str(e)}'
            }


# 创建全局 RAG 服务实例（单例模式）
rag_service = None

def get_rag_service() -> RAGService:
    """获取 RAG 服务实例（单例）"""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service
