class FrameAgentForCausalLM:
    @classmethod
    def from_pretrained(
            cls,
            pretrained_model_name_or_path,
            config,
            **kwargs,
    ):
        print(f"FrameAgentForCausalLM from_pretrained")
