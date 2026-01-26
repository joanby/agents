# Contexto del directorio – Template

**INSTRUCCIONES**: Este archivo contiene un template con datos de ejemplo. Reemplaza los valores placeholder (ej. `categoria1`, `ciudad1`, `creador1`) con tus datos reales del directorio.

## Objetivos del magazine

- Artículos SEO (guías, top list, noticias, tutoriales) en **español** (o el idioma de tu audiencia).
- Enlaces internos a **categorías**, **ciudades** y **perfiles de creadores** donde sea pertinente.
- Tono: profesional y elegante, accesible.
- Cada artículo debe dar valor al lector y conducir hacia el directorio (perfiles, categorías, ciudades).

## Categorías (slug para enlaces)

| Slug | Nombre |
|------|--------|
| categoria1 | Categoría Ejemplo 1 |
| categoria2 | Categoría Ejemplo 2 |
| categoria3 | Categoría Ejemplo 3 |
| categoria4 | Categoría Ejemplo 4 |
| categoria5 | Categoría Ejemplo 5 |

**URL base**: `/categorias/{slug}` (ej. `/categorias/categoria1`).

**Cómo personalizar**: Reemplaza `categoria1`, `categoria2`, etc. con tus categorías reales. Añade o elimina filas según necesites. El slug debe coincidir con la estructura de URLs de tu aplicación.

## Ciudades (para enlaces)

| Slug | Ciudad |
|------|--------|
| ciudad1 | Ciudad Ejemplo 1 |
| ciudad2 | Ciudad Ejemplo 2 |
| ciudad3 | Ciudad Ejemplo 3 |
| ciudad4 | Ciudad Ejemplo 4 |

**URL base**: `/ciudades/{slug}` (ej. `/ciudades/ciudad1`).  
Filtro por ciudad + categoría: `/ciudades/{ciudad}/categoria/{categoria}`.

**Cómo personalizar**: Reemplaza con tus ciudades reales. Ajusta los slugs según tu estructura de URLs.

## Ejemplo de creadores (para enlaces internos)

| Slug | Nombre | Categoría | Ciudad |
|------|--------|-----------|--------|
| creador1 | Creador Ejemplo 1 | categoria1 | ciudad1 |
| creador2 | Creador Ejemplo 2 | categoria2 | ciudad2 |
| creador3 | Creador Ejemplo 3 | categoria3 | ciudad3 |

**URL perfil**: `/perfiles/{slug}` (ej. `/perfiles/creador1`).

**Cómo personalizar**: Reemplaza con tus creadores reales. Asegúrate de que los slugs coincidan con los de tu base de datos o sistema de gestión de contenido.

## Guías para artículos

1. **Título y meta**: incluir keywords principales, máximo ~60 caracteres título, ~155 meta description.
2. **Estructura**: H1 único, H2/H3 para secciones; párrafos breves, listas donde sea útil.
3. **Enlaces internos**: insertar 2–5 enlaces a categorías/ciudades/perfiles donde el contexto sea relevante. Usar anclas naturales (ej. «creadores de [categoría]», «[ciudad]»).
4. **CTA**: cierre con invitación a explorar el directorio (categorías, ciudades, perfiles destacados).
5. **Idioma**: solo español (o el idioma de tu audiencia); evitar anglicismos innecesarios.

## Cómo poblar este archivo

- **Opción 1 (Manual)**: Edita este archivo directamente y reemplaza los placeholders con tus datos.
- **Opción 2 (Script)**: Crea un script que exporte desde tu base de datos (ej. consulta SQL o export desde CMS) y genere este archivo en formato markdown.
- **Opción 3 (API)**: Si tu directorio tiene una API, puedes crear un script que la consulte y genere este archivo.

**Formato esperado**: Mantén la estructura markdown con tablas. Los slugs deben ser consistentes con tu aplicación.
