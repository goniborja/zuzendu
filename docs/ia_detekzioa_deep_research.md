# Detección probabilística de uso de IA y plagio asistido por IA en trabajos escolares

## Enfoque operativo y marco de investigación

En la práctica escolar, lo que realmente se intenta detectar **no es “IA sí/no”**, sino **una probabilidad de desajuste de autoría y proceso**: que el texto final (o partes significativas) no provenga del trabajo cognitivo y procedimental esperable del alumno bajo las reglas de la tarea (por ejemplo: escritura íntegra por un LLM, reescritura fuerte, “paraphrase outsourcing”, o mezcla humano‑IA sin trazabilidad). Este enfoque es coherente con cómo operan investigaciones de integridad académica que funcionan: **se acumula evidencia heterogénea y se valora “en balance de probabilidades”**, no como prueba absoluta ni como veredicto automático. citeturn34view3turn5view3turn5view4

El marco que mejor se sostiene (y que es aplicable en secundaria y bachillerato sin infraestructura especial) es un **modelo de triangulación** que conecta cuatro niveles exigidos:

- **Detección técnica / estilométrica**: señales de estilo, consistencia y procedencia textual; útiles como indicios, pero frágiles ante cambios de tema, nivel y reescritura. citeturn17view0turn18view0turn3view2  
- **Detección cognitiva / didáctica**: huellas del pensamiento de un alumno (comprensión situada, errores plausibles, decisiones retóricas, relación con el aula) frente a patrones típicos de producción de un LLM (fluidez homogénea, estructura “plantilla”, generalidad, tono neutral). citeturn16view0turn15view1turn20view0turn8view0  
- **Análisis contextual**: compatibilidad con el historial del alumno, el tiempo disponible, el tipo de tarea y el nivel educativo; instituciones que funcionan ponen mucho peso aquí (picos inesperados, incoherencias con clases, cambios bruscos). citeturn5view2turn4view2turn27view0  
- **Pruebas de resistencia**: preguntas y transformaciones que fuerzan trazabilidad (de ideas, de fuentes, de decisiones) y verifican dominio en vivo (minidefensas, reescrituras en condiciones nuevas). Es una pieza central en guías institucionales de investigación porque reduce la dependencia de “señales blandas” del texto final. citeturn5view3turn5view4turn27view0  

A la vez, este enfoque asume un hecho empírico clave: **la detección puramente automática del texto (como clasificación IA/humano) es vulnerable** a ataques de parafraseo/reescritura y a cambios de escenario; por ello los sistemas fiables **no descansan en un único indicador**, sino en evidencia acumulada y verificación humana. citeturn28view0turn7search3turn33view0  

## Modelo de criterios estructurado

El modelo se organiza en **cinco dominios de evidencia**. Dentro de cada dominio, cada criterio aporta **incrementos o decrementos de probabilidad**, nunca certeza. La regla de oro es: **un criterio aislado no acusa; varios criterios convergentes justifican verificación**. citeturn34view3turn5view3turn5view4  

### Evidencia de proceso y procedencia

#### Criterio de consistencia de metadatos y cronología del archivo

**Qué detecta.** Señales de que el archivo no fue producido con el proceso temporal típico del alumno: creación/última modificación muy próximas, historial de revisiones anómalamente corto, autor/creador no alineado, o incoherencias entre campos del documento. citeturn5view3turn34view2turn34view1  

**Por qué funciona.** En casos reales de suplantación/autoria externa, el texto suele llegar como “copia limpia” y el alumno solo añade portada o ajustes mínimos, lo que puede dejar una traza temporal comprimida y propiedades inconsistentes. Además, guías institucionales tratan la **inspección de propiedades del documento** como evidencia admisible junto a otras (no como prueba única). citeturn5view3turn34view2turn34view1  

**En qué casos falla.**  
- Si el alumno redacta en un entorno y entrega en otro (copiar‑pegar a un nuevo archivo o exportar a PDF), los metadatos pueden perderse o volverse “sospechosamente limpios” sin mala conducta. citeturn33view0turn34view2  
- Si hay edición en móvil/tablet o uso de plantillas, también cambia la huella temporal. Por eso este criterio solo pesa bien cuando se compara con el **patrón habitual del propio alumno** y con el **patrón del grupo**. citeturn34view2turn5view2  

