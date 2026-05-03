// Upload screen — drag & drop ZIP with simulated processing pipeline
const UploadView = ({ onComplete }) => {
  const [stage, setStage] = React.useState("idle"); // idle | uploading | processing | done
  const [progress, setProgress] = React.useState(0);
  const [pipelineStep, setPipelineStep] = React.useState(0);
  const [dragOver, setDragOver] = React.useState(false);
  const [file, setFile] = React.useState(null);

  const pipeline = [
    { label: "Extrayendo archivos del .zip", count: "12 chats" },
    { label: "Anonimización de teléfonos y nombres", count: "1,284 entidades" },
    { label: "Tokenización y normalización", count: "4,286 mensajes" },
    { label: "Reconocimiento de productos del catálogo", count: "342 menciones" },
    { label: "Modelo de sentimiento (BETO en español)", count: "4,286 scores" },
    { label: "Vinculación con etiquetas de compra", count: "184 conversaciones" },
  ];

  const startProcess = (f) => {
    setFile(f || { name: "chats_t1_t2_2026Q1.zip", size: "18.4 MB" });
    setStage("uploading");
    setProgress(0);
    let p = 0;
    const upInt = setInterval(() => {
      p += Math.random() * 14 + 6;
      if (p >= 100) {
        p = 100;
        setProgress(100);
        clearInterval(upInt);
        setStage("processing");
        let s = 0;
        const procInt = setInterval(() => {
          s += 1;
          setPipelineStep(s);
          if (s >= pipeline.length) {
            clearInterval(procInt);
            setStage("done");
          }
        }, 700);
      } else {
        setProgress(p);
      }
    }, 180);
  };

  const onDrop = (e) => {
    e.preventDefault(); setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f) startProcess({ name: f.name, size: (f.size / 1024 / 1024).toFixed(1) + " MB" });
  };

  return (
    <div className="upload-shell">
      <div className="section-head">
        <div>
          <h1>Importar conversaciones</h1>
          <p>Sube el .zip exportado desde WhatsApp Business. Se procesa local y los datos sensibles se anonimizan antes de almacenar.</p>
        </div>
      </div>

      {stage === "idle" && (
        <div
          className={`dropzone ${dragOver ? "is-dragover" : ""}`}
          onDragOver={e => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={onDrop}
        >
          <div className="dropzone__icon"><Icon name="upload" size={22} /></div>
          <h3 className="dropzone__title">Arrastra el archivo .zip aquí</h3>
          <p className="dropzone__sub">Acepta exportaciones de WhatsApp Business · hasta 500 MB · ambas oficinas</p>
          <button className="btn btn--primary" onClick={() => startProcess()}>
            <Icon name="folder" size={14} /> Seleccionar archivo
          </button>
          <div className="dropzone__or">o conecta una fuente</div>
          <div style={{display: "flex", gap: 8, justifyContent: "center"}}>
            <button className="btn btn--sm">📁 Carpeta T1 (Polanco)</button>
            <button className="btn btn--sm">📁 Carpeta T2 (Anzures)</button>
          </div>
        </div>
      )}

      {(stage === "uploading" || stage === "processing" || stage === "done") && (
        <div className="upload-progress">
          <div className="upload-row">
            <div className="upload-row__icon"><Icon name="file" size={16} /></div>
            <div className="upload-row__name">{file?.name}</div>
            <div className="upload-row__size">{file?.size}</div>
            {stage === "done" && <span className="emo-badge emo-joy">listo</span>}
          </div>
          {stage === "uploading" && (
            <>
              <div className="progress-bar"><div className="progress-bar__fill" style={{width: `${progress}%`}} /></div>
              <div style={{fontSize: 11.5, color: "var(--text-muted)", marginTop: 6}}>Subiendo… {Math.floor(progress)}%</div>
            </>
          )}

          {(stage === "processing" || stage === "done") && (
            <div className="pipeline">
              {pipeline.map((step, i) => {
                const status = i < pipelineStep ? "done" : i === pipelineStep ? "active" : "pending";
                return (
                  <div key={i} className={`pipeline-step pipeline-step--${status}`}>
                    <div className="pipeline-step__check">
                      {status === "done" && <Icon name="check" size={10} />}
                      {status === "active" && <span style={{fontSize: 9}}>●</span>}
                    </div>
                    <span className="pipeline-step__label">{step.label}</span>
                    {status !== "pending" && <span className="pipeline-step__count">{step.count}</span>}
                  </div>
                );
              })}
            </div>
          )}

          {stage === "done" && (
            <div style={{display: "flex", gap: 8, marginTop: 16, justifyContent: "flex-end"}}>
              <button className="btn">Ver corpus</button>
              <button className="btn btn--primary" onClick={() => onComplete && onComplete()}>
                Abrir dashboard <Icon name="chevron" size={12} />
              </button>
            </div>
          )}
        </div>
      )}

      <div style={{marginTop: 24, fontSize: 11.5, color: "var(--text-faint)", textAlign: "center"}}>
        Procesamiento ejecutado localmente · sin envío a servidores externos · cumple lineamientos LFPDPPP
      </div>
    </div>
  );
};

Object.assign(window, { UploadView });
