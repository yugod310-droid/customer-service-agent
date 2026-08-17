from transformers import AutoTokenizer, AutoModelForCausalLM
'''| 代码               | 作用       |
| ---------------- | -------- |
| AutoTokenizer    | 加载分词器    |
| tokenizer()      | 文字→token |
| model.generate() | 生成token  |
| decode()         | token→文字 |
| return           | 返回回答     |
'''

MODEL_PATH = r"D:\AI\models\models\Qwen--Qwen2.5-3B-Instruct\snapshots\master"


print("正在加载模型...")


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)


model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto"
)


print("模型加载完成!")


def chat(message: str,system_prompt: str = None) -> str:

    messages = []
    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )
    messages.append(
        {
            "role": "user",
            "content": message
        }
    )
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )


    inputs = tokenizer(
        text,
        return_tensors="pt"
    ).to(model.device)


    outputs = model.generate(
        **inputs,
        max_new_tokens=200
    )


    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return response

def clarify_intent(user_input: str) -> str:
    """
    Clarifies the intent of the user's input.
    """
    prompt = f'''
    你是一个客服意图识别助手。请判断用户需求属于哪一类：

        1. balance 查询余额
        2. other 普通问题

        用户输入：
        {user_input}

        只返回类别名称。
    '''
    
    result = chat(prompt)
    return result