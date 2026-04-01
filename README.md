# Qwen2.5 本地大模型项目
基于 Qwen2.5-0.5B-Instruct 实现本地推理、Ollama 对话、FastAPI 后端、Streamlit 前端聊天机器人。

---

## 项目文件说明
| 文件名 | 作用 |
| --- | --- |
| downloader.py | 从魔搭社区下载 Qwen2.5 模型 |
| basic_infer.py | 直接加载本地模型进行基础推理 |
| test_ollama.py | 测试 Ollama 流式对话 |
| chat_api.py | FastAPI 后端接口（支持流式输出、对话历史） |
| streamlit_chat.py | 前端可视化聊天界面 |

---

## 环境安装
```bash
pip install torch transformers modelscope openai
pip install fastapi uvicorn streamlit requests