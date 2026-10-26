# Engineering evidence index

Each record keeps its original source, environment and verification scope. These
are development/qualification records, not scientific admission or project Evidence.

| Record | Scope |
| --- | --- |
| [release_0_1_1.json](release_0_1_1.json) | Normalized accepted source/tag identity, original package hashes, 19 native jobs, 17 JUnit reports, provider identities, coverage and retention owner/trigger. |
| [release_0_1_1_receipts.json.gz](release_0_1_1_receipts.json.gz) | 73 original public qualification records, including installed receipts, dependency closures, JUnit XML, coverage mapping and full native run captures. Package binaries are retained separately under #9. |
| [diagnostics_13_20261022.json](diagnostics_13_20261022.json) and [its Conda closure](diagnostics_13_20261022_conda.json.gz) | Dated diagnostic-bootstrap/scoped-advice receiving under Praxis #13. |
| [latest_public_cohort_receiving_2026-10-20.json](latest_public_cohort_receiving_2026-10-20.json) | Historical earlier support-provider receiving under #10; preserve its original scope rather than treating it as new-cohort acceptance. |
| [Earlier development receipt](../verification.json) | Historical 0.1.0.dev0 checkpoint; not current release acceptance. |

The 0.1.1 compressed bundle is gzip-compressed JSON. Each entry in `files` carries
a relative `path`, decoded-content SHA-256, explicit `encoding` (`utf-8` or
`base64`) and `content`. Decode the content before checking its checksum; the
normalized receipt also records the entire compressed bundle checksum. Native
capture manifests and archived log ZIPs retain the GH Run Receptor evidence.

For example, inspect the member inventory without writing files:

```python
import gzip
import json
from pathlib import Path

bundle = json.loads(
    gzip.decompress(Path("devguide/evidence/release_0_1_1_receipts.json.gz").read_bytes())
)
print([item["path"] for item in bundle["files"]])
```

The [release record](../releases/0.1.1.md) explains acceptance, publication limits
and retention. The [pause checkpoint](../CHECKPOINT.md) identifies remaining work.
