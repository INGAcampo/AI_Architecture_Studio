# SECURITY-RECOVERY-001

This system creates verifiable AIAS recovery snapshots with per-file SHA-256 integrity and a caller-keyed HMAC-SHA256 manifest. It excludes secret-bearing filenames, cryptographic key files, symbolic links and detected embedded credentials without logging secret values.

Restoration requires a valid signature and digest set, rejects unsafe member paths and writes only to an empty destination. Automated drills measure recovery duration against RTO. RPO status and retention candidates are reported without destructive automatic deletion.

Signing-key custody remains outside the archive. This release proves integrity, authenticity and recoverability; confidentiality at rest depends on approved encrypted storage or a separately governed cryptographic provider.