#### Criterio de trazabilidad de borradores y evolución

**Qué detecta.** Capacidad del alumno para aportar (cuando la tarea lo requiere o cuando la verificación lo solicita) **borradores razonables**, notas, esquemas, fuentes consultadas y decisiones de revisión coherentes con el producto final. citeturn5view3turn5view4turn27view0  

**Por qué funciona.** Las guías que funcionan insisten en que la investigación no debe quedarse en el texto final: el alumno debe poder **defender el trabajo y aportar evidencia de proceso** (borradores con fecha, decisiones, cómo investigó). Este tipo de evidencia reduce falsos positivos cuando un texto “suena” diferente pero fue legítimo. citeturn5view3turn5view4turn27view0  

**En qué casos falla.**  
- Alumnos que trabajan “en limpio” o con hábitos de planificación mental pueden tener pocas trazas, especialmente en secundaria. Esa ausencia **no es** evidencia fuerte por sí misma. citeturn16view2turn34view2  
- Si se permitió explícitamente IA para ideación o corrección, puede haber proceso real aunque el borrador “se vea demasiado correcto”. Este criterio debe interpretarse según las reglas declaradas. citeturn36view0turn13view0  

### Evidencia estilométrica y de consistencia textual

#### Criterio de inconsistencias intra‑documento

**Qué detecta.** “Costuras” de estilo dentro del mismo trabajo: segmentos con densidad léxica, sintaxis, puntuación, registro o terminología que cambian de forma no explicable por sección/género (por ejemplo, un cuerpo sostenidamente escolar con un bloque que adopta voz académica adulta o una regularidad inusual). citeturn3view2turn17view0  

**Por qué funciona.** La investigación en **plagio intrínseco** muestra que, cuando no hay corpus externo, una vía es detectar **variación estilística anómala** dentro del documento (p.ej., perfiles de n‑gramas de caracteres para cuantificar cambios). El principio se traslada bien a “híbridos humano‑IA” o “patchwriting asistido” cuando la mezcla deja discontinuidades. citeturn3view2turn5view5  

**En qué casos falla.**  
- El estilo también cambia legítimamente por **carga cognitiva**, sección (introducción vs. análisis), fatiga o uso de fuentes con paráfrasis cercana. citeturn18view0turn19view1  
- Un alumno puede reescribir toda la entrega con ayuda externa (humana o IA) dejando un estilo homogéneo. Ahí este criterio pierde fuerza y deben pesar más proceso, fuentes y defensa. citeturn28view0turn27view0  

#### Criterio de distancia al “perfil base” del alumno en el tiempo

**Qué detecta.** Divergencia entre el trabajo actual y un **perfil longitudinal** del alumno (errores habituales, complejidad sintáctica, cohesión, léxico, forma de argumentar, formato), usando como referencia tareas previas comparables. citeturn5view2turn17view0  

**Por qué funciona.** Varias guías de integridad señalan explícitamente que comparar con **otras entregas del estudiante** es evidencia relevante cuando se sospecha autoría externa. citeturn4view0turn5view3  
Además, la estilometría parte de la idea de que ciertos marcadores de estilo se eligen en parte de forma inconsciente, y por ello pueden ser discriminativos (aunque nunca infalibles). citeturn17view0turn3view2  

**En qué casos falla.**  
- No hay “huella” completamente estable: el estilo varía con el tema y la dificultad; estudios en autoría académica muestran efectos pequeños pero reales de la tarea y del tamaño del texto, y la propia evaluación reconoce limitaciones y necesidad de cautela. citeturn18view0turn19view2turn17view0  
- En alumnado multilingüe, cambios de registro y corrección pueden reflejar apoyo legítimo (docente, familia) o desarrollo acelerado, no IA. Aquí el paso clave es verificación didáctica y contextual, no “castigo por escribir mejor”. citeturn13view0turn29view0  

#### Criterio de “estructura plantilla” y señales de producción estandarizada

**Qué detecta.** Frecuencia alta de estructuras retóricas estandarizadas: párrafos que arrancan con conectores secuenciales (“primero… además… por otro lado… en conclusión…”), formato excesivamente ordenado para el grupo, tono instructivo‑expositivo constante, neutralidad afectiva y poca variación de longitud/ritmo. citeturn20view1turn20view0turn8view0  

**Por qué funciona.** Estudios comparativos humano‑LLM encuentran diferencias recurrentes: los textos humanos tienden a mostrar más diversidad en longitud, estructura y emoción, mientras que los generados se aproximan con frecuencia a estructuras **formulaicas** y tono neutral/positivo; además, los LLM pueden tender a respuestas “promedio” poco personalizadas o poco profundas cuando se pide opinión. citeturn20view0turn20view1turn8view0  
En lingüística aplicada también se ha observado que los LLM pueden sobre‑usar construcciones muy frecuentes y expresiones formulaicas, frente a la variabilidad pragmática humana. citeturn8view3turn8view0  

**En qué casos falla.**  
- Muchos docentes enseñan precisamente esa estructura (texto argumentativo clásico), y alumnos excelentes la aplican. Por tanto, este criterio solo pesa cuando coincide con **otros** (p.ej., falta de trazabilidad, referencias problemáticas o incapacidad de defender decisiones). citeturn5view4turn34view3  
- Un LLM puede ser instruido para evitar esa “plantilla”, aumentar variabilidad y simular errores; hay evidencia de que el prompting puede reducir algunas diferencias percibidas entre humano y máquina, por lo que el criterio no es robusto por sí solo. citeturn20view0turn28view0  

### Evidencia cognitiva y didáctica

#### Criterio de especificidad situada y anclaje al aula

**Qué detecta.** Si el texto integra de forma precisa y verificable: actividades concretas vistas en clase, ejemplos locales, términos del temario usados con el sentido trabajado, o referencias a materiales específicos (no solo “Wikipedia dice…” sino “en el documental visto el día X se observa…”). La ausencia sistemática de anclaje, junto con generalidades, incrementa la probabilidad de generación externa. citeturn5view2turn20view0turn27view0  

**Por qué funciona.** Una señal fuerte descrita en estudios de detección humana/multilingüe es la **concreción**: textos humanos tienden a incluir detalles exactos (nombres, fechas, referencias), mientras que los generados tienden a generalizar y apoyar menos sus afirmaciones. citeturn20view0turn8view0  
Además, guías de evaluación contra autoría externa recomiendan tareas contextualizadas/personalizadas porque facilitan detectar irregularidades (y también favorecen aprendizaje profundo). citeturn5view0turn4view1turn27view0  

**En qué casos falla.**  
- Si la consigna no exigía anclaje (tema muy general) o si el alumno no asistió a una sesión clave.  
- Un LLM puede insertar detalles falsos; por eso este criterio debe combinarse con verificación (preguntas orales, comprobación de fuentes). citeturn8view2turn10search23  

#### Criterio de huellas de razonamiento y “errores plausibles” del aprendizaje

**Qué detecta.** Presencia (o ausencia) de rasgos típicos del aprendizaje real en secundaria/bachillerato: dudas razonables, simplificaciones, confusiones conceptuales localizadas, autocorrecciones, o decisiones argumentativas justificadas “a su manera”. En cambio, la prosa excesivamente “cerrada”, sin fricción, puede sugerir asistencia fuerte. citeturn16view2turn15view1turn20view1  

**Por qué funciona.** Modelos cognitivos de la escritura describen la producción humana como un proceso recursivo de planificación‑traducción‑revisión, con re‑evaluaciones y re‑planteamientos durante la redacción; esto suele dejar huellas en borradores y en la manera de explicar cómo se llegó al texto. citeturn16view0turn16view2  
En composición, la distinción “decir el conocimiento” vs “transformar el conocimiento” sugiere que muchos escritores en formación producen textos más lineales y dependientes de recuperación de ideas. Cuando aparece súbitamente una argumentación “madura” sin transición observable, aumenta la sospecha contextual (no prueba). citeturn15view1turn16view4  

**En qué casos falla.**  
- Alumnos muy competentes pueden escribir con mucha limpieza.  
- Alumnos que reciben apoyo explícito del docente (plantillas, andamiajes) pueden reducir “errores visibles” sin usar IA. Por eso los “errores que desaparecen” informan solo si además hay señales de proceso y verificación fallida. citeturn13view0turn5view4  

#### Criterio de calidad de fuentes, citas y verificabilidad

**Qué detecta.** Patrones de citación incompatibles con un trabajo escolar auténtico:  
- referencias inexistentes o inverificables,  
- mezcla de datos correctos con detalles bibliográficos erróneos,  
- citas “demasiado perfectas” pero que no corresponden al texto fuente,  
- bibliografías con coherencia formal pero baja coherencia epistémica (la fuente no sostiene la afirmación). citeturn8view2turn10search23turn10search25  

**Por qué funciona.** Hay evidencia sólida de que los LLM pueden generar referencias plausibles pero falsas (“alucinadas”) y que esto ocurre a tasas relevantes incluso con modelos avanzados; trabajos empíricos en ámbitos académicos/biomédicos muestran tasas altas de referencias fabricadas o inexactas y recomiendan validación rigurosa. citeturn8view2turn10search23turn10search15  
En integridad académica, “datos bibliográficos mal representados, referencias inapropiadas o material irrelevante” aparecen como patrones típicos en casos confirmados de autoría externa y se validan mediante conversación y evidencia. citeturn27view0turn5view4  

**En qué casos falla.**  
- Alumnado que no domina normas de citación puede cometer errores sin usar IA. Este criterio debe separar: *error de competencia* vs *patrón de fabricación/inautenticidad*. Guías de entrevistas insisten en dar oportunidad de explicación y usar la entrevista también como educación. citeturn5view4turn5view3  

### Evidencia contextual y longitudinal

#### Criterio de salto de rendimiento y coherencia con el nivel

**Qué detecta.** Picos inesperados: salto brusco de notas, cambio repentino de voz/registro/precisión, o desempeño muy superior al habitual sin explicación contextual (tutorías, trabajo guiado, tiempo extra, etc.). citeturn4view2turn5view2  

**Por qué funciona.** Guías institucionales señalan explícitamente la vigilancia de “picos inesperados” y la necesidad de conocer estilos y capacidades del alumnado para interpretar indicios. citeturn4view2turn5view2  

**En qué casos falla.**  
- Mejoras reales existen (especialmente tras feedback o apoyo). De hecho, revisiones sistemáticas sobre IA como retroalimentación muestran mejoras en precisión lingüística y organización: un alumno puede “subir” por apoyo legítimo (humano o herramienta permitida). citeturn13view0turn11view1  
- Por justicia, este criterio exige corroboración mediante proceso y resistencia; no se debe “penalizar el progreso”. citeturn34view3turn5view4  

### Evidencia por pruebas de resistencia

#### Criterio de defensa oral o entrevista de autoría

**Qué detecta.** Capacidad del alumno para explicar (sin apoyo externo) el contenido, las decisiones y las fuentes: definiciones de sus propios términos, por qué eligió ejemplos, cómo conectó ideas, y cómo respondería a objeciones. citeturn5view3turn5view4turn5view3  

**Por qué funciona.** Varias guías recomiendan entrevista/defensa oral como vía especialmente útil para evaluar si el estudiante completó el trabajo o lo externalizó; también advierten de que la entrevista debe servir para reunir evidencia, permitir explicaciones y sostener equidad procedimental. citeturn5view3turn5view4turn5view3  

**En qué casos falla.**  
- Un alumno tímido o con ansiedad puede rendir peor oralmente. Mitigación: preguntas graduadas, posibilidad de preparar un esquema breve, y enfoque en comprensión más que en elocuencia. citeturn5view4turn5view3  
- Si el alumno ensayó una defensa con ayuda, puede pasar; por eso conviene incluir “pruebas de cambio” (ver criterio siguiente). citeturn27view0  

#### Criterio de transformaciones controladas y trazado de afirmaciones

**Qué detecta.** Robustez del dominio cuando se cambia una condición: reescribir un párrafo con un contra‑argumento nuevo, justificar una afirmación con evidencia específica, o adaptar el texto a un público distinto manteniendo el contenido. citeturn5view0turn27view0turn20view0  

