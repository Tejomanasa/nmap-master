"use client";

import { useEffect, useMemo, useState } from "react";
import { acceptEthics, completeModule, fetchModules, generateReport, runScan } from "../lib/api";
import { Dashboard } from "../components/Dashboard";
import { ModuleContent } from "../components/ModuleContent";
import { ProgressRail } from "../components/ProgressRail";
import { TerminalLab } from "../components/TerminalLab";

export default function Home() {
  const [modules, setModules] = useState([]);
  const [progress, setProgress] = useState(null);
  const [activeId, setActiveId] = useState(1);
  const [command, setCommand] = useState("nmap lab.local");
  const [output, setOutput] = useState("");
  const [assistant, setAssistant] = useState(null);
  const [error, setError] = useState("");
  const [flag, setFlag] = useState("");
  const [completionError, setCompletionError] = useState("");
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  async function refresh() {
    const data = await fetchModules();
    setModules(data.modules);
    setProgress(data.progress);
    const activeStillOpen = data.modules.find((item) => item.id === activeId && !item.locked);
    if (!activeStillOpen) {
      setActiveId(data.modules.find((item) => !item.locked)?.id || 1);
    }
  }

  useEffect(() => {
    refresh().catch((err) => setError(err.message));
  }, []);

  const activeModule = useMemo(
    () => modules.find((module) => module.id === activeId) || modules[0],
    [modules, activeId],
  );

  async function handleAcceptEthics() {
    const data = await acceptEthics();
    setProgress(data.progress);
  }

  async function handleRun() {
    setLoading(true);
    setError("");
    try {
      const data = await runScan(command);
      setOutput(data.simulation.output);
      setAssistant(data.assistant);
      await refresh();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleComplete(moduleId) {
    setCompletionError("");
    try {
      const data = await completeModule(moduleId, flag);
      setProgress(data.progress);
      setFlag("");
      await refresh();
      setActiveId(Math.min(moduleId + 1, modules.length || 9));
    } catch (err) {
      setCompletionError(err.message);
    }
  }

  async function handleReport() {
    setReport(await generateReport());
  }

  return (
    <main className="shell">
      <ProgressRail modules={modules} activeId={activeId} onSelect={setActiveId} />
      <section className="workspace">
        <Dashboard progress={progress || {}} modules={modules.length ? modules : Array(9).fill({})} />
        <div className="hero-strip">
          <div>
            <p className="eyebrow">Safe Cybersecurity Training Platform</p>
            <h1>NMAP MASTER - OSINT with Tejo Manasa</h1>
            <p>This platform is for educational purposes only. Unauthorized scanning is illegal.</p>
          </div>
          <button onClick={handleReport}>Generate Report</button>
        </div>
        {report && (
          <section className="report-panel">
            <strong>{report.title}</strong>
            <span>Evidence items: {report.evidence.length}</span>
            <span>Badges: {report.badges.join(", ") || "None yet"}</span>
          </section>
        )}
        <ModuleContent
          module={activeModule}
          progress={progress}
          onAcceptEthics={handleAcceptEthics}
          onComplete={handleComplete}
          flag={flag}
          setFlag={setFlag}
          completionError={completionError}
        />
        <TerminalLab
          command={command}
          setCommand={setCommand}
          onRun={handleRun}
          output={output}
          assistant={assistant}
          error={error}
          loading={loading}
        />
      </section>
    </main>
  );
}
