#!/usr/bin/env python3
"""Apply queued web-form claims (ntfy topic) to the sign-up sheets.

Runs inside the scheduled GitHub Action. Claims are applied in strict
arrival order (ntfy server timestamp, then message id). processed.json
records handled message ids so replays are impossible. A student who
already holds a slot on a sheet is skipped (one slot per student per
sheet, and it also absorbs double-clicks).
"""
import json, re, sys, urllib.request

TOPIC = "https://ntfy.sh/plsc508-fa26-e8ddb68250d6d5bab956"
SHEETS = {"methods": "METHODS.md", "readings": "READINGS.md"}

def main():
    with urllib.request.urlopen(TOPIC + "/json?poll=1&since=all", timeout=30) as r:
        lines = r.read().decode().split("\n")
    done = set(json.load(open("processed.json"))["processed"])
    claims = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
            if ev.get("event") != "message" or ev["id"] in done:
                continue
            c = json.loads(ev["message"])
            if c.get("type") in SHEETS and c.get("week") and c.get("name"):
                claims.append((ev["time"], ev["id"], c))
        except (ValueError, KeyError):
            continue
    claims.sort(key=lambda t: (t[0], t[1]))
    changed = False
    log = []
    for _, mid, c in claims:
        done.add(mid)
        path = SHEETS[c["type"]]
        name = re.sub(r"[|\n\r]", " ", c["name"]).strip()[:80]
        reading = re.sub(r"[|\n\r]", " ", c.get("reading", "")).strip()[:120]
        if not name or (c["type"] == "readings" and not reading):
            log.append(f"skip {mid}: incomplete claim")
            continue
        entry = name + (" — " + reading if c["type"] == "readings" else "")
        lines = open(path).read().split("\n")
        found = applied = already = False
        for i, line in enumerate(lines):
            if not line.startswith(f"| {c['week']} "):
                continue
            found = True
            cells = line.split("|")
            sheet_txt = open(path).read()
            if re.search(r"^\|.*\| *" + re.escape(name) + r"(?: \(| —|\s*\|)", sheet_txt, re.M):
                already = True
                break
            if cells[3].strip() == "OPEN":
                cells[3] = f" {entry} "
            elif cells[4].strip() == "OPEN":
                cells[4] = f" {entry} "
            else:
                break
            lines[i] = "|".join(cells)
            applied = True
            break
        if applied:
            open(path, "w").write("\n".join(lines))
            changed = True
            log.append(f"applied {mid}: {c['week']} {c['type']} -> {name}")
        elif already:
            log.append(f"skip {mid}: {name} already holds a slot on {path}")
        elif found:
            log.append(f"skip {mid}: {c['week']} {c['type']} full")
        else:
            log.append(f"skip {mid}: week {c['week']} not on {path}")
    json.dump({"processed": sorted(done)}, open("processed.json", "w"), indent=1)
    print("\n".join(log) if log else "no new claims")
    print("CHANGED" if (changed or claims) else "NOCHANGE")

if __name__ == "__main__":
    main()
