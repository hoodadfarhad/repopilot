from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from .tools.models import PRReport
from .tools.sandbox_tools import sandbox_tools

@CrewBase
class Repopilot():
    """Repopilot crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def cloner(self) -> Agent:
        return Agent(
            config=self.agents_config['cloner'], 
            verbose=True,
            tools= sandbox_tools
        )

    @agent
    def analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['analyzer'], 
            verbose=True,
            tools= sandbox_tools
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'], 
            verbose=True
        )

    @task
    def clone_repository(self) -> Task:
        return Task(
            config=self.tasks_config['clone_repository'], 
        )

    @task
    def analyze_repository(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_repository'],
            output_pydantic= PRReport
        )

    @task
    def create_report(self) -> Task:
        return Task(
            config=self.tasks_config['create_report'],
            output_pydantic= PRReport,
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Repopilot crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )
