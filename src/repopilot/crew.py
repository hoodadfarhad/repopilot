from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from .tools.models import PRReport
from .tools.sandbox_tools import sandbox_tools
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Repopilot():
    """Repopilot crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def cloner(self) -> Agent:
        return Agent(
            config=self.agents_config['cloner'], # type: ignore[index]
            verbose=True,
            tools= sandbox_tools
        )

    @agent
    def analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['analyzer'], # type: ignore[index]
            verbose=True,
            tools= sandbox_tools
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'], # type: ignore[index]
            verbose=True
        )

    @task
    def clone_repository(self) -> Task:
        return Task(
            config=self.tasks_config['clone_repository'], # type: ignore[index]
        )

    @task
    def analyze_repository(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_repository'], # type: ignore[index]
            output_pydantic= PRReport
        )

    @task
    def create_report(self) -> Task:
        return Task(
            config=self.tasks_config['create_report'], # type: ignore[index]
            output_pydantic= PRReport,
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Repopilot crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            tracing=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
