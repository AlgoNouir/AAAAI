from aaaai.agent import Agent


orchestraPrompt = """
you are a agent
"""


class Orchestration(Agent):
    """
    this is a class for connect agents togheter
    """

    def __init__(self, modelName, maxRetray=3, baseUrl="http://localhost:11434"):
        super().__init__(
            mainText=orchestraPrompt,
            modelName=modelName,
            maxRetray=maxRetray,
            baseUrl=baseUrl,
        )
        self.agents: dict[Agent, str] = {
            # agentName: agentAbility
        }

    @property
    def _ignoreFuncs(self):
        return ["register", "invoke", "selectAgent", *super()._ignoreFuncs]

    def register(self, agent: Agent) -> None:
        self.agents[agent] = agent._descibe_yourself()

    def selectAgent(self, desier: str) -> Agent:
        """select best registered"""

        print("check agent data for selecting best")

        selectedIndex = self.select(
            f"what agent is good for below task?\n{desier}",
            {index: desc for index, desc in enumerate(self.agents.values())},
        )

        print("agent selected", selectedIndex)

        # return from registered agents
        return list(self.agents.keys())[int(selectedIndex)]

    def invoke(self, desier: str) -> str:
        print("invoke data on orchestra")
        agent = self.selectAgent(desier)
        print("send message to agent")
        return agent.message(desier)
