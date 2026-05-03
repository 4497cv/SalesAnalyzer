// Shared UI primitives — icons, badges, valence bar, tooltips
const Icon = ({ name, size = 16, className = "" }) => {
  const paths = {
    upload: <><path d="M12 16V4M6 10l6-6 6 6"/><path d="M4 20h16"/></>,
    dashboard: <><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></>,
    chat: <><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></>,
    user: <><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/></>,
    settings: <><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h0a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h0a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v0a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></>,
    search: <><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></>,
    file: <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></>,
    check: <path d="M20 6 9 17l-5-5"/>,
    x: <><path d="M18 6 6 18M6 6l12 12"/></>,
    chevron: <path d="m9 18 6-6-6-6"/>,
    arrowUp: <path d="m18 15-6-6-6 6"/>,
    arrowDown: <path d="m6 9 6 6 6-6"/>,
    calendar: <><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></>,
    download: <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5M12 15V3"/></>,
    filter: <path d="M22 3H2l8 9.46V19l4 2v-8.54z"/>,
    folder: <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>,
    spark: <path d="m23 6-9.5 9.5-5-5L1 18"/>,
    package: <><path d="M16.5 9.4 7.55 4.24"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.27 6.96 12 12.01l8.73-5.05M12 22.08V12"/></>,
    building: <><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/></>,
    refresh: <><path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/></>,
    play: <path d="M5 3l14 9-14 9z"/>,
    sparkles: <><path d="M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6 5.6 18.4"/></>,
  };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      {paths[name]}
    </svg>
  );
};

// Maps valence in [-1, 1] to a color stop and width
function valenceColor(v) {
  if (v >= 0.15) return "var(--pos)";
  if (v <= -0.15) return "var(--neg)";
  return "var(--neu)";
}

const ValenceBar = ({ value }) => {
  // value: -1..1 → fill from center
  const center = 50;
  const pct = Math.min(Math.abs(value), 1) * 50;
  const isPos = value >= 0;
  const color = valenceColor(value);
  const left = isPos ? center : center - pct;
  return (
    <div className="valence-bar" title={value.toFixed(3)}>
      <div className="valence-bar__fill" style={{
        left: `${left}%`,
        width: `${pct}%`,
        background: color
      }} />
      <div style={{position: "absolute", left: "50%", top: 0, bottom: 0, width: 1, background: "var(--border-strong)"}} />
    </div>
  );
};

const ValenceNum = ({ value }) => {
  const cls = value >= 0.15 ? "valence-num--pos" : value <= -0.15 ? "valence-num--neg" : "valence-num--neu";
  const sign = value >= 0 ? "+" : "";
  return <span className={`valence-num ${cls}`}>{sign}{value.toFixed(3)}</span>;
};

const EmotionBadge = ({ emotion }) => {
  return <span className={`emo-badge emo-${emotion}`}>{emotion}</span>;
};

const AuthorChip = ({ author, role }) => (
  <span className="author-chip">
    <span className={`author-dot author-dot--${role}`} />
    {author}
  </span>
);

const TOPIC_STYLES = {
  pedido_entrega:           { bg: "var(--brand-soft)",      fg: "var(--brand)",            label: "Pedido/Entrega" },
  logistica_envio:          { bg: "var(--emo-surprise-bg)", fg: "var(--emo-surprise-fg)",  label: "Logística/Envío" },
  soporte_problema:         { bg: "var(--neg-soft)",        fg: "var(--neg-strong)",       label: "Soporte" },
  producto_consulta:        { bg: "var(--emo-joy-bg)",      fg: "var(--emo-joy-fg)",       label: "Consulta Producto" },
  precio_cotizacion:        { bg: "var(--emo-fear-bg)",     fg: "var(--emo-fear-fg)",      label: "Precio/Cotización" },
  confirmacion_seguimiento: { bg: "var(--pos-soft)",        fg: "var(--pos-strong)",       label: "Seguimiento" },
  pago_facturacion:         { bg: "var(--emo-sadness-bg)",  fg: "var(--emo-sadness-fg)",   label: "Pago/Facturación" },
  promocion_oferta:         { bg: "#fef9c3",                fg: "#854d0e",                 label: "Promoción" },
};

const TopicBadge = ({ topic, style }) => {
  if (!topic) return null;
  const s = TOPIC_STYLES[topic] || { bg: "var(--neu-soft)", fg: "var(--text-muted)", label: topic };
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4,
      background: s.bg, color: s.fg,
      padding: "2px 7px", borderRadius: 999,
      fontSize: 11, fontWeight: 500, whiteSpace: "nowrap",
      ...style,
    }}>
      <span style={{width: 5, height: 5, borderRadius: "50%", background: s.fg, flexShrink: 0}} />
      {s.label}
    </span>
  );
};

// expose
Object.assign(window, { Icon, ValenceBar, ValenceNum, EmotionBadge, AuthorChip, valenceColor, TOPIC_STYLES, TopicBadge });
