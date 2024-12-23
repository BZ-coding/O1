from utils.frame_utils._commoner import _Commoner


class Over(_Commoner):
    system_prompt = """你是一个判断大语言模型推理循环是否可以结束的机器人，你只需要根据以下信息判断是否可以结束循环即可。"""
    user_prompt = """## 用户问题：
```text
{question}
```




## 问题分析：
```text
{analysis}
```




## 问题规划：
```text
{plan}
```




## 历史执行信息：
```text
{history}
```




当前执行信息：
```text
{action}
{action_output}
```




批评理由:
```text
{criticism}
```




请你根据以上信息，判断是否已经有了能够解答用户问题的、正确的最终答案，不需要再继续执行了。请注意：输出结果只能是"结束"或"继续"。
"""

    def __init__(self):
        super().__init__()
        self.over_result = ""

    def predict(self, question, analysis, plan, history, action, action_output, criticism):
        self.over_result = ""
        for token in self._predict(question=question, analysis=analysis, plan=plan, history=history, action=action,
                                   action_output=action_output, criticism=criticism):
            self.over_result += token
            yield token

    def get_is_over(self):
        return self.over_result.startswith("继续") or self.over_result.endswith("继续")


if __name__ == "__main__":
    question = """S先生、P先生、Q先生他们知道桌子的抽屉里有16张扑克牌：红桃A、Q、4 黑桃J、8、4、2、7、3 草花K、Q、5、4、6 方块A、5。约翰教授从这16张牌中挑出一张牌来，并把这张牌的点数告诉P先生，把这张牌的花色告诉Q先生。这时，约翰教授问P先生和Q先生：你们能从已知的点数或花色中推知这张牌是什么牌吗？于是，S先生听到如下的对话：

P先生说：我不知道这张牌。

Q先生在P先生说话之前说：我知道你不知道这张牌。

P先生听到了Q先生的回答，说：现在我知道这张牌了。

Q先生听到了P先生的回答，说：我也知道了。

请问：这张牌是什么牌？"""
    analysis = """根据游戏规则，我们知道P先知道的是点数，Q先知道的是花色。我们依次解析两人对话的内容。

1. **P先生说：“我不知道这张牌。”**
   - P先生不能从点数就知道确切的牌是什么。也就是说，对于P先生所知道的这个点数，在这16张牌中，不止一种可能性可让P先生说出具体某个花色下的该点数。例如，如果点数为A，则可能有红桃A或方块A；如果是5，则有草花5和方块5；而诸如4或者2则能确定一个更具体的范围。

2. **Q先生说：“我知道你不知道这张牌。”**
   - 这是因为对于Q先生知道的花色，P不可能仅凭这个点数便直接知道答案。换句话说，在考虑的是16张牌中的这一特定花色的所有可能性时，无论哪个点数，该花色下都有两种或多种相同点数的其他花色可以排除（除非仅剩一种情况，例如4），这足以说明这张牌不是在草花K和方块A的情形中。

3. **P先生说：“现在我知道这张牌了。”**
   - 他得到了Q的话信息后有了清晰答案。这意味着之前的所有可能性经过Q的提示后被排除掉只剩一个点数和一个确定的花色匹配的情况，具体可以是红桃A或者黑桃7等等。
   
4. **Q先生说：“我也知道了。”**
   - 经过P的确认进一步的信息传递之后（且信息明确到了某个点即可知道情况），Q得知的确切牌面组合。

综上所述，P提到的是一个通用的规则即特定点数下，有多个卡种存在无法立刻确定。而Q利用这些多样的可能来排除，仅留下一种唯一选项可以由P进一步细化确认并公开告知答案。结合这些原则进行检验和分析能够找到正确答案。"""
    plan = """1. **步骤1：罗列所有组合**
   - 汇总所有16张牌的具体点数与花色情况。
2. **步骤2：初步确定**
   - 分别从P的角度出发，依据每个可能的点数进行排查。
3. **步骤3：应用Q的信息限制**
   - 根据Q提到的情形来细化并再次排查可能性范围。
4. **步骤4：最终确认**
   - 在限定的选择中找到只有一张符合所有信息描述条件的答案。"""
    action = """步骤1：罗列这16张扑克牌的具体点数与花色，例如红桃A、Q、4；黑桃J、8、4、2、7、3；草花K、Q、5、4、6；方块A、5"""
    action_output = """步骤1：羅列這16張扑克牌的具體點數與花色如下：

    - 紅桃 (Heart) ： A, Q, 4
    - 黑桃 (Spade)： J, 8, 4, 2, 7, 3
    - 草花 (Diamonds)： K, Q, 5, 4, 6
    - 方块 (Clubs): A, 5

    接下来，我们将按照提供的对话，逐一分析这16张牌的信息，并最终确定那张唯一的牌。"""
    criticism = """当前执行规划基本合理、详细。不过可以对一些解释进行微调和精简以更好地与对话对应：

1. 用户提供的对话及步骤分析中，“草花 (Diamonds)” 指向的是草花（并非方块）。

2. 当前细化步骤已经涵盖了背景信息罗列，是执行规划的合理开始。后续可以直接进入具体的逻辑推理过程。但需保证每个具体点数与花色组合在限定条件中被严谨排除或保留以达到唯一解。

修改后的清晰版规划如下：

1. **步骤1：罗列所有组合**
    - 汇总所有16张牌的具体点数与花色情况，即红桃 (Heart) A、Q、4；黑桃 (Spade) J、8、4、2、7、3；草花 (Diamonds) K、Q、5、4、6；方块 (Clubs) A、5。

接下来步骤2和后续分析中，请严格遵循逻辑关系来进行筛选，结合对话中的关键信息逐一排除可能性直到锁定正确答案。这样的改动能更好与原问题及解析对应，并保持逻辑连贯且严谨。"""

    over = Over()
    for token in over.predict(question=question, analysis=analysis, plan=plan, history="", action=action,
                              action_output=action_output, criticism=criticism):
        print(token, end='', flush=True)
    print('\n\n\n')
    print(f"over.get_is_over : {over.get_is_over()}")
