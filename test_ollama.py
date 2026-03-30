from openai import OpenAI

# 1. 配置 Ollama 服务信息
api_key = "ollama"  # 本地服务的 API Key 随便填，Ollama 不校验
base_url = "http://localhost:11434/v1"  # Ollama 默认端口 11434

# 2. 创建 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)

# 3. 发送请求（流式输出，和教程示例一致）
response = client.chat.completions.create(
    model="qwen2.5:0.5b",  # 你拉取的模型名称
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "讲个周幽王烽火戏诸侯的故事。"},
    ],
    max_tokens=4096,
    temperature=0.5,
    top_p=0.5,
    stream=True  # 开启流式输出，逐字打印
)

# 4. 逐块打印返回结果
print("模型回复：")
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)