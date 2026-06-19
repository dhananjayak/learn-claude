
from dotenv import load_dotenv
from research_agent import ResearchAgent
from writer_agent import WriterAgent


load_dotenv()  # Load environment variables from .env file

def main():
    topic = "The impact of artificial intelligence on modern education"

    research_agent = ResearchAgent()
    research_content = research_agent.perform_research(topic)

    print("\nResearch Content:\n")
    print(research_content)

    writer_agent = WriterAgent()
    blog_post = writer_agent.write_blog_post(research_content)

    print("\nGenerated Blog Post:\n")
    print(blog_post)

    

if __name__ == "__main__":
    main()