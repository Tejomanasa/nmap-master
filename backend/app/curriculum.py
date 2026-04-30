DISCLAIMER = "This platform is for educational purposes only. Unauthorized scanning is illegal."

MODULES = [
    {
        "id": 1,
        "slug": "foundations",
        "title": "Foundations",
        "topics": ["Introduction to Nmap", "Installation", "Legal & ethical guidelines"],
        "concept": (
            "Nmap is a network mapper used to discover hosts, services, versions, and "
            "network exposure. In a professional workflow it supports asset discovery, "
            "attack-surface validation, and defensive verification. All activity in this "
            "platform is simulated against private lab targets only."
        ),
        "real_world_use_case": (
            "A security team inventories an internal lab subnet after a change window to "
            "confirm only approved systems are visible."
        ),
        "ui_component_design": (
            "Foundation lesson view with ethics acknowledgement, install checklist, "
            "read-only command examples, and a disabled terminal until the disclaimer is accepted."
        ),
        "backend_logic": (
            "API stores disclaimer acknowledgement, returns module metadata, and denies all "
            "scan simulation requests until Module 1 is complete."
        ),
        "commands": [
            "nmap --version",
            "nmap -h",
            "nmap 192.168.56.10",
        ],
        "lab": {
            "title": "Verify the Toolkit",
            "target": "lab.local",
            "goal": "Confirm the simulated Nmap environment is available and identify the default scan behavior.",
            "starter_command": "nmap lab.local",
            "expected_findings": ["Host is up", "22/tcp open ssh", "80/tcp open http"],
        },
        "challenge": {
            "title": "Ethics Gate",
            "prompt": "Accept the legal disclaimer and run the safest default scan against lab.local.",
            "answer_flags": ["TEJO{LEGAL_FIRST}"],
            "xp": 100,
            "badge": "Ethical Operator",
        },
    },
    {
        "id": 2,
        "slug": "host-discovery",
        "title": "Host Discovery",
        "topics": ["ICMP Ping Scan", "ARP ping Scan", "UDP ping scan", "TCP ping scan"],
        "concept": (
            "Host discovery identifies live systems before deeper scanning. ICMP checks echo replies, "
            "ARP discovery works well on local networks, UDP probes can reveal hosts that block ping, "
            "and TCP ping uses SYN or ACK probes to infer liveness."
        ),
        "real_world_use_case": (
            "Before an internal assessment, a tester maps which lab machines are online so scanning time "
            "is focused on reachable systems."
        ),
        "ui_component_design": (
            "Host discovery command builder with selectable probe type, simulated subnet selector, "
            "live-host table, and terminal output stream."
        ),
        "backend_logic": (
            "Simulation API accepts only approved lab hosts and discovery flags, then returns deterministic "
            "online/offline host results."
        ),
        "commands": [
            "nmap -sn 192.168.56.0/24",
            "nmap -PR -sn 192.168.56.0/24",
            "nmap -PU53,161 -sn 192.168.56.0/24",
            "nmap -PS22,80,443 -sn 192.168.56.0/24",
        ],
        "lab": {
            "title": "Find Live Hosts",
            "target": "lab-subnet",
            "goal": "Use TCP ping to identify live hosts in the simulated lab subnet.",
            "starter_command": "nmap -PS22,80,443 -sn lab-subnet",
            "expected_findings": ["192.168.56.10 is up", "192.168.56.20 is up"],
        },
        "challenge": {
            "title": "Silent Neighbor",
            "prompt": "Identify the host that ignores ICMP but responds to TCP ping.",
            "answer_flags": ["TEJO{TCP_PING_FOUND_IT}"],
            "xp": 150,
            "badge": "Host Hunter",
        },
    },
    {
        "id": 3,
        "slug": "port-scanning",
        "title": "Port Scanning",
        "topics": ["TCP connect/full open scan", "UDP scanning", "Half open scan", "Open, Closed, Filtered ports", "SCTP INIT scan"],
        "concept": (
            "Port scanning determines which network services are reachable. Open ports accept connections, "
            "closed ports reject them, and filtered ports are blocked or silently dropped. TCP connect scans "
            "complete a handshake, SYN scans infer state from partial handshakes, UDP scans rely on responses "
            "or ICMP errors, and SCTP INIT scans target SCTP services."
        ),
        "real_world_use_case": (
            "A penetration tester validates whether a staging server exposes only SSH and HTTPS before release."
        ),
        "ui_component_design": (
            "Port matrix with state colors, protocol toggles, scan-type selector, and expandable explanations "
            "for open, closed, and filtered states."
        ),
        "backend_logic": (
            "Backend maps safe lab targets to predefined TCP, UDP, and SCTP port states and blocks arbitrary hosts."
        ),
        "commands": [
            "nmap -sT -p 22,80,443 lab.local",
            "nmap -sS -p 1-1000 lab.local",
            "nmap -sU -p 53,67,123 lab.local",
            "nmap -sY -p 2905 lab.local",
        ],
        "lab": {
            "title": "Read Port States",
            "target": "lab.local",
            "goal": "Run TCP, UDP, and SCTP simulations and classify open, closed, and filtered ports.",
            "starter_command": "nmap -sT -p 22,80,443 lab.local",
            "expected_findings": ["22/tcp open ssh", "443/tcp filtered https", "53/udp open domain"],
        },
        "challenge": {
            "title": "Filtered Door",
            "prompt": "Find the filtered HTTPS port on lab.local.",
            "answer_flags": ["TEJO{443_FILTERED}"],
            "xp": 175,
            "badge": "Port Cartographer",
        },
    },
    {
        "id": 4,
        "slug": "scan-types",
        "title": "Scan Types",
        "topics": ["SYN Scan (-sS)", "TCP Connect (-sT)", "FIN, NULL, Xmas scans"],
        "concept": (
            "Different scan types change how packets interact with target TCP stacks. SYN scans are fast and "
            "do not complete the handshake. TCP connect scans use the operating system connection API. FIN, "
            "NULL, and Xmas scans send unusual flag combinations to infer filtering behavior, but results vary "
            "by OS and firewall."
        ),
        "real_world_use_case": (
            "A tester compares scan types against a firewall lab to understand what logging and filtering reveal."
        ),
        "ui_component_design": (
            "Packet-flag visualizer with scan-type tabs, packet timeline, and terminal output side panel."
        ),
        "backend_logic": (
            "API returns simulated packet narratives and scan output based on selected scan flags."
        ),
        "commands": [
            "nmap -sS lab.local",
            "nmap -sT lab.local",
            "nmap -sF lab.local",
            "nmap -sN lab.local",
            "nmap -sX lab.local",
        ],
        "lab": {
            "title": "Compare TCP Behaviors",
            "target": "firewall.lab",
            "goal": "Compare SYN, Connect, FIN, NULL, and Xmas results against the same simulated host.",
            "starter_command": "nmap -sS firewall.lab",
            "expected_findings": ["SYN scan reports 80/tcp open", "Xmas scan reports ports as open|filtered"],
        },
        "challenge": {
            "title": "Flag Logic",
            "prompt": "Use a Xmas scan to produce an open|filtered result on firewall.lab.",
            "answer_flags": ["TEJO{XMAS_OPEN_FILTERED}"],
            "xp": 200,
            "badge": "Packet Thinker",
        },
    },
    {
        "id": 5,
        "slug": "version-detection",
        "title": "Version Detection",
        "topics": ["Service detection (-sV)", "Banner grabbing"],
        "concept": (
            "Version detection probes open ports to identify service names, software versions, and sometimes "
            "application metadata. Banner grabbing is the simpler act of reading service-provided text, while "
            "Nmap service detection uses many protocol probes."
        ),
        "real_world_use_case": (
            "A blue team checks whether an exposed web service still advertises an outdated server banner."
        ),
        "ui_component_design": (
            "Service fingerprint table with confidence labels, banner preview, and next-step recommendations."
        ),
        "backend_logic": (
            "Backend enriches open simulated ports with service/version data and returns safe remediation hints."
        ),
        "commands": [
            "nmap -sV lab.local",
            "nmap -sV --version-light lab.local",
            "nmap -sV --version-all -p 22,80 lab.local",
        ],
        "lab": {
            "title": "Identify Services",
            "target": "web.lab",
            "goal": "Run service detection and identify the web and SSH versions.",
            "starter_command": "nmap -sV web.lab",
            "expected_findings": ["OpenSSH 8.9", "nginx 1.24"],
        },
        "challenge": {
            "title": "Banner Match",
            "prompt": "Find the service banner that identifies nginx 1.24.",
            "answer_flags": ["TEJO{NGINX_124_BANNER}"],
            "xp": 225,
            "badge": "Banner Reader",
        },
    },
    {
        "id": 6,
        "slug": "os-detection",
        "title": "OS Detection",
        "topics": ["OS fingerprinting (-O)"],
        "concept": (
            "OS detection compares network responses, TCP options, IP behavior, and timing traits against "
            "known fingerprints. It is probabilistic and works best when at least one open and one closed port "
            "are visible."
        ),
        "real_world_use_case": (
            "During network hardening, defenders validate that externally visible systems do not leak excessive "
            "fingerprinting detail."
        ),
        "ui_component_design": (
            "OS fingerprint card with confidence meter, required-port checklist, and explanatory packet clues."
        ),
        "backend_logic": (
            "API returns simulated OS matches and confidence scores only for lab targets with adequate port data."
        ),
        "commands": [
            "nmap -O lab.local",
            "nmap -O --osscan-guess lab.local",
            "nmap -O -p 22,80,443 lab.local",
        ],
        "lab": {
            "title": "Fingerprint the Host",
            "target": "web.lab",
            "goal": "Run OS detection and explain why confidence is not always 100%.",
            "starter_command": "nmap -O web.lab",
            "expected_findings": ["Linux 5.x", "OS details confidence 92%"],
        },
        "challenge": {
            "title": "Probable Platform",
            "prompt": "Identify the likely OS family for web.lab.",
            "answer_flags": ["TEJO{LINUX_FINGERPRINT}"],
            "xp": 250,
            "badge": "OS Profiler",
        },
    },
    {
        "id": 7,
        "slug": "advanced-scanning",
        "title": "Advanced Scanning",
        "topics": ["Aggressive scan (-A)", "NSE scripts", "Timing templates"],
        "concept": (
            "Advanced scanning combines multiple techniques. Aggressive mode enables version detection, OS "
            "detection, traceroute, and default NSE scripts. NSE scripts automate safe checks when selected "
            "carefully. Timing templates tune speed and reliability."
        ),
        "real_world_use_case": (
            "A tester uses default safe scripts in a lab to gather web titles and SSH host key details for a report."
        ),
        "ui_component_design": (
            "Advanced scan composer with script category selector, timing slider, risk hints, and report preview."
        ),
        "backend_logic": (
            "Backend accepts a whitelist of safe NSE-style simulations and timing templates T0-T5, then returns "
            "script output and caution notes."
        ),
        "commands": [
            "nmap -A lab.local",
            "nmap --script default,safe lab.local",
            "nmap -T3 -sV lab.local",
            "nmap -T4 --script http-title web.lab",
        ],
        "lab": {
            "title": "Compose an Advanced Scan",
            "target": "web.lab",
            "goal": "Use safe scripts and a moderate timing template to collect service context.",
            "starter_command": "nmap -T3 --script http-title,ssh-hostkey web.lab",
            "expected_findings": ["http-title: Tejo Training Portal", "ssh-hostkey: simulated fingerprint"],
        },
        "challenge": {
            "title": "Scripted Clue",
            "prompt": "Use a safe NSE script to reveal the web title.",
            "answer_flags": ["TEJO{HTTP_TITLE_FOUND}"],
            "xp": 275,
            "badge": "Script Specialist",
        },
    },
    {
        "id": 8,
        "slug": "firewall-evasion",
        "title": "Firewall Evasion",
        "topics": ["Fragmentation (-f)", "Decoy scan (-D)", "Spoofing basics"],
        "concept": (
            "Firewall evasion techniques are sensitive and must be used only in authorized labs. Fragmentation "
            "splits packets, decoys add noise to source attribution, and spoofing changes apparent packet source "
            "details. This platform teaches defensive understanding with non-executable simulations only."
        ),
        "real_world_use_case": (
            "A security engineer tests whether monitoring rules detect suspicious fragmented or decoy-like traffic "
            "inside a controlled training range."
        ),
        "ui_component_design": (
            "Evasion lab simulator with defensive framing, technique cards, monitoring alerts, and blocked real-scan controls."
        ),
        "backend_logic": (
            "API never executes evasion commands; it returns simulated packet and detection outcomes for lab-only targets."
        ),
        "commands": [
            "nmap -f firewall.lab",
            "nmap -D RND:5 firewall.lab",
            "nmap -S 192.168.56.50 firewall.lab",
        ],
        "lab": {
            "title": "Defensive Evasion Awareness",
            "target": "firewall.lab",
            "goal": "Observe how simulated controls log fragmentation and decoy behavior.",
            "starter_command": "nmap -f firewall.lab",
            "expected_findings": ["IDS alert: fragmented probe", "Firewall policy: packet reassembly enabled"],
        },
        "challenge": {
            "title": "Alert Correlator",
            "prompt": "Trigger the simulated fragmented-probe alert and identify the defensive control.",
            "answer_flags": ["TEJO{REASSEMBLY_DETECTED}"],
            "xp": 300,
            "badge": "Firewall Analyst",
        },
    },
    {
        "id": 9,
        "slug": "output-reporting",
        "title": "Output & Reporting",
        "topics": ["Normal output", "XML output", "Grepable output", "Report generation"],
        "concept": (
            "Nmap can produce human-readable normal output, XML for structured tooling, and legacy grepable "
            "output for quick text processing. Professional reports translate scan evidence into scope, findings, "
            "risk, and recommended remediation."
        ),
        "real_world_use_case": (
            "After an authorized lab assessment, the tester exports XML and produces a concise executive and "
            "technical report."
        ),
        "ui_component_design": (
            "Report builder with output format tabs, evidence picker, executive summary field, and downloadable JSON report."
        ),
        "backend_logic": (
            "Backend stores simulated scan history, converts selected evidence into report JSON, and calculates final score."
        ),
        "commands": [
            "nmap -oN scan.txt lab.local",
            "nmap -oX scan.xml lab.local",
            "nmap -oG scan.gnmap lab.local",
            "nmap -oA tejo-lab lab.local",
        ],
        "lab": {
            "title": "Produce the Report",
            "target": "lab.local",
            "goal": "Generate normal, XML, and grepable simulated outputs, then summarize key findings.",
            "starter_command": "nmap -oA tejo-lab lab.local",
            "expected_findings": ["Normal output generated", "XML output generated", "Report ready"],
        },
        "challenge": {
            "title": "Final Evidence Pack",
            "prompt": "Create a complete report bundle for lab.local.",
            "answer_flags": ["TEJO{REPORT_COMPLETE}"],
            "xp": 350,
            "badge": "Recon Reporter",
        },
    },
]

