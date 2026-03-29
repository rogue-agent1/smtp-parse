from smtp_parse import parse_email, extract_addresses, build_email, parse_content_type
raw = "From: alice@example.com\nTo: bob@example.com\nSubject: Test\n\nHello World"
e = parse_email(raw)
assert e["headers"]["from"] == "alice@example.com"
assert e["headers"]["subject"] == "Test"
assert e["body"] == "Hello World"
addrs = extract_addresses("To: Alice <alice@x.com>, bob@y.com")
assert "alice@x.com" in addrs and "bob@y.com" in addrs
built = build_email("a@b.com", "c@d.com", "Hi", "Body")
assert "Subject: Hi" in built
mime, params = parse_content_type('text/html; charset="utf-8"')
assert mime == "text/html" and params["charset"] == "utf-8"
print("smtp_parse tests passed")