**Por qué funciona.** Los sistemas que funcionan recomiendan combinar evaluación escrita con modalidades orales/auténticas y usar procedimientos de verificación cuando hay sospecha. La lógica es simple: si el alumno **posee** el modelo mental del trabajo, puede transformarlo de forma coherente y defenderlo; si solo posee el producto final, la transformación suele romper coherencia o producir generalidades. citeturn5view0turn5view3turn16view0  

**En qué casos falla.**  
- Un LLM también puede transformar textos con facilidad. La diferencia práctica aparece cuando las transformaciones exigen **datos no presentes en el texto** (material de clase, decisiones personales registradas, fuentes reales consultadas por el alumno) y cuando se pide justificar “por qué” (no solo producir). citeturn20view0turn8view2  

## Pruebas de resistencia que más discriminan en secundaria y bachillerato

Estas pruebas no pretenden “pillar”, sino **verificar trazabilidad** y reducir falsos positivos. Su fuerza aumenta si se aplican como parte normal del curso (aleatorio o universal en tareas de alto impacto), porque evitan el sesgo de seleccionar solo a “sospechosos” y refuerzan equidad. citeturn5view3turn5view0  

### Minidefensa de autoría orientada a proceso

Funciona como una entrevista breve (6–10 minutos) con tres bloques: (a) investigación, (b) decisiones, (c) comprensión. En guías de investigación se recomienda explícitamente usar entrevistas para comprobar comprensión, recoger evidencia y permitir explicaciones alternativas. citeturn5view4turn5view3  

Ejemplos de preguntas con alta sensibilidad (adaptables por materia):
- “Elige dos frases tuyas y dime de dónde sale cada idea: ¿apunte, libro, vídeo, conversación en clase?”  
- “¿Qué descartaste y por qué? (un ejemplo de idea que no usaste)”  
- “Enséñame una fuente y explícame qué parte exacta te sirvió (sin leerla, solo ubicándola).”  
- “Si tu tesis fuera falsa, ¿qué evidencia la refutaría?” (verifica estructura argumental y epistemología escolar).  

### Trazado de afirmaciones y auditoría de referencias

Pide un “mapa de afirmaciones” en el que 5–8 frases del trabajo se vinculan a fuente o experiencia de aula. Este procedimiento explota dos hechos empíricos: (1) los LLM pueden producir referencias fabricadas o inexactas con frecuencia relevante; (2) los patrones de referencias mal representadas o inapropiadas aparecen en casos confirmados de autoría externa. citeturn8view2turn10search23turn27view0  

### Transformación con restricción local

La transformación más discriminativa no es “reescribe mejor”, sino “reescribe con un recurso que solo existe en tu clase”. Por ejemplo:
- Historia: “Incluye un concepto del tema visto esta semana y relaciona tu argumento con un documento trabajado en clase.”  
- Lengua: “Reformula el segundo párrafo para un público de 12 años y añade un ejemplo de tu vida cotidiana; mantiene la idea central.”  
- Biología: “Reescribe la explicación usando el esquema X del cuaderno (nombra las partes) y añade una limitación del modelo.”

Esto se apoya en la evidencia de que lo humano tiende a ser más concreto y situado, mientras lo generado tiende a generalidades y estructura formulaica, aunque el prompting puede cerrar parcialmente la brecha si no hay restricción local. citeturn20view0turn20view1  

### Variación de consigna en vivo

En 10–15 minutos en clase (sin dispositivos), pedir un microtexto nuevo sobre el mismo tema (150–250 palabras) permite comparar:
- registro,
- tipo de ejemplos,
- patrones de cohesión,
- errores característicos.

No es “prueba de autoría”, pero sí un **ancla contextual** que vuelve más interpretables los criterios estilométricos. Esto está alineado con la idea de trabajar con portafolio y balance de evidencias, no con un indicador único. citeturn34view3turn17view0  

## Propuestas de aplicación práctica

### Rúbrica docente orientada a probabilidad

La rúbrica puntúa **fuerza de evidencia**, no culpabilidad. Escala sugerida por dimensión:  
0 = no aporta evidencia (o evidencia contraria), 1 = indicio débil, 2 = indicio moderado, 3 = indicio fuerte.

Dimensiones (alineadas con el modelo anterior):

