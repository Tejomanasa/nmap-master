# NMAP MASTER - OSINT with Tejo Manasa

Production-oriented full-stack cybersecurity learning simulator for safe, legal Nmap education.

Mandatory disclaimer: **This platform is for educational purposes only. Unauthorized scanning is illegal.**

## Architecture

- **Frontend:** Next.js React app with dark hacker-style dashboard, strict module locks, command builder, terminal-style simulator, XP, badges, and report panel.
- **Backend:** FastAPI service with curriculum APIs, scan simulation, challenge completion, AI-style result explanation, and report generation.
- **Database:** MongoDB via `MONGO_URI` using Motor. If MongoDB is unavailable, the backend uses an in-memory store for local demos.
- **Execution safety:** Commands are parsed and simulated only. Real-world targets, URLs, and unknown IPs are rejected. No Nmap command is executed against the network.
- **Sandbox model:** Docker Compose runs frontend, backend, and MongoDB as isolated services for development.

## Folder Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── curriculum.py      # Modules 1-9 in strict sequence
│   │   ├── main.py            # FastAPI routes
│   │   ├── simulator.py       # Safe Nmap parser and deterministic output engine
│   │   └── store.py           # MongoDB/in-memory progress store
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.jsx
│   │   └── page.jsx
│   ├── components/
│   ├── lib/
│   ├── styles/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Strict Module Sequence

1. Foundations: Nmap intro, installation, legal and ethical rules.
2. Host Discovery: ICMP, ARP, UDP, and TCP ping discovery.
3. Port Scanning: TCP connect, UDP, SYN/half-open, states, SCTP INIT.
4. Scan Types: SYN, TCP connect, FIN, NULL, Xmas.
5. Version Detection: `-sV` and banner grabbing.
6. OS Detection: `-O` fingerprinting.
7. Advanced Scanning: `-A`, NSE scripts, timing templates.
8. Firewall Evasion: fragmentation, decoy, spoofing basics as defensive simulation only.
9. Output & Reporting: normal, XML, grepable output, report generation.

Each module includes concept explanation, real-world use case, UI component design, backend logic, Nmap examples, a simulated lab, and a CTF-style challenge.

## Run Locally

### Docker

```bash
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000/api/health`
- API docs: `http://localhost:8000/docs`

### Manual Development

Backend:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API Summary

- `GET /api/modules` - ordered curriculum with lock/completion state.
- `POST /api/ethics/accept` - accept mandatory legal disclaimer.
- `POST /api/scan` - run a safe simulated Nmap command.
- `POST /api/modules/complete` - submit module challenge flag and unlock the next module.
- `POST /api/report` - generate simulated evidence report.
- `GET /api/targets` - list lab-only targets.

## Safe Lab Targets

- `lab.local`
- `web.lab`
- `firewall.lab`
- `lab-subnet`
- Internal mapped IPs: `192.168.56.10`, `192.168.56.20`, `192.168.56.30`, `192.168.56.0/24`

Any other target is rejected by the backend.

## Example Simulated Commands

```bash
nmap lab.local
nmap -sn lab-subnet
nmap -sT -p 22,80,443 lab.local
nmap -sS firewall.lab
nmap -sV web.lab
nmap -O web.lab
nmap -T3 --script http-title,ssh-hostkey web.lab
nmap -f firewall.lab
nmap -oA tejo-lab lab.local
```

## Challenge Flags

The flags are intentionally stored in the backend curriculum for trainer-led demos. In a production CTF, move challenge validation server-side into hashed or dynamic flag checks.
