# 问卷设计助手

基于 RAG（检索增强生成）技术的智能问卷设计系统，根据用户输入的调研需求，自动生成符合专业规范的问卷。

## 技术栈

### 后端
- **Flask** - Web 框架
- **LangChain** - RAG 框架
- **ChromaDB** - 向量数据库
- **OpenAI API** - AI 模型调用
- **Python 3.x**

### 前端
- **Vue 3** - 前端框架
- **Vite** - 构建工具
- **Tailwind CSS** - UI 样式
- **Pinia** - 状态管理
- **Axios** - HTTP 客户端

## 项目结构

```
ques_design/
├── backend/                  # Python 后端
│   ├── app.py               # Flask API 服务
│   ├── config.py            # 配置文件
│   ├── rag_service.py       # RAG 核心逻辑
│   ├── requirements.txt     # Python 依赖
│   ├── .env.example         # 环境变量模板
│   ├── data/
│   │   └── ques0313.txt    # 问卷知识库
│   └── chroma_db/          # 向量数据库存储（自动生成）
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── components/     # Vue 组件
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── api/            # API 调用封装
│   │   ├── App.vue         # 主应用
│   │   └── main.js         # 入口文件
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件，设置你的 API Key

# 启动后端服务
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:5173` 启动。

### 4. 访问应用

打开浏览器访问：`http://localhost:5173`

## 功能特性

### 核心功能

1. **智能问卷生成**
   - 基于 RAG 技术，从历史问卷库中检索相关内容
   - 使用 Claude Sonnet 4.5 模型生成专业问卷
   - 自动符合用户研究规范和最佳实践

2. **问卷编辑器**
   - 可视化编辑问卷标题和介绍
   - 增删改问卷题目
   - 灵活编辑题目选项
   - 实时预览效果

3. **极简界面**
   - 类 ChatGPT 的对话式交互
   - 响应式设计，支持多设备
   - 流畅的用户体验

4. **数据导出**
   - 一键复制 JSON 格式数据
   - 方便集成到其他系统

### RAG 工作流程

1. **文档加载** - 加载 `ques0313.txt` 中的历史问卷数据
2. **文档分块** - 按换行符分块，每块最大 500 字符
3. **向量化** - 使用 OpenAI Embeddings 向量化
4. **存储** - 存储到 ChromaDB 向量数据库
5. **检索** - 根据用户需求检索 Top-3 相似问卷
6. **生成** - 结合检索结果和系统提示词生成新问卷

## API 接口

### 健康检查
```
GET /api/health
```

### 问卷生成
```
POST /api/generate
Content-Type: application/json

{
  "requirement": "用户需求描述"
}
```

**响应示例：**
```json
{
  "status": "success",
  "data": {
    "survey_name": "问卷名称",
    "survey_intro": "问卷介绍",
    "questions": [
      {
        "question_text": "问题1【单选】",
        "options": ["选项A", "选项B", "选项C"]
      }
    ]
  }
}
```

## 配置说明

### 后端配置 (backend/config.py)

```python
# OpenAI API 配置
OPENAI_API_KEY = "your-api-key"
OPENAI_BASE_URL = "https://api.v3.cm/v1/"

# AI 模型配置
AI_MODEL = "cc-sonnet-4-5-20250929"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# RAG 配置
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
SIMILARITY_TOP_K = 3
```

### 前端配置 (frontend/vite.config.js)

```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true
    }
  }
}
```

## 开发指南

### 添加新的问卷模板

1. 编辑 `backend/data/ques0313.txt`
2. 按照现有格式添加新问卷
3. 删除 `backend/chroma_db/` 目录
4. 重启后端服务（会自动重建向量数据库）

### 自定义 AI 提示词

编辑 `backend/rag_service.py` 中的 `_build_system_prompt` 方法。

### 修改 UI 样式

- 全局样式：`frontend/src/style.css`
- Tailwind 配置：`frontend/tailwind.config.js`
- 组件样式：直接在 `.vue` 文件中使用 Tailwind 类

## 部署

### 后端部署

```bash
# 使用 gunicorn 部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 前端部署

```bash
# 构建生产版本
npm run build

# dist/ 目录可部署到任何静态服务器
```

## 常见问题

### Q: 首次启动很慢？
A: 首次启动需要创建向量数据库，需要几分钟时间。后续启动会直接加载已有数据库。

### Q: 生成失败怎么办？
A: 检查：
1. API Key 是否正确
2. 网络连接是否正常
3. 后端服务是否正常运行
4. 查看后端控制台的错误信息

### Q: 如何更换 AI 模型？
A: 修改 `backend/config.py` 中的 `AI_MODEL` 配置。

### Q: 向量数据库占用空间大吗？
A: 约 10-50MB，取决于问卷库大小。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 技术支持

如有问题，请提交 GitHub Issue。
