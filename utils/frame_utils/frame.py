import jsonlines

from utils.frame_utils.criticor import Criticor
from utils.frame_utils.executor import Executor
from utils.frame_utils.over import Over
from utils.frame_utils.planner import Planner
from utils.frame_utils.summarizer import Summarizer


class Frame:
    def __init__(self):
        self.analysis = ""
        self.plan = ""
        self.action = ""
        self.action_output = ""
        self.criticism = ""
        self.history = ""
        self.is_over = False

    def _update_history(self, action, action_output, criticism):
        self.history = f"""{self.history}

执行信息：
{action}
执行结果：
{action_output}
批评信息：
{criticism}"""

    def predict(self, question):
        planner = Planner()
        executor = Executor()
        criticor = Criticor()
        over = Over()
        summarizer = Summarizer()

        self.is_over = False
        while not self.is_over:
            for token in planner.predict(question=question, history=self.history):
                yield token
            self.analysis = planner.get_analysis()
            self.plan = planner.get_plan()
            self.action = planner.get_action()
            print("\n")

            for token in executor.predict(question=question, analysis=self.analysis, plan=self.plan, action=self.action,
                                          history=self.history):
                yield token
            self.action_output = executor.get_action_output()
            print("\n")

            for token in criticor.predict(question=question, analysis=self.analysis, plan=self.plan, action=self.action,
                                          action_output=self.action_output, history=self.history):
                yield token
            self.criticism = criticor.get_criticism()
            print("\n")

            for token in over.predict(question=question, analysis=self.analysis, plan=self.plan, action=self.action,
                                      action_output=self.action_output, history=self.history, criticism=self.criticism):
                yield token
                # pass
            self.is_over = over.get_is_over()
            print("\n")

            self._update_history(action=self.action, action_output=self.action_output, criticism=self.criticism)

        for token in summarizer.predict(question=question, analysis=self.analysis, plan=self.plan, action=self.action,
                                        action_output=self.action_output, history=self.history,
                                        criticism=self.criticism):
            yield token

        with jsonlines.open('data_planner.jsonl', mode='w') as writer:
            writer.write_all(planner.get_messages())
        with jsonlines.open('data_executor.jsonl', mode='w') as writer:
            writer.write_all(executor.get_messages())
        with jsonlines.open('data_criticor.jsonl', mode='w') as writer:
            writer.write_all(criticor.get_messages())
        with jsonlines.open('data_over.jsonl', mode='w') as writer:
            writer.write_all(over.get_messages())


if __name__ == "__main__":
    question = """S先生、P先生、Q先生他们知道桌子的抽屉里有16张扑克牌：红桃A、Q、4 黑桃J、8、4、2、7、3 草花K、Q、5、4、6 方块A、5。约翰教授从这16张牌中挑出一张牌来，并把这张牌的点数告诉P先生，把这张牌的花色告诉Q先生。这时，约翰教授问P先生和Q先生：你们能从已知的点数或花色中推知这张牌是什么牌吗？于是，S先生听到如下的对话：

P先生说：我不知道这张牌。

Q先生在P先生说话之前说：我知道你不知道这张牌。

P先生听到了Q先生的回答，说：现在我知道这张牌了。

Q先生听到了P先生的回答，说：我也知道了。

请问：这张牌是什么牌？"""
    frame = Frame()
    for token in frame.predict(question=question):
        print(token, end='', flush=True)
