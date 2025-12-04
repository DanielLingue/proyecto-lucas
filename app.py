import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from finance_logic import procesar_input_ia, obtener_respuesta_educativa

# --- Configuración de Página ---
st.set_page_config(page_title="Lucas IA", page_icon="🤖", layout="wide")

# --- Estilos CSS para Accesibilidad ---
# Colores de alto contraste y fuentes legibles.
st.markdown("""
<style>
    .stChatInput {border-radius: 20px;}
    div[data-testid="stMetricValue"] {font-size: 2rem !important;}
    p {font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

# --- Inicialización de Estado (Memoria) ---
# ACCESIBILIDAD: Recordar el contexto ayuda a la memoria de trabajo (Working Memory).
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy Lucas 🤖. Cuéntame, ¿qué movimiento hiciste hoy? (Ej: 'Gasté 10 lucas en el super')"}
    ]
if "gastos" not in st.session_state:
    st.session_state.gastos = []
if "presupuesto" not in st.session_state:
    # Asumimos un sueldo base para el ejemplo, o se podría pedir al inicio.
    st.session_state.presupuesto = 800000 

# --- Sidebar: Resumen Global ---
with st.sidebar:
    st.header("📊 Tu Salud Financiera")
    st.markdown("La regla 50/30/20 simplificada.")
    
    # Calcular totales
    df = pd.DataFrame(st.session_state.gastos)
    if not df.empty:
        total_gastado = df['monto'].sum()
        por_categoria = df.groupby('categoria')['monto'].sum().to_dict()
    else:
        total_gastado = 0
        por_categoria = {"Necesidades": 0, "Deseos": 0, "Ahorros": 0}
    
    saldo = st.session_state.presupuesto - total_gastado
    
    # Métricas grandes y claras (Ideal para Discalculia)
    st.metric("Saldo Disponible", f"${saldo:,.0f}".replace(",", "."))
    st.metric("Total Gastado", f"${total_gastado:,.0f}".replace(",", "."))

    # Gráfico de Torta Accesible
    # Usamos colores distintivos pero amigables para el daltonismo
    labels = ["Necesidades (50%)", "Deseos (30%)", "Ahorros (20%)"]
    
    # Aseguramos que existan las llaves en el diccionario
    val_necesidades = por_categoria.get("Necesidades", 0)
    val_deseos = por_categoria.get("Deseos", 0)
    val_ahorros = por_categoria.get("Ahorros", 0)
    
    values = [val_necesidades, val_deseos, val_ahorros]
    
    # Colores: Azul (Calma), Naranja (Atención suave), Verde (Positivo)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', marker=dict(colors=colors))
    fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0), height=250)
    
    st.plotly_chart(fig, use_container_width=True)

# --- Área Principal: Chat ---
st.title("Lucas: Tu Asistente Financiero")

# Renderizar historial de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Procesamiento de Input ---
if prompt := st.chat_input("Escribe aquí (ej: 'Pizza 15000', 'Invertir en fondos')"):
    # 1. Mostrar mensaje usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Procesar con Lógica
    resultado = procesar_input_ia(prompt)
    
    respuesta_bot = ""
    
    if resultado["tipo"] == "gasto":
        # Guardar en estado
        nuevo_gasto = {
            "monto": resultado["monto"],
            "categoria": resultado["categoria"],
            "item": resultado["descripcion"]
        }
        st.session_state.gastos.append(nuevo_gasto)
        
        # Feedback Inmediato y Positivo
        # Usamos emojis para transmitir emoción y claridad visual
        monto_fmt = f"${resultado['monto']:,.0f}".replace(",", ".")
        emoji = "🏠" if resultado['categoria'] == 'Necesidades' else "🎉" if resultado['categoria'] == 'Deseos' else "piggy_bank"
        
        respuesta_bot = (
            f"Listo. Anoté **{monto_fmt}** en **{resultado['categoria']}** {emoji}.\n\n"
            f"*Tu saldo actual se actualizó en la barra lateral.*"
        )
        
    elif resultado["tipo"] == "educativo":
        respuesta_bot = obtener_respuesta_educativa(resultado["contenido"])

    # 3. Mostrar respuesta bot
    with st.chat_message("assistant"):
        st.markdown(respuesta_bot)
    st.session_state.messages.append({"role": "assistant", "content": respuesta_bot})
    
    # Forzar recarga para actualizar gráficos sidebar
    st.rerun()