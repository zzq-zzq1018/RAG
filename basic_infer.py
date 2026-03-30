import torch
# 导入transformers核心组件
from transformers import AutoModelForCausalLM, AutoTokenizer

# 选择设备：有GPU用cuda，无GPU用cpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("当前使用设备：", device)

# 加载分词器（本地模型路径，注意路径中特殊字符转义，案例中为models/Qwen/Qwen2___5-0___5B-Instruct）
tokenizer = AutoTokenizer.from_pretrained("models/Qwen/Qwen2___5-0___5B-Instruct")
# 加载模型并移至指定设备
model = AutoModelForCausalLM.from_pretrained("models/Qwen/Qwen2___5-0___5B-Instruct").to(device)

# 定义对话提示词和历史
prompt = "你好"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},  # 系统角色：定义模型行为
    {"role": "user", "content": prompt}  # 用户输入
]

# 处理对话格式：转换为模型可识别的格式，添加生成提示
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,  # 先不分词，生成文本格式
    add_generation_prompt=True  # 添加assistant起始标记，指示模型生成回答
)

# 分词处理：转换为PyTorch张量，移至指定设备
model_inputs = tokenizer([text], return_tensors="pt").to(device)

# 模型生成：最大生成512个新token
generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512,)

# 截取生成结果：去除原始输入部分，只保留模型生成的内容
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

# 解码：将tokenID转换为文本，忽略特殊token
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

# 输出生成结果
print("模型回答：", response)