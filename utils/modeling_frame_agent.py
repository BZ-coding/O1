from utils.frame_utils.frame import Frame


class FrameAgentForCausalLM:
    # https://huggingface.co/deepseek-ai/DeepSeek-V3-Base/blob/main/modeling_deepseek.py
    @classmethod
    def from_pretrained(
            cls,
            pretrained_model_name_or_path,
            config,
            **kwargs,
    ):
        # print(f"FrameAgentForCausalLM from_pretrained")
        # print(f"pretrained_model_name_or_path:{pretrained_model_name_or_path}")
        # print(f"config:{config}")
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
        # print(f"kwargs:{kwargs}")
        return cls()

    def __init__(self):
        self.frame = Frame()

    def generate(self, question):
        for token in self.frame.predict(question=question):
            yield token
