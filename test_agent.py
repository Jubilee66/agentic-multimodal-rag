# test_agent.py

import os

from agent.agent_loop import run_agent

response = run_agent(
    "Explain AI according to NVIDIA annual report",
    os.getenv("GROQ_API_KEY")
)

print(response)