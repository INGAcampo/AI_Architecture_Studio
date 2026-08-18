# Sprint L3 Production BIM 004BV
## Safe Offline Exchange Backends — SketchUp + GEO5

### Context
004BU proved that neither SketchUp nor GEO5 is detected on the local machine:
no executable, uninstall product, automation registration, or running process evidence.

### Scope
004BV adds additive AIAS-side safe offline staging backends for both targets. These
backends do not attempt to launch vendor software and do not write proprietary vendor
project formats.

### Safety model
- no COM/vendor API calls;
- no process launch;
- no network access;
- no `.skp` generation;
- no GEO5 proprietary project-format generation;
- neutral artifacts are copied byte-for-byte and SHA-256 verified;
- every bundle carries a JSON manifest with explicit safety flags;
- vendor-runtime verification remains false;
- compatibility certification remains false until tested with an installed vendor version.

### Repository gap vs vendor-runtime gap
After 004BV passes, AIAS has a repository implementation for safe offline exchange
staging. This closes the repository implementation gap only. Live vendor runtime
integration remains explicitly deferred because 004BU proved the applications are not
installed on this machine.

### Accepted staging extensions
The extension allowlists are staging policy only. They do not assert that a particular
vendor version can import every listed format. Vendor compatibility must be separately
verified when the relevant application is installed.

### Global regression
Not run by this installer. It remains reserved for final Macrotranche 004 certification
after all source modifications are complete.
