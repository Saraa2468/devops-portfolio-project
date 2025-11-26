#!/usr/bin/env python3
# Simple script to check health endpoint and print status
import requests
import sys

URL = "http://localhost:5000/health"

try:
    r = requests.get(URL, timeout=3)
    if r.status_code == 200:
        print("OK:", r.json())
        sys.exit(0)
    else:
        print("UNHEALTHY:", r.status_code)
        sys.exit(2)
except Exception as e:
    print("ERROR:", e)
    sys.exit(1)
