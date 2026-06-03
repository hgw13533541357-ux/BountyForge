#!/usr/bin/env python3
"""BountyForge - Automated Bounty Hunter"""
import os, sys, json, time, hashlib, logging, sqlite3
from datetime import datetime
from pathlib import Path
import requests, yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
log = logging.getLogger('BF')

class DB:
  def __init__(self, path='bf.db'):
    self.c = sqlite3.connect(path).cursor()
    self.c.execute('CREATE TABLE IF NOT EXISTS targets (fingerprint TEXT PRIMARY KEY, platform TEXT, title TEXT, bounty REAL, status TEXT DEFAULT "new")')
    self.c.connection.commit()
  def save(self, fp, platform, title, bounty):
    if self.c.execute('SELECT 1 FROM targets WHERE fingerprint=?', (fp,)).fetchone(): return
    self.c.execute('INSERT INTO targets VALUES (?,?,?,?,"new")', (fp, platform, title, bounty))
    self.c.connection.commit()

class PolarScanner:
  def __init__(self, token):
    self.s = requests.Session()
    self.s.headers.update({'Authorization': 'Bearer ' + token})
  def scan(self, limit=50):
    q = 'query { issues(first: ' + str(limit) + ', orderBy: {field: BOUNTY_AMOUNT, direction: DESC}) { nodes { id title url issueNumber bountyAmount } } }'
    try:
      r = self.s.post('https://api.polar.sh/graphql', json={'query': q}, timeout=30)
      if r.status_code == 200:
        return r.json().get('data',{}).get('issues',{}).get('nodes',[])
    except: pass
    return []

def main():
  token = os.environ.get('GITHUB_TOKEN', '')
  db = DB()
  scanner = PolarScanner(token)
  targets = scanner.scan()
  for t in targets:
    fp = hashlib.md5(t['id'].encode()).hexdigest()
    db.save(fp, 'polar', t['title'], float(t.get('bountyAmount',0) or 0))
  Path('output').mkdir(exist_ok=True)
  r = '# BountyForge Report\nGenerated: ' + datetime.now().isoformat()
  r += '\n\nFound ' + str(len(targets)) + ' bounties\n'
  with open('output/report_' + datetime.now().strftime('%Y%m%d') + '.md', 'w') as f: f.write(r)
  log.info(f'Done. {len(targets)} targets')

if __name__ == '__main__': main()