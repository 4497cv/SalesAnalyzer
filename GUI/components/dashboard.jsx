// Dashboard view — KPIs, emotion distribution, sentiment by vendedora
const KpiCard = ({ label, value, delta, suffix }) => {
  const dir = delta > 0 ? "up" : delta < 0 ? "down" : "flat";
  const arrow = delta > 0 ? "arrowUp" : delta < 0 ? "arrowDown" : null;
  return (
    <div className="kpi">
      <div className="kpi__label">{label}</div>
      <div className="kpi__value">{value}{suffix}</div>
      {delta != null && (
        <div className={`kpi__delta kpi__delta--${dir}`}>
          {arrow && <Icon name={arrow} size={12} />}
          {delta > 0 ? "+" : ""}{delta}{suffix === "%" ? " pts" : "%"} vs. mes anterior
        </div>
      )}
    </div>
  );
};

const Donut = ({ data, total }) => {
  const size = 140, r = 56, cx = size / 2, cy = size / 2;
  const colors = ["var(--emo-others-fg)", "var(--emo-joy-fg)", "var(--emo-anger-fg)", "var(--emo-sadness-fg)", "var(--emo-surprise-fg)", "var(--emo-fear-fg)"];
  let acc = 0;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      {data.map((d, i) => {
        const frac = d.count / total;
        const start = acc * 2 * Math.PI - Math.PI / 2;
        const end = (acc + frac) * 2 * Math.PI - Math.PI / 2;
        acc += frac;
        const large = frac > 0.5 ? 1 : 0;
        const x1 = cx + r * Math.cos(start), y1 = cy + r * Math.sin(start);
        const x2 = cx + r * Math.cos(end), y2 = cy + r * Math.sin(end);
        return <path key={i} d={`M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} Z`} fill={colors[i]} stroke="var(--bg-elev)" strokeWidth="2" />;
      })}
      <circle cx={cx} cy={cy} r={32} fill="var(--bg-elev)" />
      <text x={cx} y={cy - 2} textAnchor="middle" fontSize="18" fontWeight="600" fill="var(--text)">{total.toLocaleString()}</text>
      <text x={cx} y={cy + 14} textAnchor="middle" fontSize="9" fill="var(--text-muted)">MENSAJES</text>
    </svg>
  );
};

const DashboardView = () => {
  const k = MOCK.kpis;
  const totalEmo = MOCK.emotionDist.reduce((a, b) => a + b.count, 0);

  // Compute per-vendedora avg sentiment from authorSentiment (clients only)
  const vendedoraStats = React.useMemo(() => {
    const groups = {};
    MOCK.authorSentiment
      .filter(a => a.role === "client")
      .forEach(a => {
        if (!groups[a.vendedora]) groups[a.vendedora] = { sumScore: 0, sumPos: 0, count: 0, msgs: 0 };
        groups[a.vendedora].sumScore += a.avgScore;
        groups[a.vendedora].sumPos   += a.posPct;
        groups[a.vendedora].count++;
        groups[a.vendedora].msgs += a.totalMessages;
      });
    return Object.entries(groups)
      .map(([code, g]) => ({
        code,
        avgScore: g.sumScore / g.count,
        posPct:   g.sumPos   / g.count,
        msgs:     g.msgs,
      }))
      .sort((a, b) => b.avgScore - a.avgScore);
  }, []);

  const maxPos = Math.max(...vendedoraStats.map(v => v.posPct));

  return (
    <div>
      <div className="section-head">
        <div>
          <h1>Dashboard</h1>
          <p>Vista general del corpus · {k.conversations} conversaciones · análisis de sentimiento · últimos 90 días</p>
        </div>
        <div style={{display: "flex", gap: 8}}>
          <button className="btn"><Icon name="calendar" size={12} /> Últimos 90 días</button>
          <button className="btn"><Icon name="download" size={12} /> Exportar</button>
        </div>
      </div>

      <div className="kpi-grid">
        <KpiCard label="Conversaciones" value={k.conversations} delta={k.conversationsDelta} />
        <KpiCard label="Valencia promedio" value={k.avgValence > 0 ? `+${k.avgValence}` : k.avgValence} delta={k.avgValenceDelta} />
        <KpiCard label="Mensajes procesados" value={k.messagesProcessed.toLocaleString()} />
        <KpiCard label="Autores analizados" value={k.authors} />
      </div>

      <div className="dash-grid">
        <div className="card">
          <div className="card__head">
            <div>
              <div className="card__title">Sentimiento por vendedora</div>
              <div className="card__sub">% mensajes positivos de sus clientes · score promedio</div>
            </div>
          </div>
          <div className="card__body">
            <div className="bar-chart">
              {vendedoraStats.map(v => (
                <div className="bar-row" key={v.code}>
                  <div className="bar-row__label" style={{fontWeight: 600}}>{v.code}</div>
                  <div className="bar-row__track">
                    <div className="bar-row__fill" style={{
                      width: `${(v.posPct / maxPos) * 100}%`,
                      background: v.avgScore >= 0.22 ? "var(--pos)" : v.avgScore >= 0.14 ? "var(--accent)" : "var(--neg)"
                    }} />
                  </div>
                  <div className="bar-row__val" style={{minWidth: 90, display: "flex", justifyContent: "flex-end", gap: 8, alignItems: "center"}}>
                    <span style={{color: "var(--text-faint)", fontSize: 11}}>{v.posPct.toFixed(1)}%</span>
                    <ValenceNum value={v.avgScore} />
                  </div>
                </div>
              ))}
            </div>
            <div style={{marginTop: 16, paddingTop: 12, borderTop: "1px solid var(--border)", display: "flex", gap: 16, fontSize: 11.5, color: "var(--text-muted)"}}>
              <span><span style={{display: "inline-block", width: 8, height: 8, background: "var(--pos)", borderRadius: 2, marginRight: 4}} />≥+0.22 alto</span>
              <span><span style={{display: "inline-block", width: 8, height: 8, background: "var(--accent)", borderRadius: 2, marginRight: 4}} />+0.14–0.21 medio</span>
              <span><span style={{display: "inline-block", width: 8, height: 8, background: "var(--neg)", borderRadius: 2, marginRight: 4}} />&lt;+0.14 bajo</span>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card__head">
            <div>
              <div className="card__title">Distribución de emociones</div>
              <div className="card__sub">Por mensaje, todo el corpus</div>
            </div>
          </div>
          <div className="card__body">
            <div className="donut-wrap">
              <Donut data={MOCK.emotionDist} total={totalEmo} />
              <div className="donut-legend">
                {MOCK.emotionDist.map(e => (
                  <div className="donut-legend__row" key={e.name}>
                    <span className="donut-legend__sw" style={{background: e.color}} />
                    <span className="donut-legend__name"><EmotionBadge emotion={e.name} /></span>
                    <span className="donut-legend__val">{e.count.toLocaleString()} · {((e.count/totalEmo)*100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

Object.assign(window, { DashboardView });
