# BountyForge

**Automated Bounty Hunter Weapon System**

A + B + C full pipeline for automated bounty hunting.

## Features
- **A**: Multi-platform bounty scraper (Polar.sh, Gitcoin)
- **B**: Smart ranking + skill matching
- **C**: Vulnerability scanner + PoC generator

## Quick Start
```bash
pip install -r requirements.txt
python bountyforge.py all
```

## Commands
| Command | Action |
|---------|--------|
| `python bountyforge.py scan` | Scan all platforms |
| `python bountyforge.py all` | Full pipeline |
| `python bountyforge.py watch` | Continuous monitoring |

## Automated Runs
GitHub Actions runs every 6 hours automatically.
Reports are saved as artifacts.

Built with love by LO & ENI