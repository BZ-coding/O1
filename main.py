from transformers import AutoModel, PreTrainedModel, AutoConfig

model_path = "utils"

config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
print(config)

# https://huggingface.co/deepseek-ai/DeepSeek-V3-Base/blob/main/modeling_deepseek.py
# AutoModel.from_pretrained()
# PreTrainedModel.from_pretrained()
