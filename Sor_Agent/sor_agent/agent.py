# sor_agent/agent.py
import importlib
import inspect
from sor_agent.memory import Memory
from sor_agent.models import LanguageModel
from sor_agent.tools.helpers.print_style import PrintStyle
from sor_agent.tools.helpers.vector_db import VectorDB
from sor_agent.tools.helpers.file_utils import list_files

class Agent:
    def __init__(self, name="Agent Zero", model_name=None):
        self.name = name
        self.memory = Memory()
        self.language_model = LanguageModel(model_name)
        self.vector_db = VectorDB()
        self.history = []
        self.tools = self.load_tools()

    def load_tools(self):
        tools = {}
        tool_files = list_files('sor_agent/tools', exclude=['__init__.py', 'helpers'])
        for tool_file in tool_files:
            tool_name = tool_file.stem
            tool_func = self.get_tool(tool_name)
            if tool_func:
                tools[tool_name] = tool_func
        return tools

    def get_tool(self, name):
        try:
            module = importlib.import_module(f"sor_agent.tools.{name}")
            functions = {name: func for name, func in inspect.getmembers(module, inspect.isfunction)}
            return functions.get("execute")
        except ImportError:
            return None

    def execute_task(self, task):
        PrintStyle().print(f"{self.name} is processing the task: {task}")
        tool_name = self.determine_tool(task)
        if tool_name in self.tools:
            tool_func = self.tools[tool_name]
            return tool_func(task)
        return "Task could not be executed."

    def determine_tool(self, task):
        # Advanced tool determination logic based on task keywords
        for tool_name in self.tools:
            if tool_name in task.lower():
                return tool_name
        return None

    def store_memory(self, key, value, vector):
        self.memory.store(key, value)
        self.vector_db.add_memory(key, vector, value)

    def retrieve_memory(self, vector, top_n=1):
        return self.vector_db.get_similar_memory(vector, top_n)
