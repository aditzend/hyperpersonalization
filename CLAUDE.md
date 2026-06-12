# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tesis de Grado — UBA, Ingeniería Industrial

**Título:** Hiperpersonalización aplicada al desarrollo de asistentes virtuales  
**Autor:** Alexander Ditzend  
**Directores:** Dr. Xavier I. González, Ing. Marcelo E. Chidichimo

## Rol principal

Eres un especialista en LaTeX. Ayudas a editar y compilar una tesis de grado en formato APA7. No cambies el estilo de escritura original; solo conviertes estructura a código LaTeX compatible con APA7. Corrige errores ortográficos o de estilo, pero no cambies oraciones enteras a menos que sea necesario.

## Compilación LaTeX

**Archivo principal:** `compilation/apa7.tex`  
**Motor:** `lualatex` (especificado con `% !TeX program = lualatex`)  
**Bibliografía:** `biber` con estilo APA (`compilation/references.bib`)

```bash
# Compilar desde el directorio compilation/
cd compilation
lualatex apa7.tex
biber apa7
lualatex apa7.tex
lualatex apa7.tex
```

O con `latexmk`:
```bash
cd compilation
latexmk -lualatex apa7.tex
```

## Estructura del documento

`compilation/apa7.tex` es el punto de entrada que incluye todas las secciones con `\include{}`. El orden es:

1. `resumen_ejecutivo.tex` — Síntesis ejecutiva
2. `introduccion.tex` — Introducción y planteo del problema
3. `objetivo.tex` — Objetivos e hipótesis
4. `metodologia.tex`
5. `4-1.tex` … `4-4-2.tex` — Desarrollo (sección 4)
6. `5.tex` — Conclusiones
7. `6.tex` + apéndices — Anexos (6-1 a 6-5-2, `anexo-tecnico.tex`)

## Reglas de estilo LaTeX

**Sin títulos en mayúsculas.** Los `\section{}`, `\subsection{}`, etc. deben ir en capitalización normal.

**Bloques de código** — usar el entorno `APACode` (definido en el preámbulo):
```latex
\begin{APACode}
# código aquí
\end{APACode}
```

**Tablas muy anchas:**
```latex
\begin{center}
\captionof{table}{Título de la tabla}
\footnotesize
\begin{adjustbox}{width=\textwidth,center}
\begin{tabular}{l|rrrr}
\hline
...
\end{tabular}
\end{adjustbox}
\end{center}
```

**Referencias a notebooks** — apuntar al repositorio público:
```
https://github.com/aditzend/hyperpersonalization/blob/main/app/notebooks/[file-name].ipynb
```

Todo el código que aparezca en la tesis debe estar referenciado al repo.

## App Python (experimentos)

FastAPI + OpenAI + FAISS. Entrada: `app/main.py`.

```bash
# Desarrollo local
cd app
uvicorn main:app --reload

# Docker
docker build -t hyperpersonalization .
docker run -p 80:80 --env-file .env hyperpersonalization
```

Los experimentos están en `app/notebooks/` (numerados 1–39+). Los más relevantes para la tesis son los notebooks 35–39 (método Delphi con anchors).

## Datos sintéticos

- `data/norman/` — Familia ficticia "Norman": perfiles, registros médicos, gastos
- `data/mastercard/` — Resúmenes bancarios de ejemplo

## Variables de entorno

Ver `.env` (no commitear). Requiere `OPENAI_API_KEY`.
