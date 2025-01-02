from transformers import AutoModel, PreTrainedModel, AutoConfig

model_path = "utils"

config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
print(config)
"""
FrameAgentConfig {
  "_name_or_path": "utils",
  "architectures": [
    "FrameAgentForCausalLM"
  ],
  "auto_map": {
    "AutoConfig": "configuration_frame_agent.FrameAgentConfig",
    "AutoModel": "modeling_deepseek.FrameAgentForCausalLM",
    "AutoModelForCausalLM": "modeling_deepseek.FrameAgentForCausalLM"
  },
  "model_type": "frame_agent",
  "transformers_version": "4.45.2"
}
"""

# https://huggingface.co/deepseek-ai/DeepSeek-V3-Base/blob/main/modeling_deepseek.py
# AutoModel.from_pretrained()
# PreTrainedModel.from_pretrained()
model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
print(model)
PreTrainedModel.from_pretrained

