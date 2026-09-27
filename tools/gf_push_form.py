#!/usr/bin/env python3
"""Push the notifications and confirmations in gravity/puppy-application.json
to the live Gravity form over the Gravity Forms REST API v2.

The MCP cannot reach Gravity's own tables, so the emails a form sends can only
be written this way (or by hand in Forms > Settings > Notifications).

Credentials come from the environment, never from arguments:

    WP_USER          a WordPress user that can edit forms
    WP_APP_PASSWORD  an application password for that user
                     (Users > Profile > Application Passwords)

Dry run by default: fetches the live form, checks every merge tag in the new
wording against the live field ids, and prints what would change. Nothing is
written until --apply is passed.

    python3 tools/gf_push_form.py                 # dry run against form 7
    python3 tools/gf_push_form.py --apply         # write
    python3 tools/gf_push_form.py --form 8 --site https://example.com

Only `notifications` and `confirmations` are replaced. Fields, settings and
anything Abigail changed in the form editor are read from the live form and
sent back unchanged (GFAPI::update_form needs the whole form in one PUT).
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "..", "gravity", "puppy-application.json")
DEFAULT_SITE = "https://www.pinehillgermanshepherds.com"
DEFAULT_FORM = 7
MERGE_TAG = re.compile(r"\{[^{}:]*:(\d+(?:\.\d+)?)(?::[^{}]*)?\}")


def die(msg, code=1):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


def credentials():
    user = os.environ.get("WP_USER", "").strip()
    pw = os.environ.get("WP_APP_PASSWORD", "").strip()
    if not user or not pw:
        die("WP_USER and WP_APP_PASSWORD must both be set in the environment "
            "(an application password from Users > Profile). Neither is read "
            "from the command line.")
    token = base64.b64encode(f"{user}:{pw}".encode()).decode()
    return {"Authorization": "Basic " + token}


def call(method, url, headers, body=None):
    data = None
    hdrs = dict(headers)
    hdrs["Accept"] = "application/json"
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        hdrs["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        hint = {
            401: "the user or application password was refused",
            403: "the user cannot edit forms, or the REST API is off "
                 "(Forms > Settings > REST API)",
            404: "no form with that id, or the gf/v2 route is not registered",
        }.get(e.code, "")
        die(f"{method} {url} -> HTTP {e.code} {hint}\n{detail}")
    except urllib.error.URLError as e:
        die(f"{method} {url} -> {e.reason} (network policy, DNS or TLS)")


def live_field_ids(form):
    ids = set()
    for f in form.get("fields", []):
        ids.add(str(f.get("id")))
        for i in f.get("inputs") or []:
            ids.add(str(i.get("id")))
    return ids


def merge_tag_ids(obj):
    text = json.dumps(obj, ensure_ascii=False)
    return set(MERGE_TAG.findall(text))


def summary(label, notifications, confirmations):
    print(f"--- {label}")
    for k, n in (notifications or {}).items():
        state = "on " if n.get("isActive", True) else "off"
        print(f"  notification {k} [{state}] {n.get('name')!r}")
        print(f"    to:      {n.get('to')}  (toType={n.get('toType')})")
        print(f"    from:    {n.get('fromName')} <{n.get('from')}>  reply-to {n.get('replyTo')}")
        print(f"    subject: {n.get('subject')}")
        first = (n.get("message") or "").strip().splitlines()[:1]
        print(f"    message: {first[0] if first else ''!r} ...")
    for k, c in (confirmations or {}).items():
        print(f"  confirmation {k} type={c.get('type')} default={c.get('isDefault')}")
        print(f"    message: {(c.get('message') or '')[:100]!r}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--site", default=DEFAULT_SITE)
    ap.add_argument("--form", type=int, default=DEFAULT_FORM)
    ap.add_argument("--source", default=SOURCE,
                    help="Gravity export file whose notifications/confirmations to push")
    ap.add_argument("--apply", action="store_true", help="write to the site")
    args = ap.parse_args()

    with open(args.source, encoding="utf-8") as fh:
        export = json.load(fh)
    src = export["0"] if "0" in export else export[0]
    notifications = src.get("notifications") or {}
    confirmations = src.get("confirmations") or {}
    if not notifications or not confirmations:
        die(f"{args.source} carries no notifications/confirmations")

    headers = credentials()
    base = args.site.rstrip("/") + f"/wp-json/gf/v2/forms/{args.form}"
    live = call("GET", base, headers)
    print(f"live form {args.form}: {live.get('title')!r}, "
          f"{len(live.get('fields', []))} fields")

    # every {Field:ID} the new wording uses must exist on the live form,
    # and each notification's toField must be a live email field
    have = live_field_ids(live)
    want = merge_tag_ids(notifications) | merge_tag_ids(confirmations)
    missing = sorted(want - have, key=lambda s: [int(p) for p in s.split(".")])
    email_ids = {str(f["id"]) for f in live.get("fields", []) if f.get("type") == "email"}
    for k, n in notifications.items():
        if n.get("toType") == "field" and str(n.get("toField")) not in email_ids:
            missing.append(f"{k}.toField={n.get('toField')} (not a live email field)")
    if missing:
        die("merge tags in the new wording do not match the live form: "
            + ", ".join(missing) + "\n(the live form has fields "
            + ", ".join(sorted(have, key=lambda s: [int(p) for p in s.split(".")])) + ")")

    summary("live now", live.get("notifications"), live.get("confirmations"))
    summary("to be written", notifications, confirmations)

    if live.get("notifications") == notifications and live.get("confirmations") == confirmations:
        print("\nnothing to do: live form already matches the file")
        return

    if not args.apply:
        print("\ndry run; pass --apply to write")
        return

    body = dict(live)
    body["notifications"] = notifications
    body["confirmations"] = confirmations
    body["id"] = args.form
    call("PUT", base, headers, body)

    after = call("GET", base, headers)
    ok = (after.get("notifications") == notifications
          and after.get("confirmations") == confirmations)
    if not ok:
        summary("read back", after.get("notifications"), after.get("confirmations"))
        die("written, but the read-back differs from the file")
    print(f"\nwritten and verified on form {args.form}")


if __name__ == "__main__":
    main()
