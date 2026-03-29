#!/usr/bin/env python3
"""Email/MIME parser (simplified). Zero dependencies."""
import re

def parse_email(raw):
    parts = raw.split("\n\n", 1)
    header_text = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    headers = {}
    current_key = None
    for line in header_text.split("\n"):
        if line and line[0] in " \t" and current_key:
            headers[current_key] += " " + line.strip()
        elif ":" in line:
            key, val = line.split(":", 1)
            current_key = key.strip().lower()
            headers[current_key] = val.strip()
    return {"headers": headers, "body": body.strip()}

def extract_addresses(header_val):
    pattern = r'[\w.+-]+@[\w.-]+'
    return re.findall(pattern, header_val)

def build_email(from_addr, to_addr, subject, body, headers=None):
    lines = [f"From: {from_addr}", f"To: {to_addr}", f"Subject: {subject}"]
    if headers:
        for k,v in headers.items(): lines.append(f"{k}: {v}")
    lines.append(""); lines.append(body)
    return "\n".join(lines)

def parse_content_type(ct):
    parts = ct.split(";")
    mime = parts[0].strip()
    params = {}
    for p in parts[1:]:
        if "=" in p:
            k, v = p.strip().split("=", 1)
            params[k.strip()] = v.strip().strip('"')
    return mime, params

if __name__ == "__main__":
    email = build_email("a@b.com", "c@d.com", "Test", "Hello!")
    print(email)
