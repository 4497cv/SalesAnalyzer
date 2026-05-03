// Sentiment by author view — from sentiment_by_author.csv
const AuthorsView = () => {
  const [filter, setFilter]   = React.useState("all");
  const [sortBy, setSortBy]   = React.useState("avgScore");
  const [sortDir, setSortDir] = React.useState("desc");

  const filtered = MOCK.authorSentiment.filter(a => {
    if (filter === "client") return a.role === "client";
    if (filter === "seller") return a.role === "seller";
    return true;
  });

  const sorted = [...filtered].sort((a, b) => {
    const va = a[sortBy], vb = b[sortBy];
    return sortDir === "desc" ? vb - va : va - vb;
  });

  const totalMsgs = filtered.reduce((s, a) => s + a.totalMessages, 0);
  const avgScore  = filtered.length > 0
    ? filtered.reduce((s, a) => s + a.avgScore, 0) / filtered.length
    : 0;

  const toggleSort = col => {
    if (sortBy === col) setSortDir(d => d === "desc" ? "asc" : "desc");
    else { setSortBy(col); setSortDir("desc"); }
  };

  const SortTh = ({ col, label, right }) => (
    <th onClick={() => toggleSort(col)}
        style={{cursor: "pointer", userSelect: "none", textAlign: right ? "right" : "left"}}>
      {label}{sortBy === col ? (sortDir === "desc" ? " ↓" : " ↑") : ""}
    </th>
  );

  const tabs = [["all", "Todos"], ["client", "Clientes"], ["seller", "Empresa"]];

  return (
    <div>
      <div className="section-head">
        <div>
          <h1>Sentimiento por autor</h1>
          <p>Distribución POS / NEU / NEG y score promedio por autor · fuente: sentiment_by_author.csv</p>
        </div>
        <div style={{display: "flex", gap: 8}}>
          <button className="btn"><Icon name="download" size={12} /> Exportar</button>
        </div>
      </div>

      <div style={{display: "flex", gap: 8, marginBottom: 16, alignItems: "center", flexWrap: "wrap"}}>
        {tabs.map(([v, l]) => (
          <button key={v} className={`filter-chip ${filter === v ? "is-active" : ""}`}
                  onClick={() => setFilter(v)}>{l}</button>
        ))}
        <div style={{marginLeft: "auto", fontSize: 12, color: "var(--text-muted)"}}>
          {filtered.length} autores · {totalMsgs.toLocaleString()} mensajes · score promedio:{" "}
          <ValenceNum value={avgScore} />
        </div>
      </div>

      <div className="card">
        <div className="card__body" style={{padding: 0}}>
          <table className="msg-table">
            <thead>
              <tr>
                <SortTh col="author"        label="Autor" />
                <th>Vendedora</th>
                <SortTh col="totalMessages" label="Mensajes" right />
                <th style={{minWidth: 180}}>POS · NEU · NEG</th>
                <SortTh col="posPct"        label="% Pos" right />
                <SortTh col="negPct"        label="% Neg" right />
                <SortTh col="avgScore"      label="Score"  right />
              </tr>
            </thead>
            <tbody>
              {sorted.map((a, i) => (
                <tr key={i}>
                  <td style={{fontWeight: 500}}>
                    <span className={`author-dot author-dot--${a.role === "seller" ? "seller" : "client"}`}
                          style={{display: "inline-block", marginRight: 8, verticalAlign: "middle"}} />
                    {a.author}
                  </td>
                  <td>
                    {a.vendedora !== "—"
                      ? <span className="tag">{a.vendedora}</span>
                      : <span style={{color: "var(--text-faint)"}}>—</span>}
                  </td>
                  <td className="col-time" style={{textAlign: "right"}}>{a.totalMessages.toLocaleString()}</td>
                  <td>
                    <div className="sent-bar">
                      <div className="sent-bar__pos" style={{width: `${a.posPct}%`}}
                           title={`Positivo ${a.posPct.toFixed(1)}%`} />
                      <div className="sent-bar__neu" style={{width: `${a.neuPct}%`}}
                           title={`Neutro ${a.neuPct.toFixed(1)}%`} />
                      <div className="sent-bar__neg" style={{width: `${a.negPct}%`}}
                           title={`Negativo ${a.negPct.toFixed(1)}%`} />
                    </div>
                  </td>
                  <td className="col-time" style={{textAlign: "right", color: "var(--pos)"}}>
                    {a.posPct.toFixed(1)}%
                  </td>
                  <td className="col-time" style={{textAlign: "right", color: a.negPct > 8 ? "var(--neg)" : "var(--text-muted)"}}>
                    {a.negPct.toFixed(1)}%
                  </td>
                  <td style={{textAlign: "right"}}><ValenceNum value={a.avgScore} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={{marginTop: 12, fontSize: 11.5, color: "var(--text-faint)"}}>
        Score: promedio ponderado POS − NEG por mensaje. Columna "POS · NEU · NEG" a escala 100%. Modelo: BETO-sentiment-es.
      </div>
    </div>
  );
};

Object.assign(window, { AuthorsView });
