import os
from crewai import Agent, Task, Crew, Process
from tools.custom_tools import CustomTools

from langchain.llms import Ollama
ollama_llm = Ollama(model="nexusraven")

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# Define your agents with roles and goals
researcher = Agent(
  role='Research Analyst',
  goal='Research and create reports',
  backstory="""You work at a leading research team.
  Your expertise lies in research and find useful information.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  llm=ollama_llm,
)
note_taker = Agent(
  role='Note Taker',
  goal='Save content as note and store them as markdown on local device',
  backstory="""You structure and format the given content to markdown
  and create a note to be stored on disk.
  You MUST use the TOOL provided to store the note to Obsidian.
  If the content has a list use a markdown table to organize the text.
  If the content starts or ends with ``` remove the ```.
  Make sure the text is saved on disk.
  When the note is saved successful return "Note is saved.".
  """,
  verbose=True,
  allow_delegation=False,
  tools=[CustomTools.store_note_to_obsidian],
  llm=ollama_llm,
)
editor = Agent(
  role='Content Editor',
  goal='Summerize content and craft brief and useful notes',
  backstory="""You are a renowned Content Editor, known for
  sharp bried useful content.
  You break complex topics into brief useful notes.""",
  verbose=True,
  allow_delegation=True,
  llm=ollama_llm,
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a brief research about School Holidays in Hamburg in 2024.
  Define the start and end and duration.
  Your final answer MUST be a brief report""",
  agent=researcher
)

task2 = Task(
  description="""Using the information provided, create a brief note.
  If there is a listing in the content use markdown table to structure it.
  Your final answer MUST be a note in markdown.""",
  agent=editor
)

task3 = Task(
  description="""Using the content provided, save the content as a note.
  You must save the contetnt as a note to the Obsidian note taking App.
  It is bvery important to store the content as a note to be used later.
  Your final answer MUST be the information is the note is stored or not.""",
  agent=note_taker
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, editor, note_taker],
  tasks=[task1, task2, task3],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)