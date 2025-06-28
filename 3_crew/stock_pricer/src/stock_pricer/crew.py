from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

class TrendingCompany(BaseModel):
    """ Una empresa que está en las noticias y atrayendo atención """
    name: str = Field(description="Nombre de la empresa")
    ticker: str = Field(description="Símbolo de la acción")
    reason: str = Field(description="Razón por la que esta empresa está en tendencia en las noticias")

class TrendingCompanyList(BaseModel):
    """ Lista de múltiples empresas en tendencia que están en las noticias """
    companies: List[TrendingCompany] = Field(description="Lista de empresas en tendencia en las noticias")

class TrendingCompanyResearch(BaseModel):
    """ Investigación detallada sobre una empresa """
    name: str = Field(description="Nombre de la empresa")
    market_position: str = Field(description="Posición actual del mercado y análisis competitivo")
    future_outlook: str = Field(description="Perspectiva futura y perspectivas de crecimiento")
    investment_potential: str = Field(description="Potencial de inversión y adecuación para inversión")

class TrendingCompanyResearchList(BaseModel):
    """ Una lista de investigaciones detalladas sobre todas las empresas """
    research_list: List[TrendingCompanyResearch] = Field(description="Investigación exhaustiva sobre todas las empresas en tendencia")


@CrewBase
class StockPicker():
    """Crew para seleccionar la mejor empresa para inversión"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'],
                     tools=[SerperDevTool()], 
                     memory = True)
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], 
                     tools=[SerperDevTool()])

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], 
                     tools=[PushNotificationTool()], 
                     memory = True)
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'],
        )
    



    @crew
    def crew(self) -> Crew:
        """Crea la crew para seleccionar la mejor empresa para inversión"""

        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )

        # Long-term memory for persistent storage across sessions
        long_term_memory = LongTermMemory(
            storage=LTMSQLiteStorage(
                db_path="./memory/long_term_memory_storage.db"
            )
        )

        # Short-term memory for current context using RAG
        short_term_memory = ShortTermMemory(
            storage = RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            )
        
        # Entity memory for tracking key information about entities
        entity_memory = EntityMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {
                        "model": 'text-embedding-3-small'
                    }
                },
                type="short_term",
                path="./memory/"
            )
        )
            
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,

            long_term_memory = long_term_memory,
            short_term_memory = short_term_memory,            
            entity_memory = entity_memory,
        )
