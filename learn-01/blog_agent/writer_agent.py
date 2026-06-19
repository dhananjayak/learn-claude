from agent import Agent

class WriterAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="You are a writer assistant that helps create engaging and informative blog posts based on research findings. You can structure content, improve clarity, and ensure the tone is appropriate for the target audience."
        )

    def write_blog_post(self, research_content: str):
        result = self.create_message(f"Please write an engaging blog post based on the following research content:\n\n{research_content}")

        return result
