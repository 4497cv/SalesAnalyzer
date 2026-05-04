// Conversation Explorer — filters + list + tabular chat detail
const ConversationExplorer = () => {
  const [selectedId, setSelectedId] = React.useState(
    MOCK.conversations.length > 0 ? MOCK.conversations[0].id : null
  );
  const [filterClient, setFilterClient] = React.useState("all");
  const [filterOffice, setFilterOffice] = React.useState("all");
  const [dateRange,    setDateRange]    = React.useState("all");
  const [sortValence,  setSortValence]  = React.useState("none");
  const [filterAlert,  setFilterAlert]  = React.useState("all");
  const [filterTopic,  setFilterTopic]  = React.useState("all");
  const [search,       setSearch]       = React.useState("");
  const [hoverMsg,     setHoverMsg]     = React.useState(null);
  const [tooltipPos,   setTooltipPos]   = React.useState({x: 0, y: 0});

  // Unique offices derived from conversations
  const offices = React.useMemo(
    () => [...new Set(MOCK.conversations.map(c => c.office))].sort(),
    []
  );

  // Date cutoff based on range selector
  const cutoff = React.useMemo(() => {
    const today = new Date("2026-05-02");
    if (dateRange === "30d")  { const d = new Date(today); d.setDate(d.getDate() - 30);  return d.toISOString().slice(0,10); }
    if (dateRange === "90d")  { const d = new Date(today); d.setDate(d.getDate() - 90);  return d.toISOString().slice(0,10); }
    if (dateRange === "180d") { const d = new Date(today); d.setDate(d.getDate() - 180); return d.toISOString().slice(0,10); }
    if (dateRange === "ytd")  return "2026-01-01";
    return null; // "all"
  }, [dateRange]);

  const filtered = React.useMemo(() => {
    let result = MOCK.conversations.filter(c => {
      if (filterClient !== "all" && c.clientId !== filterClient) return false;
      if (filterOffice !== "all" && c.office  !== filterOffice)  return false;
      if (cutoff && c.date < cutoff) return false;
      if (filterAlert === "alert" && !c.hasAlert) return false;
      if (filterAlert === "ok"    &&  c.hasAlert) return false;
      if (filterTopic !== "all" && c.topicCluster !== filterTopic) return false;
      if (search) {
        const q = search.toLowerCase();
        if (!c.clientName.toLowerCase().includes(q) &&
            !c.messages.some(m => m.text.toLowerCase().includes(q))) return false;
      }
      return true;
    });
    if (sortValence === "pos") result = [...result].sort((a, b) => b.avgValence - a.avgValence);
    if (sortValence === "neg") result = [...result].sort((a, b) => a.avgValence - b.avgValence);
    return result;
  }, [filterClient, filterOffice, cutoff, search, sortValence, filterAlert, filterTopic]);

  const selected = filtered.find(c => c.id === selectedId) || filtered[0];

  React.useEffect(() => {
    if (selected && selected.id !== selectedId) setSelectedId(selected.id);
  }, [filterClient, filterOffice, dateRange, search, sortValence, filterAlert, filterTopic]);

  return (
    <div>
      <div className="section-head">
        <div>
          <h1>Explorador de conversaciones</h1>
          <p>Filtra por cliente, vendedora y fecha. Cada mensaje muestra su valencia y emoción inferida.</p>
        </div>
        <div style={{display: "flex", gap: 8}}>
          <button className="btn btn--primary"><Icon name="download" size={12} /> Exportar CSV</button>
        </div>
      </div>

      <div className="filters">
        <div className="search-input">
          <Icon name="search" size={13} />
          <input placeholder="Buscar texto o cliente…" value={search}
                 onChange={e => setSearch(e.target.value)} />
        </div>

        <select className="input" value={filterClient}
                onChange={e => setFilterClient(e.target.value)}>
          <option value="all">Cliente: todos</option>
          {MOCK.clients.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>

        <select className="input" value={filterOffice}
                onChange={e => setFilterOffice(e.target.value)}>
          <option value="all">Vendedora: todas</option>
          {offices.map(o => (
            <option key={o} value={o}>{o}</option>
          ))}
        </select>

        <select className="input" value={dateRange}
                onChange={e => setDateRange(e.target.value)}>
          <option value="all">Todas las fechas</option>
          <option value="30d">Últimos 30 días</option>
          <option value="90d">Últimos 90 días</option>
          <option value="180d">Últimos 6 meses</option>
          <option value="ytd">Año en curso</option>
        </select>

        <select className="input" value={sortValence}
                onChange={e => setSortValence(e.target.value)}>
          <option value="none">Valencia: sin orden</option>
          <option value="pos">↑ Más positivas primero</option>
          <option value="neg">↓ Más negativas primero</option>
        </select>

        <select className="input" value={filterAlert}
                onChange={e => setFilterAlert(e.target.value)}>
          <option value="all">Advertencias: todas</option>
          <option value="alert">⚠ Solo con advertencia</option>
          <option value="ok">Sin advertencia</option>
        </select>

        <select className="input" value={filterTopic}
                onChange={e => setFilterTopic(e.target.value)}>
          <option value="all">Tag: todos</option>
          {Object.entries(TOPIC_STYLES).map(([key, s]) => (
            <option key={key} value={key}>{s.label}</option>
          ))}
        </select>

        <div style={{marginLeft: "auto", fontSize: 11.5, color: "var(--text-muted)"}}>
          {filtered.length} de {MOCK.conversations.length} conversaciones
        </div>
      </div>

      <div className="explorer">
        <div className="conv-list">
          <div className="conv-list__head">
            <span>Conversaciones</span>
            <span>{filtered.length}</span>
          </div>
          <div className="conv-list__items">
            {filtered.map(c => (
              <div key={c.id}
                   className={`conv-item ${selectedId === c.id ? "is-selected" : ""}`}
                   onClick={() => setSelectedId(c.id)}>
                <div className="conv-item__top">
                  <span>{c.clientName}</span>
                  <span className="conv-item__time">{c.date.slice(8) + "-" + c.date.slice(5, 7)}</span>
                </div>
                <div className="conv-item__preview">
                  {c.messages[c.messages.length - 1].text}
                </div>
                <div className="conv-item__meta">
                  <span className="tag">{c.office}</span>
                  <TopicBadge topic={c.topicCluster} />
                  <span style={{marginLeft: "auto", display: "flex", alignItems: "center", gap: 6}}>
                    {c.hasAlert && (
                      <span title="Contiene mensajes con valencia < −0.5" style={{
                        display: "inline-flex", alignItems: "center", justifyContent: "center",
                        width: 16, height: 16, borderRadius: "50%",
                        background: "var(--neg-strong)", color: "#fff",
                        fontSize: 10, fontWeight: 700, flexShrink: 0,
                      }}>!</span>
                    )}
                    <ValenceNum value={c.avgValence} />
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {selected && (
          <div className="conv-detail">
            <div className="conv-detail__head">
              <div>
                <div className="conv-detail__client" style={{display: "flex", alignItems: "center", gap: 8}}>
                  {selected.clientName}
                  <TopicBadge topic={selected.topicCluster} />
                  {selected.hasAlert && (
                    <span style={{
                      display: "inline-flex", alignItems: "center", gap: 4,
                      background: "var(--neg-soft)", color: "var(--neg-strong)",
                      padding: "2px 8px", borderRadius: 999,
                      fontSize: 11, fontWeight: 600,
                    }}>
                      ⚠ mensaje crítico
                    </span>
                  )}
                </div>
                <div className="conv-detail__sub">
                  {selected.session} · {selected.seller} · {selected.date.slice(8) + "-" + selected.date.slice(5, 7) + "-" + selected.date.slice(0, 4)}
                </div>
              </div>
              <div className="conv-detail__metrics">
                <div className="conv-metric">
                  <span className="conv-metric__val">{selected.msgCount}</span>
                  <span>mensajes</span>
                </div>
                <div className="conv-metric">
                  <span className="conv-metric__val">
                    {selected.avgValence > 0 ? "+" : ""}{selected.avgValence.toFixed(2)}
                  </span>
                  <span>valencia</span>
                </div>
              </div>
            </div>

            <div className="conv-detail__body">
              <table className="msg-table">
                <thead>
                  <tr>
                    <th>Pos.</th>
                    <th>Autor</th>
                    <th>Mensaje</th>
                    <th>Valencia</th>
                    <th>Emoción dominante</th>
                  </tr>
                </thead>
                <tbody>
                  {selected.messages.map((m, i) => {
                    const EMO = {
                      joy:      { bg: "var(--emo-joy-bg)",    fg: "var(--emo-joy-fg)" },
                      surprise: { bg: "#dbeafe",               fg: "#1d4ed8" },
                      others:   { bg: "var(--emo-others-bg)", fg: "var(--emo-others-fg)" },
                      fear:     { bg: "var(--neg-soft)",       fg: "var(--neg-strong)" },
                      sadness:  { bg: "var(--emo-fear-bg)",   fg: "var(--emo-fear-fg)" },
                      disgust:  { bg: "#fde8d0",               fg: "#92400e" },
                      anger:    { bg: "var(--neg-soft)",       fg: "var(--neg-strong)" },
                    };
                    const ec   = EMO[m.emotion] || EMO.others;
                    const pct  = ((m[`p_${m.emotion}`] ?? 0) * 100).toFixed(1);
                    return (
                    <tr key={i}
                        style={m.valence < -0.1 ? {background: "var(--neg-soft)"} : undefined}
                        onMouseEnter={e => {
                          setHoverMsg({...m, idx: i});
                          setTooltipPos({x: e.clientX, y: e.clientY});
                        }}
                        onMouseMove={e => setTooltipPos({x: e.clientX, y: e.clientY})}
                        onMouseLeave={() => setHoverMsg(null)}>
                      <td className="col-time">{m.t}</td>
                      <td className="col-author">
                        <AuthorChip author={m.author} role={m.role} />
                      </td>
                      <td className="col-text">{m.text}</td>
                      <td className="col-valence">
                        <span className="valence-cell">
                          <ValenceBar value={m.valence} />
                          <ValenceNum value={m.valence} />
                        </span>
                      </td>
                      <td className="col-emotion">
                        <span style={{
                          display: "inline-flex", alignItems: "center", gap: 5,
                          background: ec.bg, color: ec.fg,
                          padding: "2px 8px", borderRadius: 999,
                          fontSize: 11, fontWeight: 500, whiteSpace: "nowrap",
                        }}>
                          <span style={{width:5, height:5, borderRadius:"50%", background: ec.fg, flexShrink:0}} />
                          {m.emotion}
                          <span style={{opacity: 0.75}}>{pct}%</span>
                        </span>
                      </td>
                    </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {hoverMsg && (
        <div className="tooltip"
             style={{left: tooltipPos.x + 14, top: tooltipPos.y + 14}}>
          <div style={{fontWeight: 600, marginBottom: 6}}>
            Mensaje {hoverMsg.t} · {hoverMsg.posPct}% conversación
          </div>
          <div className="tooltip__row">
            <span className="tooltip__k">Autor</span>
            <span>{hoverMsg.author}</span>
          </div>
          <div className="tooltip__row">
            <span className="tooltip__k">Rol</span>
            <span>{hoverMsg.role === "seller" ? "vendedora" : "cliente"}</span>
          </div>
          <div className="tooltip__row">
            <span className="tooltip__k">Valencia</span>
            <span>{hoverMsg.valence > 0 ? "+" : ""}{hoverMsg.valence.toFixed(4)}</span>
          </div>
          <div style={{borderTop:"1px solid rgba(255,255,255,0.15)", margin:"6px 0 4px"}} />
          {[
            ["joy",      hoverMsg.p_joy],
            ["surprise", hoverMsg.p_surprise],
            ["others",   hoverMsg.p_others],
            ["fear",     hoverMsg.p_fear],
            ["sadness",  hoverMsg.p_sadness],
            ["disgust",  hoverMsg.p_disgust],
            ["anger",    hoverMsg.p_anger],
          ].map(([emo, p]) => (
            <div key={emo} className="tooltip__row">
              <span className="tooltip__k">{emo}</span>
              <span style={{fontFamily:"var(--font-mono)", fontSize:11}}>
                {(p * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

Object.assign(window, { ConversationExplorer });
