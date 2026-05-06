"""
Correcciones v2 identificadas leyendo el corpus chat por chat.
Aplica sobre ML/tf_idf_matrix_clases.csv.
"""
import sys, unicodedata
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

def norm(s):
    return unicodedata.normalize('NFC', str(s))

CORRECTIONS = {
    # ── CONFIRMACIÓN_ESTADO → FACTURACIÓN_DOCUMENTOS ──────────────────────────
    "T1 Betzavel Laso Roman/04-03-2026": "Facturación_Documentos",   # opinion de favor = nota crédito
    "T1 Betzavel Laso Roman/22-01-2026": "Facturación_Documentos",   # cambio de domicilio fiscal
    "T1 Carmen Karful 45143/23-01-2026": "Facturación_Documentos",   # factura vence, pago programado
    "T1 Patricia 30049 Urrea ✨🍀🙏🏻/23-02-2026": "Facturación_Documentos",  # revisando pagos enero / hoy vence
    "T2  Oriana 46797 Taller Capule Oriana/23-03-2026": "Facturación_Documentos",  # pasame el pago a la cuenta
    "T2  Oriana 46797 Taller Capule Oriana/25-01-2025": "Facturación_Documentos",  # correo correcto para facturas
    "T2 44338_Chavez A_Victoria/09-01-2026": "Facturación_Documentos",  # facturitas pendientes / programadas?
    "T2 44338_Chavez A_Victoria/12-01-2026": "Facturación_Documentos",  # me mandas estado de cuenta
    "T2 44338_Chavez A_Victoria/19-06-2025": "Facturación_Documentos",  # PDF adjunto (folio)
    "T2 44338_Chavez A_Victoria/22-04-2026": "Facturación_Documentos",  # foto comprobante de pago
    "T2 44338_Chavez A_Victoria/25-04-2026": "Facturación_Documentos",  # ya te llego el complemento de pago
    "T2 44338_Chavez A_Victoria/29-01-2025": "Facturación_Documentos",  # PDF listo (folio)
    "T2 44338_Chavez A_Victoria/30-08-2025": "Facturación_Documentos",  # PDF facturas múltiples
    "T2 45101 Vision C_ Cleam/01-04-2026": "Facturación_Documentos",   # aun no tienes el comprobante
    "T2 45101 Vision C_ Cleam/03-01-2026": "Facturación_Documentos",   # facturación setup portal
    "T2 45101 Vision C_ Cleam/03-09-2025": "Facturación_Documentos",   # te pago / payment
    "T2 45101 Vision C_ Cleam/03-10-2025": "Facturación_Documentos",   # complementos de pago
    "T2 45101 Vision C_ Cleam/06-01-2026": "Facturación_Documentos",   # soy lupita me puedes (Vision patrón)
    "T2 45101 Vision C_ Cleam/07-04-2026": "Facturación_Documentos",   # me apoyas con estado de cuenta
    "T2 45101 Vision C_ Cleam/07-10-2025": "Facturación_Documentos",   # me puedes apoyar / te facturo?
    "T2 45101 Vision C_ Cleam/08-08-2025": "Facturación_Documentos",   # complemento pago
    "T2 45101 Vision C_ Cleam/09-03-2026": "Facturación_Documentos",   # pagos pendientes / factura enero
    "T2 45101 Vision C_ Cleam/09-08-2025": "Facturación_Documentos",   # aun no timbra, los pagos
    "T2 45101 Vision C_ Cleam/09-10-2025": "Facturación_Documentos",   # me apoyan con la solicitud
    "T2 45101 Vision C_ Cleam/10-07-2025": "Facturación_Documentos",   # asi te facturo
    "T2 45101 Vision C_ Cleam/10-11-2025": "Facturación_Documentos",   # me puedes compartir (facturas)
    "T2 45101 Vision C_ Cleam/11-02-2026": "Facturación_Documentos",   # soy lupita me apoyas
    "T2 45101 Vision C_ Cleam/11-08-2025": "Facturación_Documentos",   # adjunto complemento de pago
    "T2 45101 Vision C_ Cleam/12-03-2026": "Facturación_Documentos",   # soy lupita me puedes
    "T2 45101 Vision C_ Cleam/16-08-2025": "Facturación_Documentos",   # facturas vencidas discussion
    "T2 45101 Vision C_ Cleam/18-08-2025": "Facturación_Documentos",   # en cuando tenga el comprobante
    "T2 45101 Vision C_ Cleam/18-11-2025": "Facturación_Documentos",   # soy lupita me pue (documentos)
    "T2 45101 Vision C_ Cleam/19-12-2025": "Facturación_Documentos",   # claro que si te lo mando
    "T2 45101 Vision C_ Cleam/21-10-2025": "Facturación_Documentos",   # facturitas vencidas / pasamos a pago
    "T2 45101 Vision C_ Cleam/26-01-2026": "Facturación_Documentos",   # soy lupita me puedes
    "T2 45101 Vision C_ Cleam/26-02-2026": "Facturación_Documentos",   # soy lupita me puedes
    "T2 45101 Vision C_ Cleam/26-12-2025": "Facturación_Documentos",   # claro que si en cuanto quede (pago)
    "T2 45101 Vision C_ Cleam/28-11-2025": "Facturación_Documentos",   # te paso estado de cuenta
    "T2 45101 Vision C_ Cleam/29-01-2026": "Facturación_Documentos",   # confirmas si esta bien (factura)
    "T2 45101 Vision C_ Cleam/29-09-2025": "Facturación_Documentos",   # por favor nos podrías (documentos)
    "T2 45101 Vision C_ Cleam/30-08-2025": "Facturación_Documentos",   # en cuanto se apliquen los pagos
    "T2 45101 Vision C_ Cleam/31-03-2026": "Facturación_Documentos",   # por favor nos podrías
    "T2 Daniela 46752/02-03-2026": "Facturación_Documentos",           # apoyar reenviar de este pago
    "T2 Daniela 46752/04-07-2025": "Facturación_Documentos",           # me podrías compartir los datos
    "T2 Daniela 46752/13-02-2026": "Facturación_Documentos",           # adjunto pago
    "T2 Daniela 46752/14-01-2026": "Facturación_Documentos",           # me equivoqué en la póliza
    "T2 Daniela 46752/16-07-2025": "Facturación_Documentos",           # te facturo a si
    "T2 Jaime 47559/17-06-2024": "Facturación_Documentos",             # razón social nueva / mándamela
    "T2 Jaime 47559/26-03-2026": "Facturación_Documentos",             # nos hicieron el pago / de qué banco
    "T5 Castilla Shaula/27-01-2026": "Facturación_Documentos",         # crédito suspendido / pago
    "T5 Elizabeth Productora De Alimentos/19-03-2026": "Facturación_Documentos",  # comprobante adjunto
    "T5 Elizabeth Productora De Alimentos/23-04-2026": "Facturación_Documentos",  # pago fue sola / muchas gracias
    "T6 Sistemas de Impresion Elect. Compras/11-04-2026": "Facturación_Documentos",  # DOC enviado / listo
    "T9 Huma Uniformes Y Bordados 41403/13-04-2026": "Facturación_Documentos",    # gracias por el pago
    "T9 Huma Uniformes Y Bordados 41403/17-03-2026": "Facturación_Documentos",    # gracias por el pago
    "T9 Sergio M paper plus 10592/10-02-2026": "Facturación_Documentos",          # ya autorizaron / ya quedo el pago
    "t6 Patty (40056) 777 MSI DIAMANTE 2/04-03-2026": "Facturación_Documentos",   # comprobante de pago
    "t6 Patty (40056) 777 MSI DIAMANTE 2/06-02-2026": "Facturación_Documentos",   # le comparto estado de cuenta
    "t6 Patty (40056) 777 MSI DIAMANTE 2/10-02-2026": "Facturación_Documentos",   # saldo pendiente / pago
    "t6 Patty (40056) 777 MSI DIAMANTE 2/15-04-2026": "Facturación_Documentos",   # ya le pase los archivos
    "t6 Patty (40056) 777 MSI DIAMANTE 2/21-04-2026": "Facturación_Documentos",   # te mande estado de cuenta / me pagaron

    # ── CONFIRMACIÓN_ESTADO → GESTIÓN DE PEDIDOS/ENTREGAS ─────────────────────
    "T1 Carmen Karful 45143/19-03-2026": "Gestión de Pedidos/Entregas",  # si me lo dejaron (delivery)
    "T1 Dulce 45871/21-03-2026": "Gestión de Pedidos/Entregas",          # 2 opalalina gruesa
    "T1 Dulce 45871/31-01-2026": "Gestión de Pedidos/Entregas",          # sobres plástico / oficio
    "T2 44338_Chavez A_Victoria/20-03-2025": "Gestión de Pedidos/Entregas",  # te paso la lista / serian:
    "T2 45101 Vision C_ Cleam/15-08-2025": "Gestión de Pedidos/Entregas",    # ocupo 10 piezas
    "T2 45101 Vision C_ Cleam/17-05-2025": "Gestión de Pedidos/Entregas",    # ibamos a pedir 10
    "T2 45101 Vision C_ Cleam/23-01-2026": "Gestión de Pedidos/Entregas",    # pasariamos por ellas
    "T2 45101 Vision C_ Cleam/27-11-2025": "Gestión de Pedidos/Entregas",    # cual de estos te pongo (order)
    "T2 45101 Vision C_ Cleam/28-07-2025": "Gestión de Pedidos/Entregas",    # te envio la orden
    "T2 Daniela 46752/07-10-2024": "Gestión de Pedidos/Entregas",            # 200 sobres / tinta / cartón hojas
    "T2 Jaime 47559/19-12-2024": "Gestión de Pedidos/Entregas",              # ya tengo casi todo, con remision
    "T2 Lesli 47721/10-04-2026": "Gestión de Pedidos/Entregas",              # ¿Tendrás este toner? / me mandas 3
    "T5 Castilla Shaula/17-03-2026": "Gestión de Pedidos/Entregas",          # le encargo el cartón (35 msgs)
    "T5 Elizabeth Productora De Alimentos/24-02-2026": "Gestión de Pedidos/Entregas",  # solo me faltan las tablas
    "T5 Oriana Tribunal Agrario/20-01-2026": "Gestión de Pedidos/Entregas",  # cuando vendrán
    "T5 Raul Vama/09-03-2026": "Gestión de Pedidos/Entregas",               # ocupo plumones / mandas a Cedis
    "T5 Raul Vama/12-02-2026": "Gestión de Pedidos/Entregas",               # me puede mandar eso
    "T5 Raul Vama/13-04-2026": "Gestión de Pedidos/Entregas",               # 2 [productos] por favor
    "T5 Raul Vama/19-01-2026": "Gestión de Pedidos/Entregas",               # ya te mande el correo (pedido)
    "T6 Cleotilde Kimivac Olivas/12-02-2026": "Gestión de Pedidos/Entregas",  # de reparto que entregará
    "T6 Michelle GPS (45574)/24-04-2026": "Gestión de Pedidos/Entregas",     # te va llegar el papel
    "t6 Patty (40056) 777 MSI DIAMANTE 2/07-03-2026": "Gestión de Pedidos/Entregas",  # le envio su pedido el lunes
    "t6 Patty (40056) 777 MSI DIAMANTE 2/11-03-2026": "Gestión de Pedidos/Entregas",  # es para Humaya (dirección entrega)
    "T9 Huma Uniformes Y Bordados 41403/12-03-2026": "Gestión de Pedidos/Entregas",   # me mandas lo [que pedí]
    "T9 Sergio M paper plus 10592/06-02-2026": "Gestión de Pedidos/Entregas",         # foamy se los puedo conseguir / surta el pedido

    # ── CONFIRMACIÓN_ESTADO → SEGUIMIENTO DE VENTAS ───────────────────────────
    "T2  Oriana 46797 Taller Capule Oriana/03-12-2025": "Seguimiento de Ventas",  # registrarse en portal nuevo
    "T2  Oriana 46797 Taller Capule Oriana/13-08-2024": "Seguimiento de Ventas",  # checando si estas necesitando toner
    "T2  Oriana 46797 Taller Capule Oriana/17-05-2024": "Seguimiento de Ventas",  # como andas de papeleria
    "T2  Oriana 46797 Taller Capule Oriana/17-09-2024": "Seguimiento de Ventas",  # como andamos de papeleria
    "T2  Oriana 46797 Taller Capule Oriana/18-11-2025": "Seguimiento de Ventas",  # Aun no (respondiendo check-in)
    "T2  Oriana 46797 Taller Capule Oriana/21-01-2026": "Seguimiento de Ventas",  # ahorita po / quedo al pendiente
    "T2 44338_Chavez A_Victoria/07-02-2025": "Seguimiento de Ventas",  # quedo autorizada la cotización
    "T2 44338_Chavez A_Victoria/10-03-2025": "Seguimiento de Ventas",  # como andas de papeleria
    "T2 44338_Chavez A_Victoria/27-01-2025": "Seguimiento de Ventas",  # tienen programado algo
    "T2 45101 Vision C_ Cleam/01-12-2025": "Seguimiento de Ventas",   # nos autorizaron (algo)
    "T2 45101 Vision C_ Cleam/05-08-2025": "Seguimiento de Ventas",   # paso a preguntar si estas ocupando
    "T2 45101 Vision C_ Cleam/11-06-2025": "Seguimiento de Ventas",   # tendrás algo / deja checo
    "T2 45101 Vision C_ Cleam/24-11-2025": "Seguimiento de Ventas",   # tendria que hacerle el comentario
    "T2 45101 Vision C_ Cleam/28-04-2025": "Seguimiento de Ventas",   # paso a preguntar si estas ocupando
    "T2 Daniela 46752/12-04-2025": "Seguimiento de Ventas",           # estaras necesitando algo? tinta papeleria
    "T2 Daniela 46752/21-10-2024": "Seguimiento de Ventas",           # como andamos de papeleria, tinta
    "T2 Jaime 47559/05-08-2025": "Seguimiento de Ventas",             # ya estaras ocupando toner?
    "T2 Jaime 47559/11-10-2024": "Seguimiento de Ventas",             # quieres que te mande los toner
    "T2 Jaime 47559/21-05-2025": "Seguimiento de Ventas",             # solo tengo uno en existencia
    "T2 Jaime 47559/22-10-2025": "Seguimiento de Ventas",             # espero tu llamada
    "T4 Electrica Aselco 19649/06-04-2026": "Seguimiento de Ventas",  # digame lo que necesita
    "T9 Sergio M paper plus 10592/24-02-2026": "Seguimiento de Ventas",  # no les interesa para su papelería
    "T9 Sergio M paper plus 10592/24-03-2026": "Seguimiento de Ventas",  # quedo en espera
    "t6 CASSANDRA ADMINISTRACION CHINIZA/16-04-2026": "Seguimiento de Ventas",  # revisar si tiene faltantes
    "T6 Cleotilde Kimivac Olivas/09-03-2026": "Seguimiento de Ventas",           # revisar si requiere algo
    "T6 Michelle GPS (45574)/15-04-2026": "Seguimiento de Ventas",               # ya no me comentó (follow up)

    # ── CONFIRMACIÓN_ESTADO → INTERACCIÓN/RELACIONAL ──────────────────────────
    "T2  Oriana 46797 Taller Capule Oriana/21-08-2025": "Interacción/Relacional",  # social: bien y usted?
    "T2  Oriana 46797 Taller Capule Oriana/22-02-2024": "Interacción/Relacional",  # ok muchas gracias (2 msgs)
    "T2  Oriana 46797 Taller Capule Oriana/24-04-2026": "Interacción/Relacional",  # muchas gracias emojis
    "T2  Oriana 46797 Taller Capule Oriana/29-09-2025": "Interacción/Relacional",  # hola + muchas gracias
    "T2  Oriana 46797 Taller Capule Oriana/30-01-2024": "Interacción/Relacional",  # ok muchas gracias / de nada
    "T2 44338_Chavez A_Victoria/05-12-2025": "Interacción/Relacional",  # hola bien y tu?
    "T2 44338_Chavez A_Victoria/20-10-2025": "Interacción/Relacional",  # como estas / buen GAD
    "T2 44338_Chavez A_Victoria/21-04-2025": "Interacción/Relacional",  # como te encuentras / buen GAD
    "T2 44338_Chavez A_Victoria/27-02-2026": "Interacción/Relacional",  # como estas / Bien GAD
    "T2 45101 Vision C_ Cleam/06-11-2025": "Interacción/Relacional",   # muy bien / gracias
    "T2 45101 Vision C_ Cleam/07-01-2026": "Interacción/Relacional",   # muchas gracias / excelente dia
    "T2 45101 Vision C_ Cleam/09-09-2025": "Interacción/Relacional",   # muchas gracias (1-3 msgs)
    "T2 45101 Vision C_ Cleam/14-02-2026": "Interacción/Relacional",   # feliz dia del amor
    "T2 45101 Vision C_ Cleam/19-09-2025": "Interacción/Relacional",   # muchas gracias
    "T2 45101 Vision C_ Cleam/20-01-2026": "Interacción/Relacional",   # muchas gracias (4 msgs)
    "T2 45101 Vision C_ Cleam/20-08-2025": "Interacción/Relacional",   # buen día / con gusto (3 msgs)
    "T2 45101 Vision C_ Cleam/21-07-2025": "Interacción/Relacional",   # muchas gracias (6 msgs social)
    "T2 45101 Vision C_ Cleam/22-07-2025": "Interacción/Relacional",   # muchas gracias (4 msgs)
    "T2 Daniela 46752/02-10-2024": "Interacción/Relacional",           # andaba de vacaciones
    "T2 Daniela 46752/28-10-2025": "Interacción/Relacional",           # hola + muchas gracias (3 msgs)
    "T2 Jaime 47559/05-11-2025": "Interacción/Relacional",             # como estas / me da gusto
    "T2 Jaime 47559/15-07-2025": "Interacción/Relacional",             # como estas / bien gracias
    "T2 Jaime 47559/17-09-2024": "Interacción/Relacional",             # como estas / ya laborando
    "T2 Jaime 47559/21-10-2025": "Interacción/Relacional",             # hola bien gracias (2 msgs)
    "T2 Jaime 47559/23-01-2026": "Interacción/Relacional",             # ando de vacaciones
    "T2 Jaime 47559/27-08-2024": "Interacción/Relacional",             # como estas / con mucho trabajo
    "T4  Carnes selec compras 19256 Sel/29-01-2026": "Interacción/Relacional",  # buenos dias gracias
    "T4 Jesús Meléndez 31713/14-04-2026": "Interacción/Relacional",    # buenos dias graciasss (2 msgs)
    "T4 Mirna Jose A.Mora/21-03-2026": "Interacción/Relacional",       # Hoy trabajan?
    "T5 Castilla Shaula/04-02-2026": "Interacción/Relacional",         # ya me quitaron el yeso / y ud?
    "T5 Castilla Shaula/07-04-2026": "Interacción/Relacional",         # bien gracias a dios y tu?
    "T5 Raul Vama/06-03-2026": "Interacción/Relacional",               # muchas gracias (2 msgs)
    "T6 Sistemas de Impresion Elect. Compras/09-02-2026": "Interacción/Relacional",  # buenos dias / gracias (3 msgs)
    "T6 Sistemas de Impresion Elect. Compras/14-04-2026": "Interacción/Relacional",  # de momento no te / buenos dias
    "T9 Ferre laminas 46266/25-03-2026": "Interacción/Relacional",     # muy amable gracias (2 msgs)
    "T9 Huma Uniformes Y Bordados 41403/14-03-2026": "Interacción/Relacional",  # gracias por t[u atención]
    "T9 Miriam Fienmont 45737 Miriam/11-04-2026": "Interacción/Relacional",     # le encargo gracias (1 msg)

    # ── CONFIRMACIÓN_ESTADO → CONSULTA DE PRECIO ──────────────────────────────
    "T1 Carmen Karful 45143/06-03-2026": "Consulta de Precio",   # Es igual a ese? + foto producto
    "T1 Carmen Karful 45143/23-03-2026": "Consulta de Precio",   # vendes de estos? + foto
    "T1 Carmen Karful 45143/24-02-2026": "Consulta de Precio",   # Vendes correas para?
    "T1 Dulce 45871/25-04-2026": "Consulta de Precio",           # Tienes pasta?
    "T2 44338_Chavez A_Victoria/26-08-2025": "Consulta de Precio",  # tienes grapas de
    "T2 45101 Vision C_ Cleam/08-07-2025": "Consulta de Precio",   # precio $68.70 navaja
    "T2 45101 Vision C_ Cleam/13-06-2025": "Consulta de Precio",   # deja reviso si tenemos en ese color
    "T2 45101 Vision C_ Cleam/16-05-2025": "Consulta de Precio",   # que colores maneja
    "T2 45101 Vision C_ Cleam/25-03-2026": "Consulta de Precio",   # es de 3 orificios la perforadora
    "T4  Carnes selec compras 19256 Sel/23-04-2026": "Consulta de Precio",  # tiene también?
    "T5 Raul Vama/10-03-2026": "Consulta de Precio",              # las vendes sueltas?
    "T5 Raul Vama/11-04-2026": "Consulta de Precio",              # Si tienes? / De stock no
    "T5 Raul Vama/17-03-2026": "Consulta de Precio",              # Tienes de estos? + fotos
    "t6 CASSANDRA ADMINISTRACION CHINIZA/11-02-2026": "Consulta de Precio",  # manejas etiquetas adhesivas
    "T6 Sistemas de Impresion Elect. Compras/03-02-2026": "Consulta de Precio",  # Manejan X?
    "T6 Sistemas de Impresion Elect. Compras/03-03-2026": "Consulta de Precio",  # son broches para gafet?
    "T6 Sistemas de Impresion Elect. Compras/04-02-2026": "Cotización/Presupuesto",  # si lo manejo / nuevo cliente
    "T6 Sistemas de Impresion Elect. Compras/05-02-2026": "Consulta de Precio",  # organizador 10 niveles
    "T6 Sistemas de Impresion Elect. Compras/07-04-2026": "Consulta de Precio",  # en tamaño oficio no tengo
    "T6 Sistemas de Impresion Elect. Compras/22-04-2026": "Consulta de Precio",  # manejan X?
    "T6 Sistemas de Impresion Elect. Compras/23-02-2026": "Consulta de Precio",  # tiene hojas?
    "T6 Sistemas de Impresion Elect. Compras/23-03-2026": "Consulta de Precio",  # esa marca no / papel fotográfico
    "T9 Drenax 42513/11-02-2026": "Gestión de Pedidos/Entregas",     # tendras de esto? / precio / me envias 2
    "T9 Huma Uniformes Y Bordados 41403/05-02-2026": "Consulta de Precio",  # es epson 544 (modelo toner)
    "T9 Sergio M paper plus 10592/16-04-2026": "Cotización/Presupuesto",    # pastas encuadernar / las de plástico?
    "T9 Sergio M paper plus 10592/28-01-2026": "Consulta de Precio",        # Tendrá? / de momento no lo tenemos

    # ── INTERACCIÓN/RELACIONAL → SEGUIMIENTO DE VENTAS ────────────────────────
    "T1 Dulce 45871/20-03-2026": "Seguimiento de Ventas",           # revisando si estas necesitando
    "T1 Patricia 30049 Urrea ✨🍀🙏🏻/10-04-2026": "Seguimiento de Ventas",  # esta pendiente un (seguimiento)
    "T2  Oriana 46797 Taller Capule Oriana/02-10-2024": "Seguimiento de Ventas",  # Checando (response to check-in)
    "T2  Oriana 46797 Taller Capule Oriana/02-12-2025": "Seguimiento de Ventas",  # ya te comente de la pagina nueva
    "T2  Oriana 46797 Taller Capule Oriana/03-10-2024": "Seguimiento de Ventas",  # como andas de toner papeleria
    "T2  Oriana 46797 Taller Capule Oriana/08-05-2025": "Seguimiento de Ventas",  # nose si ya estes necesitando
    "T2  Oriana 46797 Taller Capule Oriana/10-02-2025": "Seguimiento de Ventas",  # como andas de papeleria toners
    "T2  Oriana 46797 Taller Capule Oriana/12-05-2025": "Seguimiento de Ventas",  # quedo al pendiente
    "T2  Oriana 46797 Taller Capule Oriana/15-11-2025": "Seguimiento de Ventas",  # checando si necesitas toner
    "T2  Oriana 46797 Taller Capule Oriana/20-01-2026": "Seguimiento de Ventas",  # checando si necesitas toner/hojas
    "T2  Oriana 46797 Taller Capule Oriana/21-06-2025": "Seguimiento de Ventas",  # ocupas que te mande algo?
    "T2  Oriana 46797 Taller Capule Oriana/29-07-2024": "Seguimiento de Ventas",  # checando si necesitas toner
    "T2  Oriana 46797 Taller Capule Oriana/30-11-2024": "Seguimiento de Ventas",  # como andamos de papeleria tinta
    "T2 44338_Chavez A_Victoria/10-01-2025": "Seguimiento de Ventas",  # todo bien con la papelería
    "T2 44338_Chavez A_Victoria/12-08-2025": "Seguimiento de Ventas",  # tienes algo para mi, de papeleria?
    "T2 44338_Chavez A_Victoria/13-05-2025": "Seguimiento de Ventas",  # checando si tienes algún requerimiento
    "T2 44338_Chavez A_Victoria/17-07-2025": "Seguimiento de Ventas",  # checando si necesitas algo?
    "T2 44338_Chavez A_Victoria/19-02-2025": "Seguimiento de Ventas",  # paso a preguntarte si estas ocupando
    "T2 44338_Chavez A_Victoria/19-03-2025": "Seguimiento de Ventas",  # ya tienes algo para mi
    "T2 44338_Chavez A_Victoria/22-01-2025": "Seguimiento de Ventas",  # paso a preguntar si tienes faltantes
    "T2 44338_Chavez A_Victoria/31-07-2025": "Seguimiento de Ventas",  # paso a preguntar si tienes faltantes
    "T2 45101 Vision C_ Cleam/01-11-2025": "Seguimiento de Ventas",   # checando si tienen papeleria / toner
    "T2 45101 Vision C_ Cleam/05-09-2025": "Seguimiento de Ventas",   # me quede esperando / laura apoyando
    "T2 45101 Vision C_ Cleam/22-08-2025": "Seguimiento de Ventas",   # que me dices de la cotización / aún no
    "T2 Daniela 46752/18-02-2025": "Seguimiento de Ventas",           # como andas de papeleria tintas
    "T2 Daniela 46752/19-06-2025": "Seguimiento de Ventas",           # ocupas algo
    "T2 Daniela 46752/21-11-2024": "Seguimiento de Ventas",           # algo que necesites de papeleria
    "T2 Daniela 46752/23-12-2024": "Seguimiento de Ventas",           # como anda de papeleria, tintas
    "T2 Daniela 46752/27-05-2025": "Seguimiento de Ventas",           # ocupas que te mande algo (papeleria)
    "T2 Daniela 46752/27-09-2024": "Seguimiento de Ventas",           # ya estaras ocupando papeleria
    "T2 Daniela 46752/27-11-2025": "Seguimiento de Ventas",           # daniela tenemos una pagina web
    "T2 Daniela 46752/28-07-2025": "Seguimiento de Ventas",           # paso a preguntar si estas ocupando
    "T2 Jaime 47559/02-09-2025": "Seguimiento de Ventas",             # que te comentan de los toner?
    "T2 Jaime 47559/08-04-2025": "Seguimiento de Ventas",             # como andas de toner / ya estaras ocupando
    "T2 Jaime 47559/08-08-2024": "Seguimiento de Ventas",             # checando si ya estas necesitando toner
    "T2 Jaime 47559/29-05-2025": "Seguimiento de Ventas",             # no me pasaste el dato (follow up)
    "T2 Lesli 47721/30-12-2025": "Seguimiento de Ventas",             # todavía no tengo respuesta / volver a preguntar
    "T4 Katia Agrícola Vida Vida Hogar 47387/23-02-2026": "Seguimiento de Ventas",  # revisando si necesitan algo
    "T9 Sergio M paper plus 10592/20-01-2026": "Seguimiento de Ventas",  # que le comentaron / deje revisar

    # ── INTERACCIÓN/RELACIONAL → FACTURACIÓN_DOCUMENTOS ──────────────────────
    "T2 45101 Vision C_ Cleam/14-04-2026": "Facturación_Documentos",  # me apoyas con (Vision Facturación patrón)

    # ── INTERACCIÓN/RELACIONAL → GESTIÓN DE PEDIDOS/ENTREGAS ─────────────────
    "T1 Dulce 45871/18-02-2026": "Gestión de Pedidos/Entregas",   # me manda [algo] (order request)
    "T2 45101 Vision C_ Cleam/13-08-2025": "Gestión de Pedidos/Entregas",  # tienes en existencia / si tengo
    "T5 Elizabeth Productora De Alimentos/24-02-2026": "Gestión de Pedidos/Entregas",  # solo me faltan las tablas

    # ── INTERACCIÓN/RELACIONAL → CONSULTA DE PRECIO ───────────────────────────
    "T2 45101 Vision C_ Cleam/07-07-2025": "Consulta de Precio",   # de casualidad tienes X
    "T2 45101 Vision C_ Cleam/08-04-2026": "Consulta de Precio",   # que tipo de pluma manejas
    "T4 Copycos 16807/22-01-2026": "Consulta de Precio",           # tienes hoja carta xerox / cuanto sale
    "T6 Sistemas de Impresion Elect. Compras/16-02-2026": "Consulta de Precio",  # si / en cuánto tienes
    "T6 Sistemas de Impresion Elect. Compras/18-02-2026": "Consulta de Precio",  # no lo manejamos (product query)
    "T6 Sistemas de Impresion Elect. Compras/20-02-2026": "Consulta de Precio",  # tengo marca mae / $195 IVA
    "T6 Sistemas de Impresion Elect. Compras/20-04-2026": "Consulta de Precio",  # no cuenta con engargoladoras
    "T6 Sistemas de Impresion Elect. Compras/24-02-2026": "Consulta de Precio",  # no la tengo
    "T6 Sistemas de Impresion Elect. Compras/27-01-2026": "Consulta de Precio",  # el folder de esa marca no
    "T6 Sistemas de Impresion Elect. Compras/28-01-2026": "Consulta de Precio",  # solo la de color negra / tendra
    "T9 Huma Uniformes Y Bordados 41403/09-02-2026": "Consulta de Precio",  # cuanto cuesta / no tenemos dicc.
    "T9 Sergio M paper plus 10592/17-03-2026": "Consulta de Precio",        # tengo solo suelto / colores
    "t6 CASSANDRA ADMINISTRACION CHINIZA/27-02-2026": "Consulta de Precio", # que precio cinta / $64.70

    # ── INTERACCIÓN/RELACIONAL → SOPORTE ──────────────────────────────────────
    "T2 45101 Vision C_ Cleam/16-01-2026": "Soporte",  # te equivocaste de orden / una disculpa

    # ── INTERACCIÓN/RELACIONAL → COTIZACIÓN/PRESUPUESTO ──────────────────────
    "T9 Sergio M paper plus 10592/22-01-2026": "Cotización/Presupuesto",  # ya llegaron recopiladores / cuanto seria?

    # ── COTIZACIÓN/PRESUPUESTO → SEGUIMIENTO DE VENTAS ────────────────────────
    "T2 44338_Chavez A_Victoria/03-09-2025": "Seguimiento de Ventas",  # que te comentaron de la cotización
    "T2 Jaime 47559/14-04-2025": "Seguimiento de Ventas",              # ya checaste la cotización?
    "T2 Jaime 47559/16-12-2024": "Seguimiento de Ventas",              # checaste la cotización
    "T5 Oriana Tribunal Agrario/16-04-2026": "Seguimiento de Ventas",  # revisando si tiene pedidos
    "T9 Sergio M paper plus 10592/20-03-2026": "Seguimiento de Ventas", # que a pasado con las cotizaciones

    # ── COTIZACIÓN/PRESUPUESTO → FACTURACIÓN_DOCUMENTOS ──────────────────────
    "T2 45101 Vision C_ Cleam/14-01-2026": "Facturación_Documentos",  # soy lupita me puedes apoyar (Vision patrón)

    # ── GESTIÓN → FACTURACIÓN_DOCUMENTOS ──────────────────────────────────────
    "T2 44338_Chavez A_Victoria/25-04-2026": "Facturación_Documentos",  # ya te llego el complemento de pago

    # ── GESTIÓN → COTIZACIÓN/PRESUPUESTO ──────────────────────────────────────
    "T9 Sergio M paper plus 10592/20-04-2026": "Cotización/Presupuesto",  # le cotizo la b-400 / también tengo MAE

    # ── GESTIÓN → CONSULTA DE PRECIO ──────────────────────────────────────────
    "T6 Sistemas de Impresion Elect. Compras/25-02-2026": "Consulta de Precio",  # tengo de 21 a 35 hojas en existencia
    "T6 Michelle GPS (45574)/14-04-2026": "Consulta de Precio",                  # tendras sobres que no tengan
}

CORRECTIONS_NORM = {norm(k): v for k, v in CORRECTIONS.items()}

def main():
    clases_path = 'ML/tf_idf_matrix_clases.csv'
    df = pd.read_csv(clases_path, encoding='utf-8-sig')
    df['Chat'] = df['Chat'].apply(norm)

    applied = 0
    not_found = []
    for chat_key, new_clase in CORRECTIONS_NORM.items():
        mask = df['Chat'] == chat_key
        if mask.sum() == 0:
            not_found.append(chat_key)
            continue
        old = df.loc[mask, 'Clase'].iloc[0]
        if old != new_clase:
            df.loc[mask, 'Clase'] = new_clase
            applied += 1

    df.to_csv(clases_path, index=False, encoding='utf-8-sig')
    print(f"Correcciones aplicadas: {applied}")
    if not_found:
        print(f"No encontrados ({len(not_found)}):")
        for c in not_found:
            print(f"  {c}")
    print("\nDistribución final:")
    print(df['Clase'].value_counts(dropna=False).to_string())

if __name__ == '__main__':
    main()
