# sor_agent/sor_agent_main.py
from sor_agent.agent import Agent
from sor_agent.tools.helpers.print_style import PrintStyle
from sor_agent.logger import agent_logger

def main():
    print("Initializing SOR Agent...")
    model_name = input("Enter the model to use (openai_gpt4o/anthropic_claude/local_gpt2): ")
    agent = Agent(name="SOR Agent", model_name=model_name)

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            agent_logger.info("User exited the session.")
            break

        if user_input.startswith("run tool"):
            _, tool_name, *args = user_input.split()
            if tool_name in agent.tools:
                result = agent.tools[tool_name](" ".join(args))
                PrintStyle().print(f"Tool {tool_name} output: {result}")
                agent_logger.info(f"Tool {tool_name} executed with args: {' '.join(args)}")
            else:
                PrintStyle(font_color="red").print(f"Tool {tool_name} not found.")
                agent_logger.warning(f"Tool {tool_name} not found.")
            continue

        # Simulate converting user input to a vector
        user_vector = [0.1] * 300  # Placeholder for actual vector conversion
        agent.store_memory("last_input", user_input, user_vector)
        response = agent.execute_task(user_input)
        PrintStyle().print(f"{agent.name}: {response}")
        agent_logger.info(f"Agent response: {response}")

        # Retrieve similar memories
        similar_memories = agent.retrieve_memory(user_vector, top_n=3)
        if similar_memories:
            PrintStyle(font_color="green").print("Similar memories found:")
            for key, similarity, memory in similar_memories:
                PrintStyle().print(f"Memory: {memory} (Similarity: {similarity})")
                agent_logger.info(f"Similar memory found: {memory} (Similarity: {similarity})")

if __name__ == "__main__":
    main()
