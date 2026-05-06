"""
Lee el corpus para sesiones sin etiqueta y asigna clase según contenido.
Escribe de vuelta a ML/tf_idf_matrix_clases.csv.
"""
import os, sys, unicodedata
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

CORPUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus')

# ── Reglas por prioridad (mayor peso = más específico) ──────────────────────
# Palabras en mensajes_processed.txt ya están sin acentos, minúsculas
RULES = [
    # (clase, peso, keywords)
    ('Facturación_Documentos', 5, [
        'factura', 'facturar', 'facturacion', 'cfdi', 'xml timbrado',
        'nota credito', 'nota de credito', 'complemento pago', 'timbrado',
        'comprobante fiscal', 'remision', 'xml', 'facturacion electronica',
        'regimen fiscal', 'uso cfdi',
        # bigrams
        'comprobante pago', 'pago factura', 'mande factura', 'factura correo',
        'comparto comprobante', 'apoyar cuenta', 'apoyar complemento',
        'apoyas complemento', 'apoyas cuenta', 'apoyas siguiente',
        'apoyar siguiente', 'comparte factura', 'pase correo',
        'envio comprobante', 'factura vencida', 'envio cuenta',
        'comparto cuenta', 'factura respalda', 'facturas respalda',
        'podria reenviar', 'paso factura', 'pago programado',
        'llegan correo', 'llegaron correo', 'pago coincide',
        'credito suspendido', 'cuenta favor', 'saldo favor',
        'nueva factura', 'cancelacion sat', 'constancia fiscal',
        'metodo pago', 'factura pago', 'paso comprobante',
        'dos facturas', 'factura pendiente', 'facturas orden',
        'facturas favor', 'ayudar pago', 'pago papeleria',
        'hacer pago', 'pago transferencia', 'hacer factura',
        'voy facturar', 'puedo facturar', 'poder facturar',
        'puedes facturar', 'ahorita facturo', 'facturo aparte',
        'hago factura', 'sola factura', 'hago nota', 'hacer nota',
        'factura favor',
    ]),
    ('Cancelación', 5, [
        'cancelar pedido', 'cancelar el pedido', 'ya no lo quiero',
        'ya no necesito', 'cancelacion', 'anular', 'suspender pedido',
        'ya no quiero', 'no lo quiero', 'cancela',
    ]),
    ('Cotización/Presupuesto', 4, [
        'cotizacion', 'cotiza', 'cotizame', 'presupuesto', 'proforma',
        'propuesta economica', 'lista de precios', 'cuanto cuesta',
        'cuanto sale', 'cuanto me quedaria', 'elaborar cotizacion',
        'manda cotizacion', 'cotizaciones',
        # bigrams
        'cotizas favor', 'puedes cotizar', 'cotizar favor', 'cotiza favor',
        'podrias cotizar', 'mando cotizacion', 'mande cotizacion',
        'cotizacion favor', 'paso cotizacion', 'cotizacion correo',
        'cotizacion modificada', 'cotizacion personal', 'cotizacion orden',
        'envio cotizacion', 'cotizas nombre', 'cotizar material',
        'enviarle cotizacion', 'sale iva', 'precio favor', 'pasas precio',
    ]),
    ('Gestión de Pedidos/Entregas', 4, [
        'pedido', 'entreg', 'envio', 'enviar', 'surtir', 'surtido',
        'mensajero', 'paquete', 'recoger', 'recoleccion', 'embarque',
        'despacho', 'mercancia', 'llego el', 'recibir pedido',
        'cuando llega', 'cuando entregan', 'enviarme', 'mandame',
        'manda el', 'ya salio', 'en camino', 'en ruta',
        # bigrams
        'orden compra', 'mando pedido', 'mando traer', 'claro mando',
        'puedes enviar', 'puedes mandar', 'mando manana', 'envio manana',
        'pedido manana', 'llego pedido', 'recoger pedido', 'pedido pagina',
        'entregan manana', 'entrega manana', 'entregan pedidos',
        'envie pedido', 'enviar pedido', 'mandar pedido', 'mande pedido',
        'siguiente orden', 'hacer pedido', 'hacerle pedido',
        'hacerte pedido', 'hare pedido', 'agregar pedido',
        'puedes agregar', 'favor agregas', 'agrega favor', 'puedo enviar',
        'pueden traer', 'pueden mandar', 'surtir favor',
        'estarian entregando', 'deben llegar', 'enviar paquetes',
        'manana primera', 'primera hora', 'pedido mazatlan',
        'direccion entrega', 'rutas salieron', 'junto pedido',
        'pedido papeleria', 'compra anexa', 'envio orden', 'voy solicitar',
        'listo envie', 'listo envio', 'cuantos mando', 'mandar total',
        'revisando pedido',
    ]),
    ('Soporte', 4, [
        'problema con', 'queja', 'defecto', 'danado', 'roto',
        'en mal estado', 'no sirve', 'devolucion', 'garantia',
        'falla', 'incompleto', 'equivocado', 'error en', 'mal cobrado',
        # bigrams
        'hizo falta', 'hace falta',
    ]),
    ('Seguimiento de Ventas', 4, [
        'seguimiento', 'como van', 'hay novedad', 'como quedo',
        'algun avance', 'me puede decir si', 'quedamos en',
        'le recordamos', 'retomamos', 'continuacion', 'le hago recordar',
        # bigrams
        'checando necesitas', 'andas papeleria', 'pudo revisar',
        'tiempo checar', 'faltantes papeleria', 'alguna novedad',
        'pedido faltante', 'revisar faltantes', 'alguna necesidad',
        'necesidad papeleria', 'revisando surgido', 'revisando faltantes',
        'novedad faltantes', 'algun faltante', 'revisando pasaron',
        'pasaron faltantes', 'preguntar ocupando', 'preguntar andas',
        'ocupando papeleria', 'necesitas papeleria', 'necesitan papeleria',
        'ojala autoricen', 'comentaron cotizacion', 'cotizaciones papeleria',
        'cotizacion papeleria', 'revisando cotizacion', 'papeleria cotizar',
    ]),
    ('Consulta de Precio', 3, [
        'precio de', 'precio del', 'precios de', 'cuanto esta',
        'cuanto vale', 'tarifa', 'costo de', 'precio por',
        'me das precio', 'dame precio', 'precio unitario',
        # bigrams
        'cuanto sale', 'pedir precio', 'cuanto lleguen', 'cuanto respuesta',
        'claro cuanto', 'revisar precio', 'paso precio', 'precio paquete',
        'paquete precio', 'precio envio', 'tendra paquete', 'cuantas piezas',
        'cuanto pasen', 'cuantos necesita', 'cuantas necesitas',
    ]),
    ('Interacción/Relacional', 1, [
        'buen dia', 'buenos dias', 'buenas tardes', 'buenas noches',
        'hola', 'feliz', 'saludos', 'disculpe la molestia',
        # bigrams
        'solo saludar', 'espero encuentre', 'espero encuentres',
        'excelente semana', 'excelente senorita', 'disculpa tardanza',
        'regreso lunes', 'semana entra', 'tan amable', 'mil disculpas',
        'usted tal', 'perfecto senorita', 'quien gusto',
    ]),
    ('Confirmación_Estado', 1, [
        'ok', 'listo', 'confirmado', 'recibido', 'enterado',
        'de acuerdo', 'con gusto', 'perfecto', 'gracias', 'muchas gracias',
        'ya quedo', 'ya vi', 'ya cheque',
        # bigrams
        'deja checo', 'deja ver', 'deja veo', 'momento paso',
        'dame momento', 'hace rato', 'reviso confirmo', 'reviso aviso',
        'ahorita confirmo', 'ahorita paso', 'listo pase', 'debe quedar',
        'asi quedaria', 'entonces espero', 'deme momento',
    ]),
]


