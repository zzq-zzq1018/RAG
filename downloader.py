from modelscope.hub.snapshot_download import snapshot_download
# 魔搭社区模型路径：Qwen/Qwen2.5-0.5B-Instruct；本地保存路径：models（自动创建）
llm_model_dir = snapshot_download('Qwen/Qwen2.5-0.5B-Instruct', cache_dir='models')
print("模型下载完成，保存路径：", llm_model_dir)