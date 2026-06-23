from agent.agent import Agent

agent = Agent()

print("AI Agent started. Type 'exit' to quit.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Agent stopped.")
        break

    agent.perceive(user_input)
    response = agent.think_and_act(user_input)
    print("Agent:", response)
