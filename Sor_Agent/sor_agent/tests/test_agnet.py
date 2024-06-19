import unittest
from sor_agent.agent import Agent
from sor_agent.models import LanguageModel
from sor_agent.tools.helpers.vector_db import VectorDB

class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent(name="Test Agent", model_name="local_gpt2")

    def test_tool_loading(self):
        self.assertIn("example_tool", self.agent.tools)

    def test_memory_storage(self):
        vector = [0.1] * 300
        self.agent.store_memory("test_key", "test_value", vector)
        retrieved_memory = self.agent.memory.retrieve("test_key")
        self.assertEqual(retrieved_memory, "test_value")

    def test_text_generation(self):
        response = self.agent.language_model.generate_text("Hello, world!", use_local=True)
        self.assertIsInstance(response, str)

    def test_memory_retrieval(self):
        vector = [0.1] * 300
        self.agent.store_memory("test_key", "test_value", vector)
        similar_memories = self.agent.retrieve_memory(vector, top_n=1)
        self.assertGreater(len(similar_memories), 0)

    def test_openai_model(self):
        self.agent.language_model = LanguageModel(model_name="openai_gpt4o")
        response = self.agent.language_model.generate_text("Hello, world!")
        self.assertIsInstance(response, str)

    def test_anthropic_model(self):
        self.agent.language_model = LanguageModel(model_name="anthropic_claude")
        response = self.agent.language_model.generate_text("Hello, world!")
        self.assertIsInstance(response, str)

if __name__ == "__main__":
    unittest.main()
