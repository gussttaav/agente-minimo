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
| `b5-l4` | 35 · El prompt de sistema y el fichero de proyecto |
| `b5-l5` | 36 · Compactación: cuando la ventana se llena |
| `b5-l6` | 37 · Permisos y sandbox |
| `b5-l7` | 38 · Subagentes: un bucle dentro de otro |
| `b5-l8` | 39 · Un mini-benchmark: medir harness por modelo |
| `b5-l9` | 40 · MCP y lo que viene |

Cada lección enlaza dos etiquetas: la **anterior** donde empieza su paso de implementación
(«parte de aquí») y la **suya** donde termina («si te has perdido, este es el estado al final de
esta lección»). Ninguna lección enlaza `main`: `main` se mueve; una etiqueta, no.

Para partir de una lección concreta:

```bash
git clone --branch b5-l3 --depth 1 https://github.com/gussttaav/agente-minimo.git
cd agente-minimo
```

Las etiquetas se cortan cuando se revisa la lección, así que una etiqueta que todavía no existe
es una lección que todavía no se ha publicado.

## Versiones

<!-- TODO (COURSE-C2-P1-05): rellenar al publicar la lección 32, con las versiones exactas
     sobre las que se verificó cada etiqueta en una máquina limpia. Hasta entonces esta tabla
     está vacía a propósito: una versión sin verificar es peor que ninguna. -->

| Qué | Versión verificada |
|---|---|
| Python | ≥ 3.11 |
| Runner del modelo local | _pendiente_ |
| Modelo (16 GB de RAM) | _pendiente_ |
| Modelo (8 GB de RAM) | _pendiente_ |

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

Vacío de código, a propósito. Las lecciones lo llenan una a una, y cada etiqueta aparece con la
lección que la corta.

## Licencia

[MIT](LICENSE).
