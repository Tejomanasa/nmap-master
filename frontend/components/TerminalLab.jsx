import { Bot, Play, ShieldAlert } from "lucide-react";

const TARGETS = ["lab.local", "web.lab", "firewall.lab", "lab-subnet"];
const SCAN_TYPES = [
  { label: "Default", value: "" },
  { label: "Host Discovery", value: "-sn" },
  { label: "TCP Connect", value: "-sT" },
  { label: "SYN", value: "-sS" },
  { label: "UDP", value: "-sU" },
  { label: "Version", value: "-sV" },
  { label: "OS", value: "-O" },
  { label: "Aggressive", value: "-A" },
  { label: "Safe NSE", value: "--script http-title,ssh-hostkey" },
  { label: "Fragmentation Lab", value: "-f" },
  { label: "Report Bundle", value: "-oA tejo-lab" },
];

export function TerminalLab({ command, setCommand, onRun, output, assistant, error, loading }) {
  function buildCommand(scanType, target) {
    const middle = scanType ? `${scanType} ` : "";
    setCommand(`nmap ${middle}${target}`);
  }

  return (
    <section className="terminal-zone">
      <div className="builder">
        <div>
          <p className="eyebrow">Command Builder</p>
          <h2>Safe Lab Targets Only</h2>
        </div>
        <div className="builder-grid">
          {SCAN_TYPES.map((scan) => (
            <button key={scan.label} onClick={() => buildCommand(scan.value, "lab.local")}>{scan.label}</button>
          ))}
        </div>
        <div className="target-row">
          {TARGETS.map((target) => (
            <button key={target} onClick={() => buildCommand("", target)}>{target}</button>
          ))}
        </div>
      </div>

      <div className="terminal">
        <div className="terminal-top">
          <span></span><span></span><span></span>
          <strong>simulated-nmap</strong>
        </div>
        <div className="terminal-input">
          <span>$</span>
          <input value={command} onChange={(event) => setCommand(event.target.value)} />
          <button onClick={onRun} disabled={loading}>
            <Play size={16} />
            {loading ? "Running" : "Run"}
          </button>
        </div>
        <pre>{output || "Run a simulated command to see real-time style output here."}</pre>
        {error && (
          <div className="terminal-alert">
            <ShieldAlert size={18} />
            <span>{error}</span>
          </div>
        )}
      </div>

      <div className="assistant">
        <Bot size={21} />
        <h2>AI Scan Assistant</h2>
        <p>{assistant?.summary || "I will explain results, identify likely meaning, and suggest authorized next steps after each simulated scan."}</p>
        <div>
          {(assistant?.next_steps || []).map((step) => (
            <span key={step}>{step}</span>
          ))}
        </div>
      </div>
    </section>
  );
}
