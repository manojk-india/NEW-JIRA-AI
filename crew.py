from crewai import Agent, Task, Crew,LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="sambanova/DeepSeek-R1-Distill-Llama-70B",
    temperature=0.7
)


# Jira API Endpoints
JIRA_API_MAPPING = {
    "issues": "/rest/api/3/search",
    "sprints_from_board": "/agile/1.0/board/{boardId}/sprint",
    "issues_from_board": "/agile/1.0/board/{boardId}/issue",
    "issues_from_sprint": "/agile/1.0/board/{boardId}/sprint/{sprintId}/issue",
}

# Agent 1: Query Analyzer (Understands user intent using DeepSeek)
query_analyzer = Agent(
    role="Query Analyzer",
    goal="Understands Jira-related queries and determines the appropriate API to call.",
    backstory=" You are a Jira expert who can classify user queries into Jira API categories.",
    llm=llm,
    verbose=True,
   
)


user_query="Show me all the open issues in cdf board"

prompt = f"""
You are an AI assistant that maps user queries to Jira API categories.
Given a user query, classify it into one of these categories:
- "issues" (for general Jira issues)
- "sprints_from_board" (for retrieving sprints from a board)
- "issues_from_board" (for retrieving issues from a board)
- "issues_from_sprint" (for retrieving issues from a sprint)
- "other" (if it does not match any of the above)


Query: "{user_query}"
Category:
"""




# Define Tasks
task1 = Task(
    description="Analyze user query {prompt} and determine the appropriate Jira API endpoint",
    agent=query_analyzer,
    expected_output="api_category",
)


# Define Crew (Manages the entire workflow)
crew = Crew(
    agents=[query_analyzer], 
    tasks=[task1],
    
)

# Step 1: Query Analyzer determines the API category
api_category = crew.kickoff(inputs={"prompt": prompt})


if api_category == "other":
    print("Sorry, I couldn't understand your request.")
else:
    print(api_category)

