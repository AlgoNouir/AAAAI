from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.tools import tool as langToolDecorator
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import render_text_description
from typing import Any, Dict, Optional, TypedDict
from langchain_core.runnables import RunnableConfig
import ast

toolsPrompt = """\
You are an assistant that has access to the following set of tools. 
Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. 
Return your response as a JSON blob with 'name' and 'arguments' keys.

The `arguments` should be a dictionary, with keys corresponding 
to the argument names and the values corresponding to the requested values.
"""


class ToolCallRequest(TypedDict):
    """A typed dict that shows the inputs into the invoke_tool function."""

    name: str
    arguments: Dict[str, Any]


class Agent:
    def __init__(
        self,
        mainText: str,
        modelName: str,
        maxRetray=3,
        baseUrl="http://localhost:11434",
    ):
        self.system_prompt: dict[str, str | list[str], dict[str, str]] = {}
        self.modelName = modelName
        self.baseUrl = baseUrl
        self.maxRetray = maxRetray

        # add system prompts
        self.system_prompt["SYSTEM"] = mainText
        # generate tools from method
        if len(self._tools):
            rendered_tools_text = render_text_description(self._tools.values()).replace(
                "\n", "\n\t"
            )
            self.system_prompt["TOOLS"] = toolsPrompt.format(
                rendered_tools=rendered_tools_text
            )

    @property
    def prompt(self):
        """this function return AI prompt from system_prompt"""

        result = ""
        for key, prompt in self.system_prompt.items():
            # add key of prompt

            # set prompt list
            if isinstance(prompt, list):
                # check for data is exists
                if not len(prompt):
                    continue

                # convert prompt data
                prompt = "\n".join(prompt)

            # for handleing prompt data each key can have key
            elif isinstance(prompt, dict):
                # check for data is exists
                if not len(prompt):
                    continue

                # convert prompt data
                prompt = "\n".join(list(prompt.values()))

            # normal string prompt is other wise.
            result += f"{key}:\n{prompt}\n\n"

        return result

    @property
    def chain(self):
        # create LLM model
        llm = OllamaLLM(
            model=self.modelName,
            base_url=self.baseUrl,
        )

        prompt = PromptTemplate(
            input_variables=["question"],
            template=self.prompt + "\n-------\nPLAN:\n{question}",
        )

        # set tools of chain in agent
        return prompt | llm

    @property
    def toolChain(self):
        if not len(self._tools):
            return None

        return self.chain | JsonOutputParser() | self._invoke_tool

    def __hash__(self):
        return hash(str(self.system_prompt))

    # -------------------------------------------------------- MAIN FUNCTIONS

    @property
    def _ignoreFuncs(self):
        return [
            "message",
            "tool_message",
            "select",
            "toolChain",
            "chain",
            "prompt",
            "remember",
            "forget",
            "parameter",
        ]

    @property
    def _tools(self):
        result = {}
        for tool in self.__dir__():
            # filter data
            if (
                tool.strip("_") != tool
                or tool in self.__dict__.keys()
                or tool in self._ignoreFuncs
            ):
                continue

            result[tool] = langToolDecorator(self.__getattribute__(tool))

        return result

    def _descibe_yourself(self):
        return f"i am AI agent with below prompt:{self.system_prompt}"

    def _invoke_tool(
        self,
        tool_call_request: ToolCallRequest,
        config: Optional[RunnableConfig] = None,
    ):
        """A function that we can use the perform a tool invocation.

        Args:
            tool_call_request: a dict that contains the keys name and arguments.
                The name must match the name of a tool that exists.
                The arguments are the arguments to that tool.
            config: This is configuration information that LangChain uses that contains
                things like callbacks, metadata, etc.See LCEL documentation about RunnableConfig.

        Returns:
            output from the requested tool
        """
        name = tool_call_request["name"]

        for funcName, requested_tool in self._tools.items():
            if funcName in name:
                break
        else:
            return "function not found"

        return requested_tool.invoke(tool_call_request["arguments"], config=config)

    # -------------------------------------------------------- DEFAULT TOOLS

    def message(self, message):
        return self.chain.invoke({"question": message})

    def tool_message(self, message):
        if self.toolChain is None:
            return None
        print(message)
        return self.toolChain.invoke({"question": message})

    def remember(self, key: str, message: str):
        """save data of user sended"""
        remember = self.system_prompt.get("REMEMBER", {})
        remember[key] = message
        self.system_prompt["REMEMBER"] = remember

    def forget(self, key: str):
        """forget remembered key of user sended"""
        remember = self.system_prompt.get("REMEMBER", {})
        remember.pop(key)
        self.system_prompt["REMEMBER"] = remember

    def select(
        self, text: str, options: list[str] | dict[str, str], freq=0, think=False
    ):
        """Choose exactly one of the options based on the text."""
        # create options from dict
        if isinstance(options, dict):
            # add options desc to text
            text += "options desciption: " + ", ".join(
                [f"{k} -> {v}" for k, v in options.items()]
            )
            optionsText = ", ".join([str(k) for k in options.keys()])
        else:
            optionsText = ", ".join(options)

        # create prompt and
        question = f"text: {text} | plan: Choose exactly one of the options based on the text. | options : {optionsText} "
        response = self.chain.invoke({"question": question})
        print("select response ->", response)

        # check exact option
        for opt in options:
            if opt.lower() in response.lower():
                return opt

        # if option not in response

        if freq >= self.maxRetray:
            return None

        # if not think
        if not think:
            return None

        # retray on anwsering
        return self.select(response, options, freq + 1, think=True)

    def parameter(self, text: str, parameter: dict[str, str]) -> dict:
        """from text that i give you write just answer of parameters"""

        question = f"text : {text} | plan : from text that i give you write just answer of parameters in JSON format and without more ```json or markdowns | dictionary : {parameter} "
        response = self.chain.invoke({"question": question})
        response = response.strip(" ```")
        response = response.replace("```", " ")
        response = response.replace("json", " ")
        print(response)
        res = ast.literal_eval(response)
        print(res)
        print(type(res))
