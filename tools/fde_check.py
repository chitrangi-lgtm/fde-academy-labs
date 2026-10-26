"""Check a mission or Python lab from this kit on your own machine.

    python tools/fde_check.py m05          one mission (missions/m05) or lab (pylabs/m01-py1)
    python tools/fde_check.py --list       everything, with your current score
    python tools/fde_check.py --all        check everything (GitHub Actions runs this on every push)

Each check is one of the client's acceptance criteria, evaluated against your code's end state, exactly as on the course site.
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER = r'''
import json, sys, warnings
warnings.filterwarnings("ignore")
cfg = json.load(open("check.json"))
code = open(cfg["code_file"], encoding="utf-8").read().replace("from provided import *", "")
pre = open(cfg["preamble_file"], encoding="utf-8").read() if cfg.get("preamble_file") else ""
ns = {"__name__": "__main__"}
exec("import os as _os, sys as _sys, json as _json", ns)
if cfg.get("setup_first"):
    exec(cfg["setup"], ns)
exec(pre, ns)
error = None
try:
    exec(compile(code, cfg["code_file"], "exec"), ns)
except Exception as exc:
    error = f"{type(exc).__name__}: {exc}"
if not cfg.get("setup_first") and error is None:
    exec(cfg["setup"], ns)
results = []
for name, expr in cfg["checks"]:
    if error:
        results.append([name, False, "your code stopped with an error"])
        continue
    try:
        results.append([name, bool(eval(expr, ns)), ""])
    except Exception as exc:
        results.append([name, False, f"{type(exc).__name__}: {exc}"])
print("@@RESULT@@" + json.dumps({"error": error, "results": results}))
'''


def folders():
    out = []
    for group in ("missions", "pylabs"):
        base = os.path.join(ROOT, group)
        if os.path.isdir(base):
            out += [(name, os.path.join(base, name)) for name in sorted(os.listdir(base)) if os.path.exists(os.path.join(base, name, "check.json"))]
    return out


def check(folder, quiet=False):
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    try:
        p = subprocess.run([sys.executable, "-c", RUNNER], cwd=folder, capture_output=True, text=True, timeout=60, env=env)
    except subprocess.TimeoutExpired:
        return 0, 1, "your code ran for more than 60 seconds"
    line = next((l for l in p.stdout.splitlines() if l.startswith("@@RESULT@@")), None)
    if line is None:
        return 0, 1, (p.stderr or p.stdout)[-800:]
    data = json.loads(line[len("@@RESULT@@"):])
    if not quiet:
        out = p.stdout.split("@@RESULT@@")[0].strip()
        if out:
            print(out[-3000:], end="\n\n")
        if data["error"]:
            print("Your code stopped with an error:", data["error"], end="\n\n")
        for name, ok, err in data["results"]:
            print(("PASS " if ok else "FAIL ") + name + (f"  ({err})" if err and not data["error"] else ""))
    passed = sum(1 for _, ok, _ in data["results"] if ok)
    return passed, len(data["results"]), data["error"]


def main(args):
    items = folders()
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] in ("--list", "--all"):
        lines, total_done = [], 0
        for name, folder in items:
            passed, total, _ = check(folder, quiet=True)
            done = passed == total
            total_done += done
            lines.append(f"{'DONE' if done else '    '} {name:10} {passed}/{total}  {json.load(open(os.path.join(folder, 'check.json')))['title']}")
        print("\n".join(lines))
        print(f"\n{total_done} of {len(items)} complete")
        summary = os.getenv("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as f:
                f.write(f"## FDE Academy labs: {total_done} of {len(items)} complete\n\n```\n" + "\n".join(lines) + "\n```\n")
        return 0
    match = dict(items).get(args[0])
    if not match:
        print(f"No mission or lab called {args[0]!r}. Try: python tools/fde_check.py --list")
        return 2
    passed, total, _ = check(match)
    score = round(passed / total * 100) if total else 0
    print(f"\n{passed} of {total} criteria met: {score} / 100" + ("  Complete!" if passed == total else ""))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
