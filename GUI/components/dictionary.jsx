// Product Dictionary — searchable term table from domain_dictionary.csv

const SortTh = ({ label, field, sortKey, sortDir, onSort, style }) => {
  const active = sortKey === field;
  return (
    <th style={{ cursor: "pointer", userSelect: "none", whiteSpace: "nowrap", ...style }}
        onClick={() => onSort(field)}>
      {label}
      <span style={{ marginLeft: 4, opacity: active ? 1 : 0.25, fontSize: 10 }}>
        {active ? (sortDir === 1 ? "▲" : "▼") : "▲"}
      </span>
    </th>
  );
};

const DictionaryView = () => {
  const data = (MOCK.domainDictionary || []);

  const topics = React.useMemo(
    () => [...new Set(data.map(d => d.topicLabel))].sort(),
    [data]
  );

  const [search,      setSearch]      = React.useState("");
  const [filterTopic, setFilterTopic] = React.useState("all");
  const [filterType,  setFilterType]  = React.useState("all");
  const [sortKey,     setSortKey]     = React.useState("rank");
  const [sortDir,     setSortDir]     = React.useState(1);

  const handleSort = React.useCallback(key => {
    if (sortKey === key) setSortDir(d => d * -1);
    else { setSortKey(key); setSortDir(1); }
  }, [sortKey]);

  const filtered = React.useMemo(() => {
    let result = data.filter(d => {
      if (filterTopic !== "all" && d.topicLabel !== filterTopic) return false;
      if (filterType === "uni" && d.isBigram)  return false;
      if (filterType === "bi"  && !d.isBigram) return false;
      if (search && !d.term.toLowerCase().includes(search.toLowerCase())) return false;
      return true;
    });
    return [...result].sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey];
      if (av == null) return 1;
      if (bv == null) return -1;
      return (typeof av === "string" ? av.localeCompare(bv) : av - bv) * sortDir;
    });
  }, [data, search, filterTopic, filterType, sortKey, sortDir]);

  const sharedSort = { sortKey, sortDir, onSort: handleSort };

  return (
    <div>
      <div className="section-head">
        <div>
          <h1>Diccionario de producto</h1>
          <p>{data.length} términos extraídos del corpus · ordenados por relevancia global.</p>
        </div>
      </div>

      <div className="filters">
        <div className="search-input">
          <Icon name="search" size={13} />
          <input placeholder="Buscar término…" value={search}
                 onChange={e => setSearch(e.target.value)} />
        </div>

        <select className="input" value={filterTopic}
                onChange={e => setFilterTopic(e.target.value)}>
          <option value="all">Topic: todos</option>
          {topics.map(t => (
            <option key={t} value={t}>{(TOPIC_STYLES[t] && TOPIC_STYLES[t].label) || t}</option>
          ))}
        </select>

        <select className="input" value={filterType}
                onChange={e => setFilterType(e.target.value)}>
          <option value="all">Tipo: todos</option>
          <option value="uni">Solo unigramas</option>
          <option value="bi">Solo bigramas</option>
        </select>

        <div style={{ marginLeft: "auto", fontSize: 11.5, color: "var(--text-muted)" }}>
          {filtered.length} de {data.length} términos
        </div>
      </div>

      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ overflowX: "auto", maxHeight: "calc(100vh - 260px)", overflowY: "auto" }}>
          <table className="msg-table" style={{ minWidth: 680 }}>
            <thead style={{ position: "sticky", top: 0, zIndex: 1, background: "var(--bg-elev)" }}>
              <tr>
                <SortTh label="#"      field="rank"       style={{ width: 52 }} {...sharedSort} />
                <SortTh label="Término" field="term"                             {...sharedSort} />
                <th>Topic</th>
                <SortTh label="Score"  field="score"      style={{ width: 90 }} {...sharedSort} />
                <SortTh label="Docs"   field="docFreq"    style={{ width: 72 }} {...sharedSort} />
                <SortTh label="% docs" field="docFreqPct" style={{ width: 80 }} {...sharedSort} />
                <th style={{ width: 80 }}>Tipo</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(d => (
                <tr key={d.rank}>
                  <td className="col-time" style={{ color: "var(--text-faint)" }}>{d.rank}</td>
                  <td style={{ fontWeight: 500, fontFamily: "var(--font-mono)", fontSize: 12.5 }}>{d.term}</td>
                  <td><TopicBadge topic={d.topicLabel} /></td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>
                    {typeof d.score === "number" ? d.score.toFixed(2) : "—"}
                  </td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>{d.docFreq}</td>
                  <td>
                    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                      <div style={{
                        height: 4, borderRadius: 2, flexShrink: 0,
                        width: Math.max(4, (d.docFreqPct || 0) * 0.8),
                        background: "var(--brand)", opacity: 0.5,
                      }} />
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>
                        {d.docFreqPct}%
                      </span>
                    </div>
                  </td>
                  <td>
                    <span style={{
                      display: "inline-block", padding: "1px 7px", borderRadius: 999,
                      fontSize: 11, fontWeight: 500,
                      background: d.isBigram ? "var(--emo-fear-bg)" : "var(--neu-soft)",
                      color:      d.isBigram ? "var(--emo-fear-fg)" : "var(--text-muted)",
                    }}>
                      {d.isBigram ? "bigrama" : "unigrama"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

Object.assign(window, { DictionaryView });
