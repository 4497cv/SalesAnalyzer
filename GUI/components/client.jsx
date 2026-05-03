// Client detail view — list of clients + selected client timeline
const ClientView = () => {
  const [selectedId, setSelectedId] = React.useState(MOCK.clients[0].id);
  const client = MOCK.clients.find(c => c.id === selectedId);
  const clientConvs = MOCK.conversations.filter(c => c.clientId === selectedId);

  const valenceType = v => v > 0.15 ? "pos" : v < -0.15 ? "neg" : "neu";

  const timeline = [
    ...clientConvs.map(c => ({
      date: c.date,
      type: valenceType(c.avgValence),
      title: `Conversación · ${c.category}`,
      meta: [c.session, c.seller, `${c.msgCount} mensajes`],
    })),
    { date: "2026-02-18", type: "pos", title: "Conversación · Consumibles", meta: ["T1", "vía recompra programada", "6 mensajes"] },
    { date: "2025-12-04", type: "pos", title: "Conversación · Papelería", meta: ["T1", "M. Hernández", "11 mensajes"] },
    { date: "2025-10-22", type: "neu", title: "Conversación · Mobiliario", meta: ["T1", "L. Vázquez", "8 mensajes"] },
  ].sort((a, b) => b.date.localeCompare(a.date));

  const avgV = clientConvs.length > 0
    ? clientConvs.reduce((s, c) => s + c.avgValence, 0) / clientConvs.length
    : 0;

  return (
    <div>
      <div className="section-head">
        <div>
          <h1>Clientes</h1>
          <p>Historial conversacional y patrones por cliente. {MOCK.clients.length} clientes activos.</p>
        </div>
        <div style={{display: "flex", gap: 8}}>
          <button className="btn"><Icon name="filter" size={12} /> Filtrar</button>
        </div>
      </div>

      <div className="client-grid">
        <div>
          <div className="card" style={{marginBottom: 12}}>
            <div className="card__head"><div className="card__title">Cartera ({MOCK.clients.length})</div></div>
            <div style={{maxHeight: 520, overflowY: "auto"}}>
              {MOCK.clients.map(c => (
                <div key={c.id} className={`conv-item ${selectedId === c.id ? "is-selected" : ""}`} onClick={() => setSelectedId(c.id)}>
                  <div className="conv-item__top">
                    <span>{c.name}</span>
                    <span className="conv-item__time">{c.office}</span>
                  </div>
                  <div className="conv-item__preview">{c.contact} · {c.category}</div>
                  <div className="conv-item__meta">
                    <span className="tag">{c.segment}</span>
                    <span style={{marginLeft: "auto"}}>{c.conversations} chats</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div className="client-card">
            <div style={{display: "flex", alignItems: "flex-start", gap: 14, flexWrap: "wrap"}}>
              <div className="avatar" style={{width: 48, height: 48, fontSize: 16, background: "var(--brand)", color: "var(--accent)"}}>{client.name.slice(0, 2).toUpperCase()}</div>
              <div style={{flex: 1}}>
                <h2 className="client-card__name">{client.name}</h2>
                <div className="client-card__sub">{client.contact} · {client.phone} · cliente desde {client.since}</div>
                <div style={{display: "flex", gap: 6, marginTop: 8}}>
                  <span className="tag">{client.segment}</span>
                  <span className="tag">{client.category}</span>
                  <span className="tag">{client.office}</span>
                </div>
              </div>
              <button className="btn btn--sm">Abrir conversaciones</button>
            </div>

            <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 12, marginTop: 18, paddingTop: 16, borderTop: "1px solid var(--border)"}}>
              <div><div className="kpi__label">LTV</div><div style={{fontSize: 18, fontWeight: 600, marginTop: 2}}>${client.ltv.toLocaleString()}</div></div>
              <div><div className="kpi__label">Conversaciones</div><div style={{fontSize: 18, fontWeight: 600, marginTop: 2}}>{client.conversations}</div></div>
              <div><div className="kpi__label">Valencia promedio</div><div style={{fontSize: 18, fontWeight: 600, marginTop: 2}}><ValenceNum value={avgV} /></div></div>
              <div><div className="kpi__label">Cadencia recompra</div><div style={{fontSize: 18, fontWeight: 600, marginTop: 2}}>{client.recompra}</div></div>
            </div>
          </div>

          <div className="card" style={{marginTop: 12}}>
            <div className="card__head">
              <div>
                <div className="card__title">Línea temporal</div>
                <div className="card__sub">Conversaciones y eventos comerciales</div>
              </div>
              <div style={{marginLeft: "auto"}}>
                <span className="tag">{clientConvs.length} recientes</span>
              </div>
            </div>
            <div className="card__body" style={{paddingTop: 0}}>
              <div className="timeline">
                {timeline.map((t, i) => (
                  <div className="tl-row" key={i}>
                    <div className="tl-date">{t.date}</div>
                    <div className={`tl-marker tl-marker--${t.type === "pos" ? "won" : t.type === "neg" ? "lost" : "open"}`}>
                      {t.type === "pos" && <Icon name="arrowUp" size={10} />}
                      {t.type === "neg" && <Icon name="arrowDown" size={10} />}
                      {t.type === "neu" && <span style={{fontSize: 14, lineHeight: 1}}>·</span>}
                    </div>
                    <div className="tl-content">
                      <div className="tl-title">{t.title}</div>
                      <div className="tl-meta">{t.meta.map((m, j) => <span key={j}>{m}</span>)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="card" style={{marginTop: 12}}>
            <div className="card__head">
              <div className="card__title">Próxima recompra estimada</div>
            </div>
            <div className="card__body" style={{display: "flex", alignItems: "center", gap: 16}}>
              <div style={{flex: 1}}>
                <div style={{fontSize: 13, color: "var(--text-muted)", marginBottom: 6}}>Basado en cadencia de {client.recompra} y última conversación</div>
                <div style={{display: "flex", gap: 8, flexWrap: "wrap"}}>
                  <span className="tag" style={{background: "var(--brand-soft)", color: "var(--brand)", borderColor: "transparent"}}>cartuchos hp · 4 piezas</span>
                  <span className="tag" style={{background: "var(--brand-soft)", color: "var(--brand)", borderColor: "transparent"}}>papel bond carta · 5 paquetes</span>
                  <span className="tag" style={{background: "var(--brand-soft)", color: "var(--brand)", borderColor: "transparent"}}>folders manila · 100 piezas</span>
                </div>
              </div>
              <button className="btn btn--accent">Generar borrador WhatsApp</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

Object.assign(window, { ClientView });
