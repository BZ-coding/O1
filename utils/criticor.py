from utils.commoner import Commoner
from utils.model_utils.chatbot import ChatBot


class Criticor(Commoner):
    prompt = """你是一个逻辑批评家。你需要根据用户问题和历史执行信息，对问题规划和当前执行信息进行批评。请注意：整个问题规划是一步一步执行的，所以批评理由不要是还没执行某个步骤；如果当前信息没有问题，也请给出理由。




用户问题：
{question}




问题分析：
{analysis}




问题规划：
{plan}




历史执行信息：
{history}




当前执行信息：
{action}
{action_output}




批评时请注意以上信息是否符合用户问题，特别是用户问题中的隐含条件，或是模型的逻辑问题，还有数学计算也可能算错。
请输出批评理由:"""

    def __init__(self, question):
        super().__init__(question)
        self.criticism = ""

    def predict(self, plan, action, action_output, analysis="", history=""):
        self.criticism = ""
        for token in self._predict(analysis=analysis, plan=plan, history=history, action=action,
                                   action_output=action_output):
            self.criticism += token
            yield token

    def get_criticism(self):
        return self.criticism


if __name__ == "__main__":
    question = """S先生、P先生、Q先生他们知道桌子的抽屉里有16张扑克牌：红桃A、Q、4 黑桃J、8、4、2、7、3 草花K、Q、5、4、6 方块A、5。约翰教授从这16张牌中挑出一张牌来，并把这张牌的点数告诉 P先生，把这张牌的花色告诉Q先生。这时，约翰教授问P先生和Q 先生：你们能从已知的点数或花色中推知这张牌是什么牌吗？于是，S先生听到如下的对话：

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

    criticor = Criticor(question=question)
    for token in criticor.predict(analysis=analysis, plan=plan, action=action, action_output=action_output, history=""):
        print(token, end='', flush=True)
    print('\n\n\n')
    print(f"criticor.criticism : {criticor.get_criticism()}")
