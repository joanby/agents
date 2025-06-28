from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio

class ResearchManager:

    async def run(self, query: str):
        """ Ejecuta el proceso de investigación profunda, generando los actualizaciones de estado y el informe final """
        trace_id = gen_trace_id()
        with trace("Ingestigación", trace_id=trace_id):
            print(f"Ver traza: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"Ver traza: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Iniciando investigación...")
            search_plan = await self.plan_searches(query)
            yield "Búsquedas planificadas, iniciando búsqueda..."     
            search_results = await self.perform_searches(search_plan)
            yield "Búsquedas completas, escribiendo informe..."
            report = await self.write_report(query, search_results)
            yield "Informe escrito, enviando correo electrónico..."
            await self.send_email(report)
            yield "Correo electrónico enviado, investigación completa"
            yield report.markdown_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Planifica las búsquedas a realizar para la consulta """
        print("Planificando búsquedas...")
        result = await Runner.run(
            planner_agent,
            f"Consulta: {query}",
        )
        print(f"Se realizarán {len(result.final_output.searches)} búsquedas")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Realiza las búsquedas para la consulta """
        print("Buscando...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Buscando... {num_completed}/{len(tasks)} completadas")
        print("Búsqueda completada")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Realiza una búsqueda para la consulta """
        input = f"Término de búsqueda: {item.query}\nRazón para buscar: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Escribe el informe para la consulta """
        print("Pensando en el informe...")
        input = f"Consulta original: {query}\nResultados de búsqueda resumidos: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Informe escrito")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        print("Escribiendo correo electrónico...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Correo electrónico enviado")
        return report