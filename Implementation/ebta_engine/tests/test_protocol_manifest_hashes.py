import hashlib
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST = REPO_ROOT / "Protocole" / "MANIFESTE DE GEL EBTA.md"


class ProtocolManifestHashTests(unittest.TestCase):
    def test_frozen_protocol_hashes_still_match(self):
        text = MANIFEST.read_text(encoding="utf-8")
        rows = re.findall(r"\| `([^`]+)` \| `([A-F0-9]{64})` \|", text)
        self.assertGreater(len(rows), 10)
        mismatches = []
        for relative_path, expected in rows:
            path = REPO_ROOT / "Protocole" / relative_path
            actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
            if actual != expected:
                mismatches.append(relative_path)
        self.assertEqual(mismatches, [])


if __name__ == "__main__":
    unittest.main()