**Proceso y procedencia (0–3).** Metadatos plausibles, borradores, coherencia temporal y de archivo. citeturn5view3turn34view2turn34view3  

**Consistencia textual (0–3).** Sin costuras internas; el estilo no cambia de forma inexplicable; coherencia de registro y terminología. citeturn3view2turn5view5turn17view0  

**Anclaje al aula y especificidad (0–3).** Uso de detalles verificables, materiales de clase, ejemplos situados, precisión conceptual al nivel esperado. citeturn20view0turn5view2turn5view0  

**Fuentes y verificabilidad (0–3).** Referencias reales, trazables y coherentes; ausencia de patrones típicos de referencias fabricadas o bibliografía “bonita pero falsa”. citeturn8view2turn10search23turn27view0  

**Resistencia (0–3).** Resultado de minidefensa/transformación: capacidad de explicar, modificar con restricción local y sostener el argumento. citeturn5view3turn5view4turn5view0  

Interpretación **probabilística** recomendada (heurística, no mecánica):
- 0–4: probabilidad baja de uso indebido; si hay problemas, suelen ser de competencia (citación, organización).  
- 5–9: probabilidad moderada; activar verificación ligera (entrevista breve + trazado de 3 afirmaciones).  
- 10–15: probabilidad alta; activar protocolo completo (evidencia documental + entrevista estructurada + re‑tarea controlada).  

Este enfoque encaja con la lógica institucional de reunir evidencia y valorar “en balance de probabilidades”, no como certeza. citeturn34view3turn5view4  

### Protocolo de verificación realista para un centro

**Marco previo (preventivo).**  
Definir por escrito qué usos están permitidos (p. ej., corrección lingüística, ideación, resumen) y qué usos requieren declaración (p. ej., redacción de secciones completas). La claridad reduce conflictos y dirige la verificación hacia el proceso y el aprendizaje. citeturn36view0turn5view0  

**Triage inicial (docente corrector).**  
Detectar “banderas” sin acusar: pico de rendimiento, falta de alineación con clases, bibliografía rara, estructura excesivamente plantilla. Registrar observaciones concretas. citeturn4view2turn27view0turn20view1  

**Recogida mínima de evidencia.**  
Solicitar: (a) borradores o notas, (b) lista de fuentes consultadas, (c) archivo original si procede, (d) explicación breve del proceso (5–8 líneas). citeturn5view3turn5view4turn34view2  

**Verificación de fuentes (centrada en hechos).**  
Seleccionar 3–5 citas/afirmaciones y comprobar que existen y apoyan lo afirmado. Esto es crítico porque la fabricación de referencias es un fallo bien documentado en LLM. citeturn8view2turn10search23turn10search25  

**Entrevista breve con enfoque educativo.**  
Objetivos: comprobar comprensión, ofrecer oportunidad de explicación, recoger evidencia y, si procede, orientar a recursos de apoyo. citeturn5view4turn5view3  

**Prueba de resistencia proporcional.**  
Si persiste la probabilidad moderada/alta: micro‑reescritura con restricción local en aula (10–15 min) o defensa oral de 5 preguntas. citeturn5view0turn5view3  

**Decisión y documentación.**  
Separar: (a) mala práctica por desconocimiento (intervención pedagógica), (b) uso indebido probable (aplicar normativa del centro), (c) incertidumbre alta (opción conservadora: re‑evaluación alternativa). El principio operativo en guías expertas es que no siempre habrá “tell‑tales” y una tarea honesta puede mostrar señales; por tanto la decisión debe basarse en evidencia acumulada, no en una sola. citeturn34view3turn5view2turn27view0  

### Base para un prompt evaluador de otra IA

El objetivo de este prompt no es “que la IA decida”, sino que **ayude a estructurar la revisión** con el mismo modelo de criterios, explicitando evidencias textuales y proponiendo preguntas de verificación.

