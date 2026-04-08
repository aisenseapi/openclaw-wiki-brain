# 🧠 OpenClaw Wiki Brain

> Give your AI assistant a long-term memory

A file-based wiki system that creates a "second brain" for OpenClaw AI assistants.
Combines automated system logging, manual documentation, and relationship graphs
so your AI remembers everything, predicts problems, and gives context-rich answers.

---

## What is this?

**Before (standard AI):**
- ❌ Forgotten after the conversation
- ❌ No context about your system
- ❌ Can't learn from history

**After (with Wiki Brain):**
- ✅ Remembers everything from day one
- ✅ Knows every detail about your systems
- ✅ Predicts problems before they happen
- ✅ Gives data-driven recommendations

---

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/aisenseapi/openclaw-wiki-brain.git
cd openclaw-wiki-brain

# 2. Start DokuWiki
docker compose up -d
# Available at http://localhost:8080

# 3. Copy automation scripts
cp scripts/*.py ~/dokuwiki/scripts/

# 4. Run first update
python3 ~/dokuwiki/scripts/update-wiki.py

# 5. Set up cron (runs every hour)
echo "0 * * * * python3 ~/dokuwiki/scripts/update-wiki.py" | crontab -
```

---

## How It Works

```
┌─────────────────────────────────────────┐
│         OpenClaw AI Assistant          │
│         (You are here)                   │
└─────────────────┬─────────────────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                         │
    ▼                         ▼
┌─────────────┐        ┌─────────────┐
│ File-based  │        │  XML-RPC    │
│ (fast read) │        │  (metadata) │
└──────┬──────┘        └──────┬──────┘
       │                      │
       └──────────┬───────────┘
                  ▼
       ┌──────────────────────┐
       │    DokuWiki          │
       │    (Port 8080)       │
       └──────────────────────┘
```

**Key insight:** OpenClaw reads directly from files for speed, while humans use the web UI.
Both see the same data.

---

## Wiki Structure

```
dokuwiki/data/pages/
├── start.txt                    # Landing page
├── system/
│   ├── docker.txt              # Live containers
│   ├── resources.txt           # CPU/RAM/Disk history
│   ├── network.txt             # Ports & connections
│   └── services.txt            # Service health
├── homeassistant/
│   └── entities.txt            # HA entity counts
├── diary/
│   └── 2026-04-08.txt         # Daily events
├── relations.txt              # Dependency graph
├── decisions.txt              # Architecture choices
└── incidents.txt              # Problem history
```

---

## Usage Patterns

### Pattern 1: Context Before Action

**You:** "Should I restart Home Assistant?"

**OpenClaw:**
1. Reads `relations.txt` → HA depends on MQTT & PostgreSQL
2. Reads `diary/2026-04-08.txt` → Last restart: OK at 09:00
3. Reads `system/resources.txt` → Resources normal
4. **Answer:** "Yes, but check PostgreSQL first. Last restart went fine (09:00 today)."

### Pattern 2: Prediction

**OpenClaw:** *"Based on 30 days of disk data: you're using 0.5%/day.
At 21% now → full in ~158 days. Consider monitoring backup space."*

### Pattern 3: Historical Learning

**You:** "What went wrong last time?"

**OpenClaw:** Searches `incidents.txt`, finds similar problem,
explains solution and current status.

---

## File Formats

### System Data (Table format)

```text
====== Docker - 2026-04-08 11:58 ======

^ Container ^ Image ^ Status ^ Ports ^
| dokuwiki | linuxserver/dokuwiki:latest | Up 3h | 8080→80 |
| homeassistant | ghcr.io/home-assistant | Up 26h | 8123 |
```

### Diary (Chronological)

```text
====== Diary 2026-04-08 ======

**09:00** - Full test OK
**11:30** - Wiki automation set up
**16:42** - All pages complete
```

### Relations (Hierarchy)

```text
====== Relations ======

Spark
├── Docker
│   ├── Home Assistant
│   │   └── Mosquitto (MQTT)
│   └── DokuWiki
└── Databases
    └── PostgreSQL
```

---

## Scripts Included

| Script | Purpose |
|--------|---------|
| `update-wiki.py` | Main automation - runs hourly |
| `wiki-client.py` | OpenClaw integration (XML-RPC + file fallback) |
| `wiki-search.py` | Search across all pages |
| `wiki-show.py` | Display a specific page |
| `wiki-list.py` | List all pages |
| `fulltest-to-wiki.py` | Log test results |

---

## OpenClaw Commands

Add these to your `COMMANDS.md`:

```markdown
### Wiki Commands

**!wiki-search <query>** - Search wiki content
**!wiki-show <page>** - Display page content  
**!wiki-list** - List all pages
**!wiki-update** - Force update now
```

---

## Why DokuWiki?

| Feature | Benefit |
|---------|---------|
| **File-based** | No database, simple backups |
| **Fast** | Direct file reads for OpenClaw |
| **Portable** | Copy files = move wiki |
| **Versioned** | Git-compatible |
| **Searchable** | Built-in search + AI search |
| **No plugins needed** | Simple, maintainable |

---

## Backup

```bash
# Automated backup script
./scripts/backup-wiki.sh

# Or manually
cp -r dokuwiki/data/pages ~/wiki-backup/$(date +%Y-%m-%d)
```

**Recommended:** Daily backup via cron at 2 AM.

---

## Real-World Examples

See `examples/` directory for:
- Home lab setup (Docker + Home Assistant)
- DevOps team (K8s + CI/CD)
- Small business (Servers + network)

---

## Contributing

This is a pattern, not a product. Adapt it to your needs:

1. Fork the repo
2. Add your own automation scripts
3. Share what works

---

## License

MIT - Share freely, give credit.

---

**Made with ❤️ for better AI memory**  
*Created by [aisenseapi](https://github.com/aisenseapi) using OpenClaw*