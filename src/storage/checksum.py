import hashlib,json
def canonical_json_bytes(data): return json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def calculate_checksum(data): return hashlib.sha256(canonical_json_bytes(data)).hexdigest()
def verify_checksum(data,expected_checksum): return calculate_checksum(data)==expected_checksum
