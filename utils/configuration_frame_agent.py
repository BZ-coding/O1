from transformers.configuration_utils import PretrainedConfig
from transformers.utils import logging

logger = logging.get_logger(__name__)


class FrameAgentConfig(PretrainedConfig):
    model_type = "frame_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