LAB_TARGETS = {
    "lab.local": {
        "ip": "192.168.56.10",
        "os": "Linux 5.x",
        "ports": {
            "22/tcp": {"state": "open", "service": "ssh", "version": "OpenSSH 8.9"},
            "80/tcp": {"state": "open", "service": "http", "version": "nginx 1.24"},
            "443/tcp": {"state": "filtered", "service": "https", "version": ""},
            "53/udp": {"state": "open", "service": "domain", "version": "CoreDNS simulated"},
            "2905/sctp": {"state": "closed", "service": "m3ua", "version": ""},
        },
    },
    "web.lab": {
        "ip": "192.168.56.20",
        "os": "Linux 5.x",
        "ports": {
            "22/tcp": {"state": "open", "service": "ssh", "version": "OpenSSH 8.9"},
            "80/tcp": {"state": "open", "service": "http", "version": "nginx 1.24"},
            "8080/tcp": {"state": "open", "service": "http-proxy", "version": "FastAPI training app"},
        },
    },
    "firewall.lab": {
        "ip": "192.168.56.30",
        "os": "Network firewall appliance",
        "ports": {
            "22/tcp": {"state": "filtered", "service": "ssh", "version": ""},
            "80/tcp": {"state": "open", "service": "http", "version": "admin banner hidden"},
            "443/tcp": {"state": "filtered", "service": "https", "version": ""},
        },
    },
    "lab-subnet": {
        "ip": "192.168.56.0/24",
        "hosts": ["192.168.56.10", "192.168.56.20", "192.168.56.30"],
    },
}

BADGES_BY_LEVEL = {
    1: "Ethics Cadet",
    2: "Recon Apprentice",
    3: "Scan Operator",
    4: "Nmap Master",
}