```text
Rol: Asistente de integridad académica para secundaria/bachillerato.
Tarea: Analiza el texto del alumno y devuelve una estimación probabilística (baja/media/alta) de:
(A) uso de LLM para redacción sustancial, y/o
(B) plagio o plagio asistido (paráfrasis sin atribución),
indicando SIEMPRE incertidumbre y riesgos de falso positivo.

Entrada que recibirás:
1) Enunciado/tarea y nivel educativo.
2) Texto entregado.
3) (Opcional) Dos muestras previas del alumno + notas del docente sobre su estilo habitual.
4) (Opcional) Lista de fuentes declaradas por el alumno.

Instrucciones:
- NO uses una decisión binaria.
- NO bases tu evaluación solo en señales estadísticas del texto.
- Estructura el análisis en 5 dominios:
  1) Proceso/Procedencia (solo si hay datos: borradores, metadatos, etc.)
  2) Consistencia textual intra-documento
  3) Consistencia con el perfil del alumno (si hay muestras)
  4) Cognitivo-didáctico (profundidad, anclaje al aula, plausibilidad de razonamiento)
  5) Fuentes y verificabilidad (calidad de citas, señales de referencias inventadas)
- Para cada dominio, produce:
  a) Observaciones específicas citando fragmentos del texto (copiar 1–2 frases cortas).
  b) Interpretación: por qué eso aumenta o disminuye la probabilidad.
  c) Cómo podría fallar esa señal (alternativas inocentes).
- Genera al final:
  - “Estimación”: baja/media/alta para A y B por separado, con explicación.
  - “Preguntas de verificación”: 6–10 preguntas concretas para una minidefensa oral o re-tarea en aula.
  - “Comprobaciones de fuente”: lista de 5 afirmaciones del texto que deberían rastrearse a una fuente real.

Salida en formato JSON con campos:
{ contexto, dominio1, dominio2, dominio3, dominio4, dominio5, estimacion, preguntas_verificacion, comprobaciones_fuente, advertencias_falsos_positivos }
```

Este uso debe respetar privacidad y proporcionalidad: organismos internacionales advierten que centros educativos deben proteger datos, validar la pertinencia pedagógica y ser cautelosos con impactos a largo plazo. citeturn37view0turn37view1  

## Limitaciones y riesgos de falsos positivos

La detección de IA/plagio asistido **tiene límites estructurales** y debe operar con garantías. Cinco riesgos principales:

**Fragilidad ante reescritura y ataques.** La evidencia muestra que detectores de texto IA pueden ser debilitados mediante parafraseo recursivo con degradación limitada de calidad; esto impone un techo a la fiabilidad del “texto‑solo” en escenarios adversarios. citeturn28view0turn7search3  

**Sesgos contra ciertos grupos.** Evaluaciones han encontrado que detectores pueden clasificar erróneamente escritura de no nativos como “IA”, lo que hace especialmente peligroso usar señalización automática como base sancionadora en educación. citeturn29view0  

**Variabilidad legítima del estilo.** La escritura cambia con tema, carga cognitiva, longitud del texto y andamiaje docente; incluso investigaciones de verificación de autoría discuten limitaciones por tamaño y generalización. citeturn18view0turn19view3turn17view0  

**Ambigüedad de “mejora súbita”.** El uso (permitido o no) de herramientas de retroalimentación puede mejorar precisión lingüística y organización; también el apoyo docente o familiar puede producir saltos reales. Penalizar “escribir demasiado bien” es un error frecuente y éticamente dañino. citeturn13view0turn5view2turn34view3  

**Daño por procedimiento injusto.** Guías de integridad subrayan que entrevistas/defensas deben diseñarse para equidad (permitir defensa, registrar evidencia, independencia) y que las sospechas pueden tener explicación razonable. citeturn5view3turn5view4turn5view3  

Mitigación práctica recomendada:
- **No usar un solo criterio** (ni estilométrico ni “sensación docente”) como base de decisión. citeturn34view3turn17view0  
- **Aplicar verificación proporcional** (de menor a mayor intrusión) y documentar. citeturn5view4turn34view3  
- **Diseñar evaluación mixta** (escrita + oral/auténtica) para que la verificación sea parte del aprendizaje, no solo “policía”. citeturn5view0turn4view1  

En síntesis: los métodos que funcionan en centros reales no dependen de “detectar IA” como si fuera una huella química; dependen de **triangulación** (texto + proceso + contexto + resistencia) y de un estándar probatorio educativo (“más probable que…”) con garantías y foco didáctico. citeturn34view3turn5view4turn28view0