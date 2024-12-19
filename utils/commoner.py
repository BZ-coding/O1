from abc import ABC, abstractmethod

from utils.model_utils.chatbot import ChatBot


class Commoner(ABC):
    prompt = """"""

    def __init__(self, question):
        self.question = question
        self.chatbot = ChatBot()

    def _apply_prompt(self, **kwargs):
        return self.prompt.format(question=self.question, **kwargs)

    def _model_predict(self, content):
        return self.chatbot.chat(messages=content, stream=True)

    def _predict(self, **kwargs):
        content = self._apply_prompt(**kwargs)
        for token in self._model_predict(content=content):
            yield token

    @abstractmethod
    def predict(self, **kwargs):
        pass
