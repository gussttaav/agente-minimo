# agente-minimo

El repositorio de acompañamiento del **bloque 5** del curso
[Modelos de Lenguaje: del Transformer al Agente](https://gustavoai.dev/cursos/llm-agents):
un agente de programación en la terminal, escrito desde cero en Python, contra un modelo
de lenguaje que corre en tu máquina.

> *English:* the companion repository of Block 5 of the course above. The lessons are in
> Spanish; the code and this README follow them.

## Qué es y qué no es

**La lección es la fuente de verdad; este repositorio es la copia.** Cada lección del bloque
muestra su código en bloques de texto y tú lo escribes en tu propio repositorio. Lo que hay
aquí es un *punto de control* por lección — el estado exacto del programa al terminar cada una —
para que, si te pierdes en la sexta, puedas clonar la quinta y seguir. No es un proyecto para
usar: es el que vas a escribir tú.

## Las etiquetas

Una etiqueta por lección, `b5-l1` … `b5-l9`, cortada del código de la lección revisada:

| Etiqueta | Lección |
|---|---|
| `b5-l1` | 32 · Preparar la máquina: un modelo local y la API de mensajes |
| `b5-l2` | 33 · El bucle con un modelo real |
| `b5-l3` | 34 · Herramientas: leer, buscar, editar, ejecutar |
| `b5-l4` | El inicio de M tiene dos voces: `agente.py` trae un prompt de sistema nuevo (las reglas del agente en cualquier repositorio) y lee el fichero de proyecto, `AGENTE.md`, si la carpeta tiene uno, en un segundo mensaje de sistema. `ejemplo/AGENTE.md` (cómo se ejecutan sus tests), `coste.py` (lo que ocupa cada pieza fija de M en la ventana) y `tests/test_inicio.py`. `bucle.py`, `api.py`, `permisos.py`, `herramientas/` y `correr.py` no cambian. |
| `b5-l4` | 35 · El prompt de sistema y el fichero de proyecto |
| `b5-l5` | 36 · Compactación: cuando la ventana se llena |
| `b5-l6` | 37 · Permisos y sandbox |
| `b5-l7` | 38 · Subagentes: un bucle dentro de otro |
| `b5-l8` | 39 · Un mini-benchmark: medir harness por modelo |
| `b5-l9` | 40 · MCP y lo que viene |

Cada lección enlaza dos etiquetas: la **anterior** donde empieza su paso de implementación
(«parte de aquí») y la **suya** donde termina («si te has perdido, este es el estado al final de
esta lección»). Ninguna lección enlaza `main`: `main` se mueve; una etiqueta, no.

Para partir de una lección concreta, clona su etiqueta. `--branch` acepta tanto una rama como
una etiqueta, y aquí sólo hay etiquetas:

```bash
git clone --branch b5-l3 --depth 1 https://github.com/gussttaav/agente-minimo.git
cd agente-minimo
git switch -c mi-agente
```

Git avisará de que la etiqueta «is not a commit» y de que no estás en ninguna rama: las dos
cosas son normales. La última orden crea tu propia rama, para que lo que escribas a partir de
aquí quede guardado en ella.

Si más adelante te pierdes y quieres saltar a otra etiqueta sin clonar de nuevo:

```bash
git fetch --depth 1 origin tag b5-l5
git switch -c desde-l5 b5-l5
```

Las etiquetas se cortan cuando se revisa la lección, así que una etiqueta que todavía no existe
es una lección que todavía no se ha publicado.

## Versiones

<!-- COURSE-C2-P1-05: verificado el 2026-10-30 con la etiqueta b5-l1. El bloque se verifica con
     un solo modelo; uno mayor (16 GB de RAM) sólo se mide en la lección 39. -->

| Qué | Versión verificada |
|---|---|
| Python | ≥ 3.11 (verificado con 3.14) |
| Runner del modelo local | Ollama 0.40.13 |
| Modelo | `qwen3:4b-instruct` (Q4_K_M, unos 2.5 GB; funciona con 8 GB de RAM y sin GPU) |

El código sólo nombra un modelo, `local`, que creas con el `Modelfile`: el fichero dice de qué
modelo partir y fija la ventana de contexto del curso, 8192 tokens.

```bash
ollama pull qwen3:4b-instruct
ollama create local -f Modelfile
```

Con más memoria puedes cambiar la línea `FROM` del `Modelfile` por un modelo mayor y volver a
crear `local`. El código no cambia; las salidas esperadas de las lecciones son las del modelo de
la tabla.

El runner y las etiquetas de los modelos son *versiones*, no el objeto del curso: el programa
habla un protocolo de mensajes sobre `urllib` y `json`, sin SDK, y cambiar de runner es cambiar
una URL, no reescribir nada.

## Cómo está organizado

La organización sigue el orden de las lecciones — el orden de los ficheros es el orden en que
los escribes — y la fija la lección de proyecto del bloque 4, donde el agente ya es este
programa con un `modelo` guionizado. Lo que este README compromete:

- **Una interfaz, dos adaptadores.** El bucle habla con `modelo(mensajes, herramientas) ->
  respuesta` y nada más. Un adaptador implementa esa interfaz sobre la API de mensajes de un
  modelo local; el otro es un modelo guionizado, para las pruebas. El agente es el mismo
  programa con un `modelo` distinto.
- **Un fichero por herramienta** (`leer`, `buscar`, `editar`, `escribir`, `ejecutar`), **uno
  para el bucle, uno para los permisos, uno para la compactación.**
- **`tareas/`**: los cinco repositorios diminutos del mini-benchmark de la lección 39, cinco
  ficheros cada uno.
- **Python ≥ 3.11 y la biblioteca estándar.** Sin dependencias: eso también es parte de lo que
  enseña. No hace falta un entorno virtual; las lecciones lo muestran igualmente por costumbre.

## Estado

| Etiqueta | Qué hay |
|---|---|
| `b5-l1` | El agente del bloque 4, en ficheros y sobre el modelo guionizado (`guionizado.py`, `entorno.py`, `permisos.py`, `bucle.py`, `agente.py`, `tests/`), el `Modelfile` y `protocolo.py`, un turno del protocolo hecho a mano. `python -m unittest` pasa sin el servidor. |
| `b5-l2` | El adaptador `api.py` (`ModeloAPI`, la firma de `modelo` sobre la API de mensajes, con `urllib` y `json`), `correr.py` (un pedido contra el modelo local, turno a turno) y `tests/test_api.py`. Ningún fichero de `b5-l1` cambia. |
| `b5-l3` | El entorno es una carpeta de tu disco. `herramientas/`, un fichero por herramienta (`leer`, `buscar`, `editar`, `escribir`, `ejecutar`) con lo que lee el modelo, su clase y su función; `ejemplo/`, un proyecto de dos ficheros con dos tests que no pasan; `tests/test_herramientas.py`. `correr.py` trabaja sobre una copia de una carpeta y pregunta antes de cada escritura y cada comando. `bucle.py`, `agente.py`, `api.py` y `guionizado.py` no cambian. |

## Licencia

[MIT](LICENSE).
