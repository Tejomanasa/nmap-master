import { CheckCircle2, Lock, ShieldCheck } from "lucide-react";

export function ProgressRail({ modules, activeId, onSelect }) {
  return (
    <aside className="rail" aria-label="Module progression">
      <div className="brand">
        <ShieldCheck size={26} />
        <div>
          <strong>NMAP MASTER</strong>
          <span>OSINT with Tejo Manasa</span>
        </div>
      </div>
      <nav className="module-nav">
        {modules.map((module) => (
          <button
            key={module.id}
            className={`module-link ${activeId === module.id ? "active" : ""}`}
            onClick={() => !module.locked && onSelect(module.id)}
            disabled={module.locked}
          >
            <span className="module-index">{module.id}</span>
            <span>
              <strong>{module.title}</strong>
              <small>{module.topics.slice(0, 2).join(" • ")}</small>
            </span>
            {module.completed ? <CheckCircle2 size={18} /> : module.locked ? <Lock size={17} /> : null}
          </button>
        ))}
      </nav>
    </aside>
  );
}
