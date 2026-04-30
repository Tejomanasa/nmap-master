import { BookOpen, Flag, ServerCog, TerminalSquare } from "lucide-react";

export function ModuleContent({ module, progress, onAcceptEthics, onComplete, flag, setFlag, completionError }) {
  if (!module) return null;
  const accepted = progress?.accepted_ethics;

  return (
    <article className="lesson">
      <header className="lesson-header">
        <div>
          <p className="eyebrow">Module {module.id}</p>
          <h1>{module.title}</h1>
        </div>
        <span className={module.completed ? "pill done" : "pill"}>{module.completed ? "Completed" : "Active"}</span>
      </header>

      {module.id === 1 && (
        <div className="disclaimer-panel">
          <strong>This platform is for educational purposes only. Unauthorized scanning is illegal.</strong>
          <button onClick={onAcceptEthics} disabled={accepted}>{accepted ? "Ethics Accepted" : "Accept Ethics"}</button>
        </div>
      )}

      <section className="lesson-grid">
        <div className="lesson-block">
          <BookOpen size={20} />
          <h2>Concept</h2>
          <p>{module.concept}</p>
        </div>
        <div className="lesson-block">
          <ServerCog size={20} />
          <h2>Real-World Use Case</h2>
          <p>{module.real_world_use_case}</p>
        </div>
        <div className="lesson-block">
          <TerminalSquare size={20} />
          <h2>Implementation Design</h2>
          <p>{module.ui_component_design}</p>
          <p>{module.backend_logic}</p>
        </div>
      </section>

      <section className="commands">
        <h2>Example Commands</h2>
        <div className="command-list">
          {module.commands.map((command) => (
            <code key={command}>{command}</code>
          ))}
        </div>
      </section>

      <section className="lab-panel">
        <div>
          <p className="eyebrow">Simulated Lab</p>
          <h2>{module.lab.title}</h2>
          <p>{module.lab.goal}</p>
          <code>{module.lab.starter_command}</code>
        </div>
        <div>
          <p className="eyebrow">Expected Findings</p>
          {module.lab.expected_findings.map((finding) => (
            <span className="finding" key={finding}>{finding}</span>
          ))}
        </div>
      </section>

      <section className="challenge">
        <Flag size={20} />
        <div>
          <h2>{module.challenge.title}</h2>
          <p>{module.challenge.prompt}</p>
          <div className="flag-row">
            <input value={flag} onChange={(event) => setFlag(event.target.value)} placeholder="TEJO{...}" />
            <button onClick={() => onComplete(module.id)}>Submit Flag</button>
          </div>
          {completionError && <p className="error-text">{completionError}</p>}
        </div>
      </section>
    </article>
  );
}
