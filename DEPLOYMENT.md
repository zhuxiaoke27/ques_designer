# Zeabur 部署指南

本项目需要分别部署**后端**和**前端**两个服务。

## 部署架构

```
前端 (Vue 3 Static Site)  →  后端 (Python Flask API)
      ↓                              ↓
   Zeabur Service 1            Zeabur Service 2
```

---

## 第一步：部署后端 API

### 1. 在 Zeabur 创建新服务

1. 登录 [Zeabur](https://zeabur.com)
2. 创建新项目或选择现有项目
3. 点击 "Add Service" → 选择 "Git"
4. 连接你的 GitHub 仓库：`zhuxiaoke27/ques_designer`
5. 选择分支：`zeabur-deploy`

### 2. 配置后端服务

**服务名称**：`backend`

**根目录**：选择 `backend` 文件夹

**构建设置**：
- Zeabur 会自动检测为 Python 项目
- 使用 `requirements.txt` 安装依赖
- 使用 `Procfile` 启动服务

**环境变量**（必须配置）：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `OPENAI_API_KEY` | `your-api-key-here` | OpenAI API 密钥（必需） |
| `OPENAI_BASE_URL` | `https://api.v3.cm/v1/` | API 基础 URL |
| `CORS_ORIGINS` | `https://your-frontend.zeabur.app` | 前端域名（部署后填写） |
| `DEBUG` | `False` | 生产环境关闭调试模式 |

**注意**：
- `PORT` 环境变量会由 Zeabur 自动提供，无需手动配置
- 部署完成后，记录下后端服务的 URL（例如：`https://backend-xxx.zeabur.app`）

### 3. 等待部署完成

- 构建和部署大约需要 3-5 分钟
- 完成后访问 `https://your-backend.zeabur.app/api/health` 验证服务正常

---

## 第二步：部署前端

### 1. 在同一项目创建新服务

1. 在同一个 Zeabur 项目中，点击 "Add Service" → 选择 "Git"
2. 选择相同的仓库和分支
3. 这次选择 `frontend` 文件夹

### 2. 配置前端服务

**服务名称**：`frontend`

**根目录**：选择 `frontend` 文件夹

**构建设置**：
- Zeabur 会自动检测为 Node.js 项目
- 自动运行 `npm install` 和 `npm run build`

**环境变量**：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `VITE_API_BASE_URL` | `https://backend-xxx.zeabur.app/api` | 后端 API 地址（使用第一步的 URL） |

**注意**：
- 前端会被构建为静态文件
- Zeabur 会自动配置静态文件服务

### 3. 更新后端 CORS 配置

前端部署完成后：
1. 获取前端 URL（例如：`https://frontend-xxx.zeabur.app`）
2. 回到后端服务
3. 更新 `CORS_ORIGINS` 环境变量：
   ```
   https://frontend-xxx.zeabur.app
   ```
4. 重启后端服务

---

## 第三步：验证部署

### 1. 测试后端

访问：`https://your-backend.zeabur.app/api/health`

应该返回：
```json
{
  "status": "healthy",
  "service": "问卷设计 API"
}
```

### 2. 测试前端

1. 访问：`https://your-frontend.zeabur.app`
2. 输入问卷需求
3. 点击"生成问卷"
4. 验证能否正常生成问卷

---

## 常见问题

### Q1: 后端部署失败，提示找不到 Python 版本

**解决方案**：
- 确保 `backend/runtime.txt` 文件存在
- 内容为：`python-3.12`

### Q2: 前端无法连接后端

**检查清单**：
1. ✅ 前端环境变量 `VITE_API_BASE_URL` 是否正确
2. ✅ 后端 CORS 配置是否包含前端域名
3. ✅ 后端服务是否正常运行

### Q3: 生成问卷时超时

**解决方案**：
- AI 生成可能需要 30-60 秒
- 确保前端 axios timeout 设置足够大（已设置为 60 秒）
- 检查后端日志是否有错误

### Q4: 向量数据库初始化失败

**解决方案**：
- 确保 `backend/data/ques0313.txt` 文件已上传
- 首次启动会自动创建向量数据库（约 2-3 分钟）
- 检查后端日志

### Q5: tiktoken 包构建失败

**问题描述**：
```
ERROR: Failed building wheel for tiktoken
× Failed to build installable wheels for some pyproject.toml based projects
```

**解决方案**：
本问题已在 `fix-zeabur-tiktoken-build` 分支中修复：
1. ✅ 升级 tiktoken 到 0.8.0（更好的 Python 3.13 支持）
2. ✅ 添加 Dockerfile 明确指定 Python 3.12 和构建工具
3. ✅ 添加 `.python-version` 文件确保版本一致

**修复措施**：
- 使用 Dockerfile 构建可确保安装必要的编译工具（gcc、g++、make）
- 明确使用 Python 3.12（避免 Python 3.13 兼容性问题）
- 升级 tiktoken 版本以获得更好的构建支持

---

## 环境变量总结

### 后端必需环境变量

```bash
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.v3.cm/v1/
CORS_ORIGINS=https://your-frontend.zeabur.app
DEBUG=False
```

### 前端必需环境变量

```bash
VITE_API_BASE_URL=https://your-backend.zeabur.app/api
```

---

## 项目结构说明

```
ques_design/
├── backend/              # Python 后端服务
│   ├── Procfile         # Zeabur 启动配置
│   ├── runtime.txt      # Python 版本声明
│   ├── requirements.txt # Python 依赖
│   ├── app.py          # Flask 应用入口
│   ├── config.py       # 配置管理
│   ├── rag_service.py  # RAG 核心逻辑
│   └── data/
│       └── ques0313.txt # 问卷知识库
└── frontend/            # Vue 3 前端
    ├── package.json     # Node.js 配置
    ├── vite.config.js   # Vite 构建配置
    └── src/             # 源代码
```

---

## 本地开发

如果需要在本地测试：

### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

---

## 技术支持

如遇到问题，请检查：
1. Zeabur 部署日志
2. 浏览器开发者工具 Console
3. 网络请求是否正常

GitHub: https://github.com/zhuxiaoke27/ques_designer
