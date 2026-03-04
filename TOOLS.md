# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Current Setup

### Discord
- Target channel: general
- Channel ID: 1468628478420324375

### Canvas
- Access domain: https://openclaw.lazycat1012.heiyu.space
- Canvas path: /__openclaw__/canvas/

### Environment
- Working directory: /home/node/clawd
- Configuration directory: /home/node/.openclaw
- Runtime: Docker container with root access

### Memory
- Daily notes: memory/YYYY-MM-DD.md
- Long-term: MEMORY.md

### Security Notes
- **API Tokens**: Never push sensitive tokens to public repositories
- **GitHub Protection**: GitHub automatically detects and blocks secrets in pushes
- **Environment Variables**: Sensitive data should be kept in .env files (excluded from git)
- **Git Ignore**: Always maintain .gitignore to protect sensitive files