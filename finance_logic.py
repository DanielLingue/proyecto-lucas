import re

def procesar_input_ia(texto):
    """
    Simula un procesamiento de lenguaje natural (NLP) para extraer intenciones y datos.
    ACCESIBILIDAD: Permite inputs desordenados (ej: "5 lucas en comida") para reducir
    la demanda de función ejecutiva. No obliga a formatos estrictos.
    """
    texto = texto.lower()
    
    # 1. Detección de Montos (Soporte para jerga chilena "Lucas")
    monto = 0
    # Regex para buscar números. Soporta "5000", "5.000", "5 lucas", "5k"
    match_lucas = re.search(r'(\d+)\s*lucas', texto)
    match_k = re.search(r'(\d+)k', texto)
    match_num = re.search(r'(\d+[\d.]*)', texto)

    if match_lucas:
        monto = int(match_lucas.group(1)) * 1000
    elif match_k:
        monto = int(match_k.group(1)) * 1000
    elif match_num:
        # Eliminar puntos si el usuario escribió "5.000"
        limpio = match_num.group(1).replace('.', '')
        monto = int(limpio)
    
    # Si no hay monto, puede ser una pregunta educativa
    if monto == 0:
        return {"tipo": "educativo", "contenido": texto}

    # 2. Clasificación de Categorías (Regla 50/30/20)
    # ACCESIBILIDAD: Clasificación automática para evitar fatiga de decisión.
    categoria = "Deseos" # Default seguro
    
    keywords_necesidades = ['super', 'luz', 'agua', 'arriendo', 'comida', 'farmacia', 'medico', 'internet']
    keywords_ahorro = ['fintual', 'deposito', 'dap', 'fondo', 'guardar', 'chanchito']
    
    if any(word in texto for word in keywords_necesidades):
        categoria = "Necesidades"
    elif any(word in texto for word in keywords_ahorro):
        categoria = "Ahorros"
    
    return {
        "tipo": "gasto",
        "monto": monto,
        "categoria": categoria,
        "descripcion": texto
    }

def obtener_respuesta_educativa(texto):
    """
    Simula un sistema RAG (Retrieval-Augmented Generation) con fuentes oficiales.
    ACCESIBILIDAD: Respuestas cortas, sin jerga técnica innecesaria y con fuentes confiables
    para reducir la ansiedad financiera generada por la desinformación.
    """
    texto = texto.lower()
    
    if "inversi" in texto or "plata" in texto:
        return (
            "💰 **Sobre Inversiones:**\n\n"
            "Para empezar sin riesgo, la **CMF (Comisión para el Mercado Financiero)** recomienda los Depósitos a Plazo (DAP). "
            "Son seguros y sabes exactamente cuánto ganarás. \n\n"
            "⚠️ *Lucas dice: Evita criptomonedas o 'trading' si estás empezando. Cuida tu esfuerzo.*"
        )
    elif "deuda" in texto or "crédito" in texto or "tarjeta" in texto:
        return (
            "💳 **Sobre Deudas:**\n\n"
            "El **SERNAC** recomienda que tu carga financiera mensual no supere el 25% de tu sueldo. "
            "Si estás pagando el mínimo de la tarjeta, intenta pagar un poco más para bajar los intereses (CAE). "
            "¿Necesitas armar un plan de pago?"
        )
    else:
        return "No estoy seguro de entender eso, pero estoy aquí para ayudarte a registrar gastos o responder dudas sobre ahorro y deudas básicas."