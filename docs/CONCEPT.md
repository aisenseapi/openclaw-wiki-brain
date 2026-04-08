# Wiki Brain Concept

## The Problem

AI assistants have **no persistent memory** across sessions:

- Each conversation starts blank
- System knowledge must be relearned every time
- History, patterns, and context are lost
- Can't learn from past problems

## The Solution

**Give the AI a file it can read and write.**

Simple idea, powerful result:

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Human      │◄────►│   DokuWiki   │◄────►│  OpenClaw    │
│   (Web UI)   │      │  (Files)     │      │  (File Read) │
└──────────────┘      └──────────────┘      └──────────────┘
```

## Core Principles

### 1. Files Over Database

- Text files are **human-readable**
- Text files are **git-compatible** 
- Text files are **fast to read**
- Text files **survive forever**

### 2. Structure Over Chaos

Standard pages every Wiki Brain should have:

| Page | Purpose | Updated |
|------|---------|---------|
| `system/docker` | Live container status | Auto |
| `system/resources` | CPU/RAM/Disk history | Auto |
| `diary/YYYY-MM-DD` | Daily events | Auto/Manual |
| `relations` | Service dependencies | Manual |
| `incidents` | Problem history | Manual |
| `decisions` | Architecture choices | Manual |

### 3. Relations Over Isolation

Don't just list services. Map connections:

```
Home Assistant
├── Requires: Mosquitto (MQTT)
├── Requires: PostgreSQL (database)
├── Uses: ESPHome
└── Used by: Dashboard, Mobile App
```

This lets the AI answer: *"What breaks if I restart X?"*

## How OpenClaw Uses It

### Pattern: Read Before Answer

```python
# User asks: "Should I restart Home Assistant?"

# 1. Read relations
deps = wiki.get_page("relations")
# → HA depends on MQTT, PostgreSQL

# 2. Read recent diary
diary = wiki.get_page("diary/2026-04-08")
# → Last restart: OK at 09:00

# 3. Read resources
resources = wiki.get_page("system/resources")
# → System normal

# Answer: "Yes, but check PostgreSQL first. 
#          Last restart went fine."
```

### Pattern: Write After Action

```python
# After completing any significant task

wiki.put_page(
    "diary/2026-04-08",
    "**14:30** - Restarted Home Assistant\n"
    "**14:35** - All services recovered\n",
    append=True
)
```

## Format Standards

### Tables for Data

```text
^ Container ^ Status ^ Ports ^
| dokuwiki | Up 3h | 8080→80 |
```

### Timestamps for Events

```text
**14:30** - Event description
```

### Headers for Structure

```text
===== Section =====
```

## Security Considerations

- **Never store secrets in wiki** (passwords, API keys)
- **Use environment variables** for sensitive data
- **Back up regularly** - files can be corrupted
- **Version control** - track changes with git

## Scaling

### Home User (You)
- Pages: 10-20
- Update: Hourly
- Backup: Daily

### DevOps Team
- Pages: 50-100
- Update: Every 5 minutes
- Backup: Hourly

### Enterprise
- Pages: 500+
- Update: Real-time via webhooks
- Backup: Continuous

## The Philosophy

**Your AI should know your systems as well as you do.**

Not by magic. By reading what you wrote.

Not by guessing. By seeing the history.

Not by forgetting. By writing it down.

---

*Simple tools. Powerful results.*