# Prompt de Evaluación de Toxicidad

Evalúa el siguiente mensaje de usuario y determina si contiene lenguaje inapropiado, tóxico o ofensivo.

**Mensaje del usuario:**
{{ message }}

**Historial de conversación:**
{{ history }}

Responde ÚNICAMENTE en formato JSON:

```json
{
  "classification": "ACCEPTABLE" | "NOT_ACCEPTABLE",
  "toxicity_score": 0.0-1.0,
  "reason": "Breve explicación de la evaluación"
}
```

Criterios:
- Score 0.0-0.3: Mensaje completamente aceptable
- Score 0.3-0.7: Mensaje potencialmente problemático (contexto dependiente)
- Score 0.7-1.0: Mensaje claramente tóxico o inapropiado (debe bloquearse)
