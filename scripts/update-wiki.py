#!/usr/bin/env python3
"""
Wiki Automation - Update DokuWiki with live system data.
Run this hourly via cron.
"""

import subprocess
from datetime import datetime
from pathlib import Path
import os

# Configuration
WIKI_DIR = os.environ.get('WIKI_DIR', '/home/user/dokuwiki/data/pages')

def run_cmd(cmd):
    """Run shell command, return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip()
    except:
        return ""

def update_docker_page():
    """Update Docker containers page."""
    output = run_cmd('docker ps --format "{{.Names}}|{{.Image}}|{{.Status}}|{{.Ports}}"')
    
    content = f"====== Docker Containers - {datetime.now().strftime('%Y-%m-%d %H:%M')} ======\n\n"
    content += "^ Container ^ Image ^ Status ^ Ports ^\n"
    
    count = 0
    for line in output.split('\n'):
        if line and '|' in line:
            parts = line.split('|')
            status_icon = "✅" if "Up" in parts[2] else "❌"
            content += f"| {status_icon} **{parts[0]}** | {parts[1]} | {parts[2]} | {parts[3]} |\n"
            count += 1
    
    content += f"\n**Total:** {count} containers\n"
    
    page_file = Path(WIKI_DIR) / "system" / "docker.txt"
    page_file.parent.mkdir(parents=True, exist_ok=True)
    page_file.write_text(content)
    return count

def update_resources_page():
    """Update system resources page."""
    # Get disk usage
    disk = run_cmd("df -h / | tail -1 | awk '{print $5}'")
    
    # Get memory
    mem = run_cmd("free -h | grep Mem | awk '{print $3 \"/\" $2}'")
    
    content = f"====== System Resources - {datetime.now().strftime('%Y-%m-%d %H:%M')} ======\n\n"
    content += "^ Resource ^ Current ^\n"
    content += f"| Disk Usage | {disk} |\n"
    content += f"| Memory | {mem} |\n"
    
    page_file = Path(WIKI_DIR) / "system" / "resources.txt"
    page_file.parent.mkdir(parents=True, exist_ok=True)
    page_file.write_text(content)

def main():
    """Main update routine."""
    print("=== Wiki Automation ===")
    
    Path(WIKI_DIR).mkdir(parents=True, exist_ok=True)
    
    print("\n1. Updating Docker...")
    count = update_docker_page()
    print(f"   ✓ {count} containers")
    
    print("\n2. Updating Resources...")
    update_resources_page()
    print("   ✓ Resources logged")
    
    print(f"\n=== Done at {datetime.now().strftime('%H:%M:%S')} ===")

if __name__ == "__main__":
    main()