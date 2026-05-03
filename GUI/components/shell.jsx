// Sidebar navigation
const Sidebar = ({ active, onNavigate, counts }) => {
  const items = [
    { id: "upload",   icon: "upload",    label: "Importar chats" },
    { id: "dashboard",icon: "dashboard", label: "Dashboard" },
    { id: "explorer", icon: "chat",      label: "Conversaciones", count: counts.conversations },
    { id: "client",   icon: "user",      label: "Clientes",       count: counts.clients },
    { id: "authors",  icon: "spark",     label: "Sentimiento",    count: counts.authors },
  ];
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <div className="sidebar__logo">EO</div>
        <div className="sidebar__brand-text">
          <span className="sidebar__brand-name">Comercios Unidos</span>
          <span className="sidebar__brand-sub">Insights · v0.4</span>
        </div>
      </div>

      <div className="nav-group-label">Espacio de trabajo</div>
      {items.map(it => (
        <button key={it.id} className={`nav-item ${active === it.id ? "is-active" : ""}`} onClick={() => onNavigate(it.id)}>
          <Icon name={it.icon} className="nav-item__icon" />
          <span>{it.label}</span>
          {it.count != null && <span className="nav-item__count">{it.count}</span>}
        </button>
      ))}

      <div className="nav-group-label">Análisis</div>
      <button className={`nav-item ${active === "dictionary" ? "is-active" : ""}`}
              onClick={() => onNavigate("dictionary")}>
        <Icon name="package" className="nav-item__icon" />
        <span>Diccionario producto</span>
      </button>
      <button className="nav-item">
        <Icon name="building" className="nav-item__icon" />
        <span>Comparar vendedoras</span>
      </button>

      <div className="sidebar__footer">
        <div className="avatar">JM</div>
        <div>
          <div className="sidebar__user-name">Juan Mendoza</div>
          <div className="sidebar__user-role">Analista comercial</div>
        </div>
      </div>
    </aside>
  );
};

const Topbar = ({ crumbs, actions }) => (
  <div className="topbar">
    {crumbs.map((c, i) => (
      <React.Fragment key={i}>
        <span className={i === crumbs.length - 1 ? "topbar__title" : "topbar__crumb"}>{c}</span>
        {i < crumbs.length - 1 && <span className="topbar__crumb-sep">/</span>}
      </React.Fragment>
    ))}
    <div className="topbar__actions">{actions}</div>
  </div>
);

Object.assign(window, { Sidebar, Topbar });
