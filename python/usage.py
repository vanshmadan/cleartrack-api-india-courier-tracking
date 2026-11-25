"""Show your plan and how many lookups are left.

Usage: python usage.py
"""
from cleartrack import ClearTrack

u = ClearTrack().usage()
print(f"Plan   : {u['plan']} ({u['status']})")
print(f"Period : {u['period_lookups_used']} / {u['period_lookups_limit']} lookups, ends {u.get('period_end') or '-'}")
print(f"Today  : {u['daily_used']} / {u['daily_limit']}")
