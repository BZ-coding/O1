from abc import ABC, abstractmethod

from utils.model_utils.chatbot import ChatBot


class _Commoner(ABC):
    system_prompt = """"""
    user_prompt = """"""

    def __init__(self):
        self._chatbot = ChatBot()
        self._messages = []

    def _model_predict(self, messages):
        return self._chatbot.chat(messages=messages, stream=True, temperature=0.0)

    def _predict(self, **kwargs):
        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt.format(**kwargs)}]
        result = ""
        for token in self._model_predict(messages=messages):
            result += token
            yield token
        messages.append({"role": "assistant", "content": result})
        self._messages.append(messages)

    def get_messages(self):
        return self._messages

    @abstractmethod
    def predict(self, **kwargs):
        pass