def read_processed(client, session):
    path = os.path.join(CORPUS_DIR, client, session, 'mensajes_processed.txt')
    if not os.path.exists(path):
        path = os.path.join(CORPUS_DIR, client, session, 'mensajes.txt')
    if not os.path.exists(path):
        return '', 0
    lines = []
    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # strip author prefix
            if ':' in line:
                line = line.split(':', 1)[1].strip()
            lines.append(line)
    return ' '.join(lines), len(lines)


def norm(s):
    return unicodedata.normalize('NFC', str(s))


def score_text(text):
    scores = {}
    for clase, peso, keywords in RULES:
        hits = sum(1 for kw in keywords if kw in text)
        if hits:
            scores[clase] = scores.get(clase, 0) + hits * peso
    return scores


def classify(text, msg_count):
    scores = score_text(text)
    if not scores:
        # Sin señales claras — conversación muy corta → Relacional, sino Confirmación
        if msg_count <= 3:
            return 'Interacción/Relacional', 'sin_señales_corta'
        return 'Confirmación_Estado', 'sin_señales'

    top = sorted(scores.items(), key=lambda x: -x[1])
    best_clase, best_score = top[0]

    # Relacional solo gana si está muy sola (pocas señales de negocio)
    if best_clase == 'Interacción/Relacional':
        biz_score = sum(s for c, s in top[1:] if c != 'Interacción/Relacional')
        if biz_score > 0:
            top2 = [t for t in top if t[0] != 'Interacción/Relacional']
            if top2:
                best_clase, best_score = top2[0]

    return best_clase, f'score={best_score}'


def main():
    clases_path = 'ML/tf_idf_matrix_clases.csv'
    df = pd.read_csv(clases_path, encoding='utf-8-sig')

    unlabeled_idx = df[df['Clase'].isna()].index
    print(f"Sesiones sin etiqueta: {len(unlabeled_idx)}")

    applied = {}
    no_corpus = []

    for idx in unlabeled_idx:
        chat = norm(df.at[idx, 'Chat'])
        parts = chat.split('/')
        if len(parts) < 2:
            no_corpus.append(chat)
            continue
        client  = parts[0]
        session = parts[1]

        text, msg_count = read_processed(client, session)
        if not text:
            no_corpus.append(chat)
            continue

        clase, reason = classify(text, msg_count)
        df.at[idx, 'Clase'] = clase
        applied[clase] = applied.get(clase, 0) + 1

    df.to_csv(clases_path, index=False, encoding='utf-8-sig')

    print("\nClases asignadas:")
    for k, v in sorted(applied.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    if no_corpus:
        print(f"\nSin corpus ({len(no_corpus)}): {no_corpus[:5]}")
    print(f"\nDistribución final:")
    print(df['Clase'].value_counts(dropna=False).to_string())


if __name__ == '__main__':
    main()
