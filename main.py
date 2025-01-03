from transformers import AutoModel, PreTrainedModel, AutoConfig

model_path = "utils"

config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path, trust_remote_code=True)

question = """为什么会出现近大远小？"""
for token in model.generate(question=question):
    print(token, end='', flush=True)
