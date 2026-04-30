from __future__ import annotations

import re
import shlex
from datetime import datetime, timezone
from typing import Any

from .curriculum import DISCLAIMER, LAB_TARGETS, MODULES

ALLOWED_TARGETS = set(LAB_TARGETS.keys()) | {
    "192.168.56.10",
    "192.168.56.20",
    "192.168.56.30",
    "192.168.56.0/24",
}

FLAG_MODULE_MAP = {
    "-sn": 2,
    "-PR": 2,
    "-PU": 2,
    "-PS": 2,
    "-sT": 3,
    "-sU": 3,
    "-sY": 3,
    "-sS": 4,
    "-sF": 4,
    "-sN": 4,
    "-sX": 4,
    "-sV": 5,
    "-O": 6,
    "-A": 7,
    "--script": 7,
    "-f": 8,
    "-D": 8,
    "-S": 8,
    "-oN": 9,
    "-oX": 9,
    "-oG": 9,
    "-oA": 9,
}


class SimulationError(ValueError):
    pass


def _normalize_target(token: str) -> str | None:
    if token in LAB_TARGETS:
        return token
    ip_map = {data["ip"]: name for name, data in LAB_TARGETS.items() if "ip" in data}
    return ip_map.get(token)


def parse_command(command: str) -> dict[str, Any]:
    try:
        tokens = shlex.split(command)
    except ValueError as exc:
        raise SimulationError("Command could not be parsed. Check quotes and spacing.") from exc

    if not tokens or tokens[0] != "nmap":
        raise SimulationError("Only simulated nmap commands are supported.")

    if re.search(r"https?://", command):
        raise SimulationError("URLs are blocked. Use lab.local, web.lab, firewall.lab, or lab-subnet.")
    for token in tokens:
        if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}(/24)?", token) and token not in ALLOWED_TARGETS:
            raise SimulationError("Real-world targets are blocked. Use lab.local, web.lab, firewall.lab, or lab-subnet.")

    flags: list[str] = []
    target = "lab.local"
    skip_next_for = {"-p", "-oN", "-oX", "-oG", "-oA", "--script", "-D", "-S"}
    iterator = iter(enumerate(tokens[1:], start=1))
    for _, token in iterator:
        if token.startswith("-"):
            base = token.split("=")[0]
            for known in FLAG_MODULE_MAP:
                if base.startswith(known) and known not in {"-S"}:
                    base = known
                    break
            flags.append(base)
            if base in skip_next_for and "=" not in token:
                next(iterator, None)
            continue
        normalized = _normalize_target(token)
        if normalized:
            target = normalized
        elif token not in {"default,safe", "http-title,ssh-hostkey"}:
            raise SimulationError("Unknown target. This lab only permits simulated targets.")

    module_id = max([FLAG_MODULE_MAP.get(flag, 1) for flag in flags] or [1])
    return {"tokens": tokens, "flags": flags, "target": target, "module_id": module_id}


def required_module_for_command(command: str) -> int:
    return parse_command(command)["module_id"]


def simulate_nmap(command: str) -> dict[str, Any]:
    parsed = parse_command(command)
    target_name = parsed["target"]
    target = LAB_TARGETS[target_name]
    flags = parsed["flags"]

    if "-f" in flags or "-D" in flags or "-S" in flags:
        output = [
            f"Starting Nmap simulated evasion lab at {datetime.now(timezone.utc).isoformat()}",
            f"Nmap scan report for {target_name} ({target['ip']})",
            "IDS alert: fragmented probe" if "-f" in flags else "IDS alert: decoy-like traffic pattern",
            "Firewall policy: packet reassembly enabled",
            "Note: evasion commands are simulated and never executed.",
        ]
        findings = ["Defensive alert triggered", "Use only in authorized labs"]
    elif target_name == "lab-subnet" or "-sn" in flags or "-PR" in flags or "-PU" in flags or "-PS" in flags:
        output = [
            "Starting Nmap host discovery simulation",
            "Nmap scan report for 192.168.56.10",
            "Host is up (0.0010s latency).",
            "Nmap scan report for 192.168.56.20",
            "Host is up (0.0014s latency).",
            "Nmap scan report for 192.168.56.30",
            "Host is up; ICMP blocked, TCP probe responded.",
            "Nmap done: 256 IP addresses (3 hosts up) scanned.",
        ]
        findings = ["3 live hosts", "firewall.lab ignores ICMP but responds to TCP ping"]
    else:
        output = [
            f"Starting Nmap simulation for {target_name} ({target['ip']})",
            f"Nmap scan report for {target_name} ({target['ip']})",
            "Host is up (0.0012s latency).",
            "PORT       STATE     SERVICE       VERSION",
        ]
        for port, detail in target.get("ports", {}).items():
            version = detail["version"] if ("-sV" in flags or "-A" in flags) and detail["version"] else ""
            output.append(f"{port:<10} {detail['state']:<9} {detail['service']:<13} {version}".rstrip())
        findings = [f"{port} {d['state']} {d['service']}" for port, d in target.get("ports", {}).items()]

        if "-O" in flags or "-A" in flags:
            output.extend(["OS details: Linux 5.x", "OS detection confidence: 92%"])
            findings.append(f"Likely OS: {target['os']}")
        if "--script" in flags or "-A" in flags:
            output.extend([
                "| http-title: Tejo Training Portal",
                "| ssh-hostkey: simulated fingerprint SHA256:TEJO...",
            ])
            findings.append("Safe script output collected")
        if any(flag in flags for flag in ["-sF", "-sN", "-sX"]):
            output.append("Unusual TCP flag scan result: several ports open|filtered")
            findings.append("open|filtered result observed")
        if any(flag in flags for flag in ["-oN", "-oX", "-oG", "-oA"]):
            output.extend(["Normal output generated", "XML output generated", "Grepable output generated"])
            findings.append("Report evidence generated")

    return {
        "command": command,
        "target": target_name,
        "module_id": parsed["module_id"],
        "output": "\n".join(output),
        "findings": findings,
        "disclaimer": DISCLAIMER,
    }


def explain_results(simulation: dict[str, Any]) -> dict[str, Any]:
    findings = simulation.get("findings", [])
    next_steps = [
        "Confirm the scope and authorization before any deeper testing.",
        "Prioritize open services for version detection in the simulated lab.",
        "Document filtered ports as firewall-controlled exposure.",
    ]
    if simulation["module_id"] >= 5:
        next_steps.append("Map service versions to patch guidance and configuration hardening.")
    if simulation["module_id"] >= 9:
        next_steps.append("Convert evidence into a concise report with risk and remediation.")
    return {
        "summary": f"Simulated scan completed against {simulation['target']} with {len(findings)} notable observations.",
        "findings": findings,
        "next_steps": next_steps,
        "ethics": DISCLAIMER,
    }


def module_by_id(module_id: int) -> dict[str, Any]:
    for module in MODULES:
        if module["id"] == module_id:
            return module
    raise SimulationError("Module not found.")
