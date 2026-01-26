# src/direttorio/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from direttorio.tools.keyword_research_tool import KeywordResearchTool


@CrewBase
class DirettorioCalendarCrew:
    """Crew para crear el plan editorial 15-20 días."""

    tasks_config = "config/tasks_calendar.yaml"

    @agent
    def especialista_calendario_editorial(self) -> Agent:
        return Agent(
            config=self.agents_config["especialista_calendario_editorial"],
            verbose=True,
        )

    @task
    def tarea_calendario_editorial(self) -> Task:
        return Task(config=self.tasks_config["tarea_calendario_editorial"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


@CrewBase
class DirettorioArticleCrew:
    """Crew para artículo: plan estratégico, copywriter, SEO, enlaces, calidad, manager, actualización calendario."""

    @agent
    def planificador_estrategico(self) -> Agent:
        return Agent(
            config=self.agents_config["planificador_estrategico"],
            verbose=True,
        )

    @agent
    def investigador_keywords(self) -> Agent:
        return Agent(
            config=self.agents_config["investigador_keywords"],
            verbose=True,
            tools=[KeywordResearchTool()],
        )

    @agent
    def investigador_contenido(self) -> Agent:
        return Agent(
            config=self.agents_config["investigador_contenido"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def copywriter_profesional(self) -> Agent:
        return Agent(
            config=self.agents_config["copywriter_profesional"],
            verbose=True,
        )

    @agent
    def editor_seo(self) -> Agent:
        return Agent(
            config=self.agents_config["editor_seo"],
            verbose=True,
        )

    @agent
    def especialista_enlaces(self) -> Agent:
        return Agent(
            config=self.agents_config["especialista_enlaces"],
            verbose=True,
        )

    @agent
    def corrector_calidad(self) -> Agent:
        return Agent(
            config=self.agents_config["corrector_calidad"],
            verbose=True,
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"],
            verbose=True,
        )

    @agent
    def actualizador_calendario(self) -> Agent:
        return Agent(
            config=self.agents_config["actualizador_calendario"],
            verbose=True,
        )

    @task
    def tarea_plan_estrategico(self) -> Task:
        return Task(config=self.tasks_config["tarea_plan_estrategico"])

    @task
    def tarea_investigacion_keywords(self) -> Task:
        return Task(config=self.tasks_config["tarea_investigacion_keywords"])

    @task
    def tarea_investigacion_contenido(self) -> Task:
        return Task(config=self.tasks_config["tarea_investigacion_contenido"])

    @task
    def tarea_escribir_articulo(self) -> Task:
        return Task(config=self.tasks_config["tarea_escribir_articulo"])

    @task
    def tarea_editar_seo(self) -> Task:
        return Task(config=self.tasks_config["tarea_editar_seo"])

    @task
    def tarea_especialista_enlaces(self) -> Task:
        return Task(config=self.tasks_config["tarea_especialista_enlaces"])

    @task
    def tarea_correccion_calidad(self) -> Task:
        return Task(config=self.tasks_config["tarea_correccion_calidad"])

    @task
    def tarea_aprobacion_manager(self) -> Task:
        return Task(config=self.tasks_config["tarea_aprobacion_manager"])

    @task
    def tarea_actualizar_calendario(self) -> Task:
        return Task(config=self.tasks_config["tarea_actualizar_calendario"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
