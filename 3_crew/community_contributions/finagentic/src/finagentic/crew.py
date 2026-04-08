from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool


@CrewBase
class Finagentic():
    """Finagentic crew"""

    @agent
    def financial_product_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_product_researcher'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True
        )

    @task
    def research_financial_products_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_financial_products_task'],
        )

    @task
    def analyze_and_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_and_report_task'],
           # output_file='financial_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Finagentic crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
