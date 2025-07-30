custom_css = """
/* Fondo general blanco y tipografía sobria */
body, .gradio-container {
  background-color: #ffffff;
  color: #202123;
  font-family: 'Segoe UI', Arial, sans-serif;
  margin: 0;
  padding: 0;
}

/* Cabecera principal: misma disposición, colores más neutros */
#header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #202123;
}

/* Subtítulo con gris suave */
#subtitle {
  color: #5f6368;
  margin-bottom: 2rem;
}

/* Pestañas: desactivamos el fondo azul y usamos una línea inferior gris */
.gradio-tabs {
  border-bottom: 1px solid #e8e8e8;
}
.gradio-tabs .tabitem {
  color: #202123;
  font-weight: 500;
  padding: 0.5rem 1rem;
}
.gradio-tabs .tabitem.selected {
  border-bottom: 2px solid #202123;
}
.gradio-tabs .tabitem:hover {
  background-color: #f5f5f5;
}

/* Contenedor de controles (etiqueta, campo de texto y botón) */
#controls {
  margin-top: 1.5rem;
}

/* Etiqueta “Query” transformada en un chip como el de ChatGPT */
#controls label {
  background-color: #f7f7f8;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
  color: #5f6368;
  display: inline-block;
  margin-bottom: 0.5rem;
}

/* Campo de texto tipo “Ask anything” con bordes redondeados y fondo gris claro */
#controls textarea,
#controls input[type="text"] {
  background-color: #f7f7f8;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 1rem 1.5rem;
  width: 100%;
  font-size: 1rem;
  color: #202123;
  outline: none;
}

/* Botón “Run Workflow” en un tono gris claro con texto oscuro */
#controls button {
  background-color: #f5f5f5;
  color: #202123;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  margin-top: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
#controls button:hover {
  background-color: #e8e8e8;
}

/* Contenedores de Markdown (logs y resultados) con sombra suave */
.markdown {
  background-color: #ffffff;
  border: 1px solid #f0f0f0;
  border-radius: 16px;
  padding: 1rem;
  margin-top: 1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
"""
