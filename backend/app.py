"""
Flask API 服务
提供问卷生成的 REST API 接口
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_service import get_rag_service
from config import FLASK_HOST, FLASK_PORT, DEBUG, CORS_ORIGINS

# 创建 Flask 应用
app = Flask(__name__)

# 配置 CORS（跨域资源共享）
CORS(app, resources={
    r"/api/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': '问卷设计 API'
    })


@app.route('/api/generate', methods=['POST'])
def generate_survey():
    """
    问卷生成接口

    Request Body:
    {
        "requirement": "用户需求描述"
    }

    Response:
    {
        "status": "success",
        "data": {
            "survey_name": "问卷名称",
            "survey_intro": "问卷介绍",
            "questions": [...]
        }
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()

        if not data or 'requirement' not in data:
            return jsonify({
                'status': 'error',
                'message': '缺少必需参数: requirement'
            }), 400

        requirement = data['requirement'].strip()

        if not requirement:
            return jsonify({
                'status': 'error',
                'message': '需求描述不能为空'
            }), 400

        # 调用 RAG 服务生成问卷
        rag = get_rag_service()
        result = rag.generate_survey(requirement)

        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """测试接口"""
    return jsonify({
        'status': 'success',
        'message': 'API 服务正常运行',
        'endpoints': {
            'health': '/api/health',
            'generate': '/api/generate (POST)',
            'test': '/api/test'
        }
    })


if __name__ == '__main__':
    print("=" * 50)
    print("问卷设计 API 服务启动中...")
    print(f"服务地址: http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"健康检查: http://localhost:{FLASK_PORT}/api/health")
    print(f"测试接口: http://localhost:{FLASK_PORT}/api/test")
    print("=" * 50)

    # 预加载 RAG 服务（避免首次请求时加载耗时）
    print("\n正在初始化 RAG 服务...")
    get_rag_service()
    print("RAG 服务初始化完成\n")

    # 启动 Flask 应用
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)
