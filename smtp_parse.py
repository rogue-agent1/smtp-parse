#!/usr/bin/env python3
"""smtp_parse: SMTP protocol message parser/builder."""
import sys, re

def build_envelope(sender, recipients, subject, body, headers=None):
    headers = headers or {}
    msg = f"From: {sender}\r\n"
    msg += f"To: {', '.join(recipients)}\r\n"
    msg += f"Subject: {subject}\r\n"
    for k, v in headers.items():
        msg += f"{k}: {v}\r\n"
    msg += f"\r\n{body}"
    return msg

def parse_message(data):
    parts = data.split("\r\n\r\n", 1)
    header_text = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    headers = {}
    current_key = None
    for line in header_text.split("\r\n"):
        if line.startswith((" ", "\t")) and current_key:
            headers[current_key] += " " + line.strip()
        elif ": " in line:
            key, val = line.split(": ", 1)
            current_key = key.lower()
            headers[current_key] = val
    return {"headers": headers, "body": body}

def build_smtp_session(sender, recipients, message):
    commands = []
    commands.append(f"EHLO localhost")
    commands.append(f"MAIL FROM:<{sender}>")
    for r in recipients:
        commands.append(f"RCPT TO:<{r}>")
    commands.append("DATA")
    commands.append(message)
    commands.append(".")
    commands.append("QUIT")
    return commands

def parse_smtp_response(line):
    m = re.match(r'^(\d{3})([ -])(.*)$', line)
    if not m: return None
    return {"code": int(m.group(1)), "continued": m.group(2) == "-", "message": m.group(3)}

def test():
    msg = build_envelope("alice@a.com", ["bob@b.com"], "Hello", "Hi Bob!")
    assert "From: alice@a.com" in msg
    assert "To: bob@b.com" in msg
    assert "Subject: Hello" in msg
    assert "Hi Bob!" in msg
    parsed = parse_message(msg)
    assert parsed["headers"]["from"] == "alice@a.com"
    assert parsed["headers"]["subject"] == "Hello"
    assert parsed["body"] == "Hi Bob!"
    # SMTP session
    cmds = build_smtp_session("alice@a.com", ["bob@b.com"], msg)
    assert cmds[0] == "EHLO localhost"
    assert "MAIL FROM:<alice@a.com>" in cmds
    assert cmds[-1] == "QUIT"
    # Response parsing
    r = parse_smtp_response("250 OK")
    assert r["code"] == 250
    assert not r["continued"]
    r2 = parse_smtp_response("250-PIPELINING")
    assert r2["continued"]
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: smtp_parse.py test")
