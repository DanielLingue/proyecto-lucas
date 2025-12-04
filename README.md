Proyecto Lucas: Asistente Financiero IA 🤖
Este proyecto es un prototipo funcional desarrollado para la cátedra de Inteligencia Artificial y Diversidad.
Descripción
Lucas es un agente interactivo que ayuda a jóvenes a organizar sus finanzas mediante un chat en lenguaje natural. Utiliza una arquitectura modular separando la lógica de negocio de la interfaz visual.
Estructura de Archivos
app.py (Frontend): - Contiene la interfaz gráfica construida con Streamlit.
Maneja la sesión del usuario (memoria del chat y saldo).
Renderiza los gráficos con Plotly.
finance_logic.py (Backend):
Procesamiento de Lenguaje Natural (NLP): Extrae montos y categorías de las frases del usuario sin necesidad de formularios.
Sistema RAG (Simulado): Base de conocimientos con respuestas educativas de la CMF y SERNAC.
requirements.txt: Lista de dependencias necesarias.
Cómo ejecutar el proyecto
Asegúrate de tener Python instalado.
Abre una terminal en la carpeta del proyecto.
Instala las librerías:
pip install -r requirements.txt

Ejecuta la aplicación:
streamlit run app.py

Funcionalidades Demo
Escribe "Gasté 5000 en el cine" -> Lo clasifica como Ocio.
Escribe "Gasté 20000 en el super" -> Lo clasifica como Necesidad.
Pregunta "¿Cómo invertir?" -> Responde con datos de la CMF.
