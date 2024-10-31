import os
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool, PDFSearchTool
from crewai_tools import PDFSearchTool

os.environ["OPENAI_API_KEY"] = ""

docs_tool = DirectoryReadTool(directory="./blog-posts")
file_tool = FileReadTool()

researcher = Agent(
    role="Market Research Analyst",
    goal="Analyze provided text to summarize.",
    backstory="An expert analyst with a keen eye for market trends.",
    tools=[],
    verbose=True,
)

writer = Agent(
    role="Content Writer",
    goal="Craft engaging blog posts",
    backstory="A skilled writer.",
    tools=[docs_tool, file_tool],
    verbose=True,
)


# Initialize the tool allowing for any PDF content search if the path is provided during execution
# pdf_tool = PDFSearchTool()

# OR

# Initialize the tool with a specific PDF path for exclusive search within that document
pdf_tool = PDFSearchTool(
    pdf="/home/kamal/Documents/learning/agent-crewai-exmaple/pdf/story/shorttelling/Storytelling.pdf"
)

# Usage example
research = Task(
    description="Summarize the provided text to highlight the top 3 trending topics.",
    expected_output="A summary of the top 3.",
    agent=researcher,
    tools=[pdf_tool],  # Add PDFSearchTool to researcher's tools
)

write = Task(
    description="Write an engaging blog post about it.",
    expected_output="A 4-paragraph blog post formatted in json with engaging, informative.",
    agent=writer,
    output_file="blog-posts/sample.json",
)

crew = Crew(
    agents=[researcher, writer], tasks=[research, write], verbose=True, planning=True
)

blog = crew.kickoff()

print(blog)
