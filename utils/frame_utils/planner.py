from utils.frame_utils._commoner import _Commoner


class Planner(_Commoner):
    system_prompt = """你是一个规划问题解决步骤的大师。你需要对用户问题进行分析，并根据历史执行信息的具体执行情况，判断如果执行出错则可以要求重新执行当前步骤或直接给出新的解题规划步骤并从头重新执行；而如果历史执行信息良好，则可以给出下一步骤，让其继续执行。"""
    user_prompt = """## 用户问题：
```text
{question}
```




## 历史问题规划：
```text
{old_plan}
```




## 历史执行信息：
```text
{history}
```




请以以下格式输出：“问题分析analysis：
{{analysis}}

问题规划plan：
{{...步骤x：yyy...}}

请执行action：
{{步骤xi：yyy}}”。
请注意：你不需要自己解决问题，你只负责规划解题方案以及反思。"""

    def __init__(self):
        super().__init__()
        self._analysis = ""
        self._plan = ""
        self._action = ""

    def predict(self, question, history=""):
        result = ""
        for token in self._predict(question=question, old_plan=self._plan, history=history):
            result += token
            yield token

        self._analysis = result.split(sep="问题分析analysis：", maxsplit=1)[1].strip()
        result_ = self._analysis.split(sep="问题规划plan：", maxsplit=1)
        self._analysis = result_[0].strip()
        self._plan = result_[1].strip()
        result_ = self._plan.split(sep="请执行action：")
        self._plan = result_[0].strip()
        self._action = result_[-1].strip()

    def get_analysis(self):
        return self._analysis

    def get_plan(self):
        return self._plan

    def get_action(self):
        return self._action


if __name__ == "__main__":
    question = """S先生、P先生、Q先生他们知道桌子的抽屉里有16张扑克牌：红桃A、Q、4 黑桃J、8、4、2、7、3 草花K、Q、5、4、6 方块A、5。约翰教授从这16张牌中挑出一张牌来，并把这张牌的点数告诉P先生，把这张牌的花色告诉Q先生。这时，约翰教授问P先生和Q先生：你们能从已知的点数或花色中推知这张牌是什么牌吗？于是，S先生听到如下的对话：

P先生说：我不知道这张牌。

Q先生在P先生说话之前说：我知道你不知道这张牌。

P先生听到了Q先生的回答，说：现在我知道这张牌了。

Q先生听到了P先生的回答，说：我也知道了。

请问：这张牌是什么牌？"""
    planner = Planner()
    for token in planner.predict(question=question, history=""):
        print(token, end='', flush=True)
    print('\n\n\n')
    print(f"planner.analysis : {planner.get_analysis()}")
    print(f"planner.plan : {planner.get_plan()}")
    print(f"planner.action : {planner.get_action()}")
