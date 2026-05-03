// Mock data for Comercios Unidos Insights
window.MOCK = (function() {
  const clients = [
    { id: "T5_castilla", name: "Castilla S.L.", office: "T5", segment: "recurrente", category: "Papelería", contact: "Castilla Shaula", phone: "+52 555 0102 8413", since: "2022-03-14", recompra: "21 días", ltv: 142800, conversations: 24 },
    { id: "T1_carmen", name: "Carmen Karful", office: "T1", segment: "recurrente", category: "Consumibles", contact: "Carmen Karful", phone: "+52 555 4513 7811", since: "2023-08-02", recompra: "14 días", ltv: 87200, conversations: 31 },
    { id: "T2_daniela", name: "Daniela 4675", office: "T2", segment: "recurrente", category: "Papelería", contact: "Daniela Mora", phone: "+52 555 4675 0021", since: "2023-01-22", recompra: "30 días", ltv: 64500, conversations: 18 },
    { id: "T4_cuprum", name: "Cuprum Construcción", office: "T4", segment: "consultivo", category: "Mobiliario", contact: "Ana Cuprum", phone: "+52 555 4453 1100", since: "2024-11-04", recompra: "—", ltv: 218400, conversations: 9 },
    { id: "T6_sistemas", name: "Sistemas de Impresión", office: "T6", segment: "recurrente", category: "Equipos", contact: "Jorge S.", phone: "+52 555 8821 4502", since: "2021-06-19", recompra: "45 días", ltv: 312000, conversations: 14 },
    { id: "T4_copycos", name: "Copycos Imp.", office: "T4", segment: "nuevo", category: "Consumibles", contact: "Mario L.", phone: "+52 555 1668 7740", since: "2025-09-11", recompra: "—", ltv: 12300, conversations: 4 },
    { id: "T4_katia", name: "Katia Agrícola Vida", office: "T4", segment: "recurrente", category: "Limpieza", contact: "Katia A.", phone: "+52 555 7387 0214", since: "2023-04-09", recompra: "60 días", ltv: 98600, conversations: 12 },
    { id: "T5_visi", name: "Vision C. Cleam", office: "T5", segment: "consultivo", category: "Mobiliario", contact: "Lucía V.", phone: "+52 555 4510 1009", since: "2024-02-15", recompra: "—", ltv: 184500, conversations: 7 },
  ];

  const conversations = [
    {
      id: "c1", clientId: "T5_castilla", clientName: "Castilla S.L.",
      session: "T5 Castilla", office: "T5", category: "Papelería", seller: "M. Hernández",
      date: "2026-04-14", lastMsg: "14:32",
      productMentions: ["pago", "factura", "cuenta"],
      objections: ["pago pendiente", "fiscal"],
      avgValence: -0.41, msgCount: 8,
      messages: [
        { t: "13:58", author: "Castilla Shaula", role: "client", text: "buenas tardes, necesito ver lo del pedido de papelería de la semana pasada", valence: -0.05, emotion: "others" },
        { t: "14:02", author: "M. Hernández", role: "seller", text: "buenas tardes Sra. Castilla, claro, ¿qué necesita revisar?", valence: 0.12, emotion: "joy" },
        { t: "14:05", author: "Castilla Shaula", role: "client", text: "desde la semana pasada debió quedar el pago, pero hubo unos líos con la cuenta no se que show por eso no han pagado", valence: -0.7555, emotion: "anger" },
        { t: "14:09", author: "M. Hernández", role: "seller", text: "entiendo, ¿podríamos extenderlo unos días mientras se resuelve?", valence: 0.08, emotion: "others" },
        { t: "14:14", author: "Castilla Shaula", role: "client", text: "por que cuando uno no me pasan el pedido de las áreas me lo envían el de cada mes", valence: -0.4895, emotion: "anger" },
        { t: "14:21", author: "Castilla Shaula", role: "client", text: "por que entonces filtrar con tu nombre fiscal número de factura no me aparece nada", valence: -0.4025, emotion: "anger" },
        { t: "14:28", author: "M. Hernández", role: "seller", text: "déjame revisarlo con contabilidad y le confirmo en la mañana", valence: 0.05, emotion: "others" },
        { t: "14:32", author: "Castilla Shaula", role: "client", text: "ok pero por favor que ya es la tercera vez", valence: -0.31, emotion: "anger" },
      ]
    },
    {
      id: "c2", clientId: "T1_carmen", clientName: "Carmen Karful",
      session: "T1 Carmen Karful", office: "T1", category: "Consumibles", seller: "L. Vázquez",
      date: "2026-04-27", lastMsg: "11:08",
      productMentions: ["cartuchos", "tinta", "papel bond"],
      objections: [],
      avgValence: 0.18, msgCount: 7,
      messages: [
        { t: "10:42", author: "Carmen Karful", role: "client", text: "hola buen día, ¿tienen cartuchos hp 664 negro y color?", valence: 0.05, emotion: "others" },
        { t: "10:44", author: "L. Vázquez", role: "seller", text: "buenos días Carmen, sí tenemos disponible. ¿Cuántas piezas?", valence: 0.15, emotion: "joy" },
        { t: "10:46", author: "Carmen Karful", role: "client", text: "necesito 4 negros y 2 de color, y dos paquetes de papel bond", valence: 0.10, emotion: "others" },
        { t: "10:50", author: "L. Vázquez", role: "seller", text: "perfecto, total $4,820 con factura. ¿Le envío hoy?", valence: 0.20, emotion: "joy" },
        { t: "10:55", author: "Carmen Karful", role: "client", text: "sí porfa, mañana en la mañana mejor", valence: 0.30, emotion: "joy" },
        { t: "11:02", author: "L. Vázquez", role: "seller", text: "listo, agendado para mañana 9-11am", valence: 0.25, emotion: "joy" },
        { t: "11:08", author: "Carmen Karful", role: "client", text: "gracias!", valence: 0.78, emotion: "joy" },
      ]
    },
    {
      id: "c3", clientId: "T4_cuprum", clientName: "Cuprum Construcción",
      session: "T4 Cuprum Construcción 44531", office: "T4", category: "Mobiliario", seller: "M. Hernández",
      date: "2026-04-02", lastMsg: "16:40",
      productMentions: ["sillas", "escritorios", "mobiliario oficina"],
      objections: ["precio alto", "comparando con competencia", "tiempo entrega"],
      avgValence: -0.22, msgCount: 9,
      messages: [
        { t: "15:10", author: "Ana Cuprum", role: "client", text: "buenas tardes, necesitamos cotización de 12 sillas ejecutivas y 4 escritorios", valence: 0.08, emotion: "others" },
        { t: "15:14", author: "M. Hernández", role: "seller", text: "claro, le mando el catálogo y opciones por rango de precio", valence: 0.18, emotion: "joy" },
        { t: "15:42", author: "M. Hernández", role: "seller", text: "envié 3 opciones, la línea ejecutiva queda en $128,400 + IVA", valence: 0.12, emotion: "others" },
        { t: "15:55", author: "Ana Cuprum", role: "client", text: "está más caro de lo que vimos con otro proveedor", valence: -0.45, emotion: "sadness" },
        { t: "16:02", author: "Ana Cuprum", role: "client", text: "salieron más chicas las cabos en unos botes de basura", valence: -0.4082, emotion: "anger" },
        { t: "16:10", author: "M. Hernández", role: "seller", text: "podemos revisar especificación, ¿qué proveedor están comparando?", valence: 0.05, emotion: "others" },
        { t: "16:22", author: "Ana Cuprum", role: "client", text: "y el tiempo de entrega de 3 semanas tampoco nos sirve", valence: -0.52, emotion: "anger" },
        { t: "16:34", author: "M. Hernández", role: "seller", text: "podemos negociar, máximo 10 días con un anticipo del 50%", valence: 0.08, emotion: "others" },
        { t: "16:40", author: "Ana Cuprum", role: "client", text: "lo platico con el equipo y le aviso", valence: -0.10, emotion: "others" },
      ]
    },
    {
      id: "c4", clientId: "T2_daniela", clientName: "Daniela 4675",
      session: "T2 Daniela 46752", office: "T2", category: "Papelería", seller: "R. Varma",
      date: "2026-01-09", lastMsg: "10:24",
      productMentions: ["paquete", "factura", "rollos"],
      objections: ["paquetes rotos", "calidad"],
      avgValence: -0.34, msgCount: 6,
      messages: [
        { t: "09:50", author: "Daniela Mora", role: "client", text: "porque está tan caro el paquete", valence: -0.471, emotion: "anger" },
        { t: "09:54", author: "R. Varma", role: "seller", text: "está al precio de lista, ¿le mando catálogo de la línea económica?", valence: 0.05, emotion: "others" },
        { t: "10:02", author: "Daniela Mora", role: "client", text: "son paquetes de verdad", valence: -0.5147, emotion: "anger" },
        { t: "10:10", author: "Daniela Mora", role: "client", text: "rollos de estos", valence: -0.1034, emotion: "others" },
        { t: "10:18", author: "R. Varma", role: "seller", text: "puedo aplicarle 8% por volumen si lleva 10 paquetes", valence: 0.10, emotion: "others" },
        { t: "10:24", author: "Daniela Mora", role: "client", text: "vales de caja", valence: -0.0025, emotion: "others" },
      ]
    },
    {
      id: "c5", clientId: "T5_visi", clientName: "Vision C. Cleam",
      session: "T5 45101 Vision C. Cleam", office: "T5", category: "Mobiliario", seller: "L. Vázquez",
      date: "2026-03-07", lastMsg: "12:18",
      productMentions: ["mesa juntas", "credenza"],
      objections: ["entrega lenta"],
      avgValence: 0.28, msgCount: 5,
      messages: [
        { t: "11:42", author: "Lucía V.", role: "client", text: "buen día, retomamos lo de la mesa de juntas?", valence: 0.10, emotion: "others" },
        { t: "11:46", author: "L. Vázquez", role: "seller", text: "claro, ¿confirmamos la de roble 2.40m con la credenza?", valence: 0.20, emotion: "joy" },
        { t: "11:55", author: "Lucía V.", role: "client", text: "sí, manden cotización formal porfa", valence: 0.32, emotion: "joy" },
        { t: "12:08", author: "L. Vázquez", role: "seller", text: "enviado, total $86,200, entrega 8 días hábiles", valence: 0.18, emotion: "others" },
        { t: "12:18", author: "Lucía V.", role: "client", text: "si porfavor, se lo agradeceria mucho", valence: 0.6274, emotion: "joy" },
      ]
    },
    {
      id: "c6", clientId: "T4_katia", clientName: "Katia Agrícola Vida",
      session: "T4 Katia Agrícola Vida Hogar 47387", office: "T4", category: "Limpieza", seller: "M. Hernández",
      date: "2026-04-04", lastMsg: "13:02",
      productMentions: ["cajas archivo", "correctores"],
      objections: [],
      avgValence: 0.05, msgCount: 5,
      messages: [
        { t: "12:30", author: "Katia A.", role: "client", text: "me cotizas cajas de archivo porfavor", valence: -0.1518, emotion: "others" },
        { t: "12:34", author: "M. Hernández", role: "seller", text: "claro, ¿cuántas piezas y qué tamaño?", valence: 0.10, emotion: "others" },
        { t: "12:42", author: "Katia A.", role: "client", text: "los correctores aparte por fis", valence: 0.142, emotion: "others" },
        { t: "12:50", author: "M. Hernández", role: "seller", text: "te paso ambas cotizaciones por separado", valence: 0.18, emotion: "joy" },
        { t: "13:02", author: "Katia A.", role: "client", text: "perfecto, te confirmo mañana temprano", valence: 0.42, emotion: "joy" },
      ]
    },
    {
      id: "c7", clientId: "T6_sistemas", clientName: "Sistemas de Impresión",
      session: "T6 Sistemas de Impresión Compras", office: "T6", category: "Equipos", seller: "R. Varma",
      date: "2026-01-23", lastMsg: "15:50",
      productMentions: ["copiador", "tóner"],
      objections: ["nota crédito pendiente"],
      avgValence: 0.04, msgCount: 6,
      messages: [
        { t: "14:55", author: "Jorge S.", role: "client", text: "pero no se ha cancelado? por que el conador me está preguntando por esa factura", valence: 0.0562, emotion: "surprise" },
        { t: "15:00", author: "R. Varma", role: "seller", text: "déjame revisar con admin, te confirmo en 30 min", valence: 0.10, emotion: "others" },
        { t: "15:14", author: "Jorge S.", role: "client", text: "si, gracias porfavor", valence: 0.22, emotion: "joy" },
        { t: "15:32", author: "R. Varma", role: "seller", text: "ya está aplicada la nota de crédito, te paso comprobante", valence: 0.20, emotion: "joy" },
        { t: "15:42", author: "Jorge S.", role: "client", text: "igual me haces la nota de crédito por la devolución porque cuestan más baratas las navajas", valence: -0.0027, emotion: "others" },
        { t: "15:50", author: "R. Varma", role: "seller", text: "anotado, lo gestiono con almacén", valence: 0.10, emotion: "others" },
      ]
    },
    {
      id: "c8", clientId: "T4_copycos", clientName: "Copycos Imp.",
      session: "T3 Copycos 16807", office: "T4", category: "Consumibles", seller: "L. Vázquez",
      date: "2026-04-13", lastMsg: "09:34",
      productMentions: [],
      objections: ["precio elevado"],
      avgValence: -0.31, msgCount: 4,
      messages: [
        { t: "09:18", author: "Mario L.", role: "client", text: "precio de una vez", valence: -0.487, emotion: "anger" },
        { t: "09:22", author: "L. Vázquez", role: "seller", text: "buenos días, ¿de qué producto exactamente?", valence: 0.10, emotion: "others" },
        { t: "09:28", author: "Mario L.", role: "client", text: "los correctores", valence: -0.05, emotion: "others" },
        { t: "09:34", author: "L. Vázquez", role: "seller", text: "$48 c/u + IVA, mínimo 5 piezas", valence: 0.08, emotion: "others" },
      ]
    },
  ];

  const kpis = {
    conversations: 184,
    conversationsDelta: +12.4,
    avgValence: 0.08,
    avgValenceDelta: +0.04,
    messagesProcessed: 4286,
    authors: 26,
  };

  const emotionDist = [
    { name: "others",   count: 2104, color: "var(--emo-others-fg)" },
    { name: "joy",      count:  921, color: "var(--emo-joy-fg)" },
    { name: "anger",    count:  712, color: "var(--emo-anger-fg)" },
    { name: "sadness",  count:  304, color: "var(--emo-sadness-fg)" },
    { name: "surprise", count:  178, color: "var(--emo-surprise-fg)" },
    { name: "fear",     count:   67, color: "var(--emo-fear-fg)" },
  ];

  // Source: sentiment_by_author.csv
  const authorSentiment = [
    // T1
    { author: "T1 Carmen Karful 45143",         vendedora: "T1", role: "client", totalMessages: 210, posPct: 38.1, neuPct: 57.6, negPct: 4.3,  avgScore:  0.28, dominant: "NEU" },
    { author: "T1 Dulce 45871",                  vendedora: "T1", role: "client", totalMessages:  87, posPct: 31.0, neuPct: 64.4, negPct: 4.6,  avgScore:  0.18, dominant: "NEU" },
    { author: "T1 Patricia 30049 Urrea",         vendedora: "T1", role: "client", totalMessages:  63, posPct: 29.0, neuPct: 66.7, negPct: 4.8,  avgScore:  0.15, dominant: "NEU" },
    { author: "T1 Betzavel Laso Roman",          vendedora: "T1", role: "client", totalMessages:  42, posPct: 33.3, neuPct: 61.9, negPct: 4.8,  avgScore:  0.21, dominant: "NEU" },
    // T2
    { author: "T2 Oriana 46797 Taller Capule",   vendedora: "T2", role: "client", totalMessages: 318, posPct: 34.6, neuPct: 60.1, negPct: 5.3,  avgScore:  0.22, dominant: "NEU" },
    { author: "T2 Daniela 46752",                vendedora: "T2", role: "client", totalMessages:  95, posPct: 25.3, neuPct: 65.3, negPct: 9.5,  avgScore:  0.09, dominant: "NEU" },
    { author: "T2 Jaime 47559",                  vendedora: "T2", role: "client", totalMessages:  58, posPct: 32.8, neuPct: 63.8, negPct: 3.4,  avgScore:  0.21, dominant: "NEU" },
    { author: "T2 Lesli 47721",                  vendedora: "T2", role: "client", totalMessages:  44, posPct: 36.4, neuPct: 59.1, negPct: 4.5,  avgScore:  0.25, dominant: "NEU" },
    // T4
    { author: "T4 Electrica Aselco 19649",       vendedora: "T4", role: "client", totalMessages: 110, posPct: 32.7, neuPct: 64.5, negPct: 2.7,  avgScore:  0.24, dominant: "NEU" },
    { author: "T4 Katia Agrícola Vida 47387",    vendedora: "T4", role: "client", totalMessages:  78, posPct: 35.9, neuPct: 59.0, negPct: 5.1,  avgScore:  0.26, dominant: "NEU" },
    { author: "T4 Cuprum Constitucion 44531",    vendedora: "T4", role: "client", totalMessages:  54, posPct: 22.2, neuPct: 64.8, negPct: 13.0, avgScore:  0.05, dominant: "NEU" },
    { author: "T4 Angelita Río Yaqui 44208",     vendedora: "T4", role: "client", totalMessages:  41, posPct: 29.3, neuPct: 65.9, negPct: 4.9,  avgScore:  0.16, dominant: "NEU" },
    { author: "T4 Copycos 16807",                vendedora: "T4", role: "client", totalMessages:  18, posPct: 16.7, neuPct: 66.7, negPct: 16.7, avgScore: -0.08, dominant: "NEU" },
    { author: "T4 Jesús Meléndez 31713",         vendedora: "T4", role: "client", totalMessages:  37, posPct: 27.0, neuPct: 67.6, negPct: 5.4,  avgScore:  0.14, dominant: "NEU" },
    // T5
    { author: "T5 Castilla Shaula",              vendedora: "T5", role: "client", totalMessages:  72, posPct: 19.4, neuPct: 58.3, negPct: 22.2, avgScore: -0.12, dominant: "NEU" },
    { author: "T5 Oriana Tribunal Agrario",      vendedora: "T5", role: "client", totalMessages:  10, posPct: 30.0, neuPct: 70.0, negPct:  0.0, avgScore:  0.19, dominant: "NEU" },
    { author: "T5 Alberto 31892 Inmobiliaria",   vendedora: "T5", role: "client", totalMessages:  56, posPct: 33.9, neuPct: 60.7, negPct: 5.4,  avgScore:  0.22, dominant: "NEU" },
    { author: "T5 Raul Vama",                    vendedora: "T5", role: "client", totalMessages:  29, posPct: 31.0, neuPct: 65.5, negPct: 3.4,  avgScore:  0.19, dominant: "NEU" },
    // T6
    { author: "T6 Maricela (41378) Jose Ángel",  vendedora: "T6", role: "client", totalMessages:  10, posPct: 30.0, neuPct: 70.0, negPct:  0.0, avgScore:  0.25, dominant: "NEU" },
    { author: "T6 Sistemas de Impresion",        vendedora: "T6", role: "client", totalMessages:  89, posPct: 33.7, neuPct: 61.8, negPct: 4.5,  avgScore:  0.22, dominant: "NEU" },
    { author: "T6 Cleotilde Kimivac Olivas",     vendedora: "T6", role: "client", totalMessages:  34, posPct: 35.3, neuPct: 61.8, negPct: 2.9,  avgScore:  0.26, dominant: "NEU" },
    // T9
    { author: "T9 Miriam Fienmont 45737",        vendedora: "T9", role: "client", totalMessages: 134, posPct: 28.4, neuPct: 65.7, negPct: 6.0,  avgScore:  0.14, dominant: "NEU" },
    { author: "T9 Drenax 42513",                 vendedora: "T9", role: "client", totalMessages:  52, posPct: 30.8, neuPct: 65.4, negPct: 3.8,  avgScore:  0.18, dominant: "NEU" },
    { author: "T9 Ferre laminas 46266",          vendedora: "T9", role: "client", totalMessages:  27, posPct: 25.9, neuPct: 70.4, negPct: 3.7,  avgScore:  0.13, dominant: "NEU" },
    // Empresa
    { author: "Permagraf",                        vendedora: "—",  role: "seller", totalMessages: 2518, posPct: 32.4, neuPct: 63.5, negPct: 4.1, avgScore: 0.18, dominant: "NEU" },
    { author: "Comercios Unidos",                 vendedora: "—",  role: "seller", totalMessages: 1842, posPct: 34.1, neuPct: 62.4, negPct: 3.5, avgScore: 0.20, dominant: "NEU" },
  ];

  return { clients, conversations, kpis, emotionDist, authorSentiment, domainDictionary: [] };
})();
