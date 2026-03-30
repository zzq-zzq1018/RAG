from fastapi import FastAPI, Body
from openai import AsyncOpenAI
from typing import List
from fastapi.responses import StreamingResponse

# 1. 初始化 FastAPI 应用
app = FastAPI(title="Qwen2.5 Chat API")

# 2. 初始化 Ollama 客户端
api_key = "ollama"
base_url = "http://localhost:11434/v1"
aclient = AsyncOpenAI(api_key=api_key, base_url=base_url)

# 初始化对话列表（全局变量，用于维护上下文）
messages = []

# 3. 定义 /chat 接口
@app.post("/chat")
async def chat(
    query: str = Body(..., description="用户输入的问题"),
    sys_prompt: str = Body("你是一个有用的助手。", description="系统提示词"),
    history: List = Body([], description="历史对话记录"),
    history_len: int = Body(1, description="保留历史对话的轮数"),
    temperature: float = Body(0.5, description="LLM 采样温度"),
    top_p: float = Body(0.5, description="LLM 采样概率"),
    max_tokens: int = Body(None, description="LLM 最大 token 数量")
):
    global messages
    
    # 控制历史记录长度
    if history_len > 0:
        history = history[-2 * history_len:]
    
    # 清空消息列表，重新构建上下文
    messages.clear()
    messages.append({"role": "system", "content": sys_prompt})
    messages.extend(history)
    messages.append({"role": "user", "content": query})
    
    # 发送请求到 Ollama（流式输出）
    response = await aclient.chat.completions.create(
        model="qwen2.5:0.5b",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True
    )
    
    # 定义生成器函数，用于流式输出
    async def generate_response():
        async for chunk in response:
            chunk_msg = chunk.choices[0].delta.content
            if chunk_msg:
                yield chunk_msg
    
    # 返回流式响应
    return StreamingResponse(generate_response(), media_type="text/plain")

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6066, log_level="info")