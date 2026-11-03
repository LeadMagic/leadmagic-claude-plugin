"""Public-file checks reject credential files without opening their contents."""
import contextlib
import io
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest import mock


SCANNER = Path(__file__).resolve().parents[1] / "scripts" / "check-public-files.py"


class PublicFilesTest(unittest.TestCase):
    def scan(self, files, *, unreadable=()):
        """Run the actual scanner with a supplied file inventory in a temp root."""
        source = SCANNER.read_text()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir).resolve()
            scanner = root / "scripts" / "check-public-files.py"
            scanner.parent.mkdir()
            scanner.write_text(source)
            for name in files:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                # Keep synthetic credential fixtures in memory, never on disk.
                target.touch()

            reads = []

            def read_public_file(file_path):
                name = str(file_path.relative_to(root))
                self.assertNotIn(name, unreadable, "rejected credential file was opened")
                reads.append(name)
                return files[name].encode()

            output = io.StringIO()
            inventory = "\0".join(files).encode() + b"\0"
            with mock.patch("subprocess.check_output", return_value=inventory) as listing:
                with mock.patch.object(Path, "read_bytes", new=read_public_file):
                    with contextlib.redirect_stdout(output):
                        try:
                            runpy.run_path(str(scanner), run_name="__main__")
                            status = 0
                        except SystemExit as error:
                            status = error.code
            self.assertEqual(listing.call_args.kwargs["cwd"], root)
            return status, output.getvalue(), reads

    def test_prohibited_environment_files_are_rejected_without_reading(self):
        secret = "lm_" + "A" * 32
        names = (".env", ".env.production", "nested/.env.local")
        files = {name: secret for name in names}
        files["README.md"] = "Safe public documentation.\n"
        status, output, reads = self.scan(files, unreadable=names)
        self.assertEqual(status, 1)
        for name in names:
            self.assertIn(f"{name}: environment file must not be published", output)
        self.assertNotIn(secret, output)
        self.assertEqual(reads, ["README.md"])

    def test_public_credentials_are_still_detected_without_printing_values(self):
        secret = "lm_" + "B" * 32
        status, output, reads = self.scan({"example.md": f"key={secret}\n"})
        self.assertEqual(status, 1)
        self.assertIn("example.md:1: possible leadmagic-key (value omitted)", output)
        self.assertNotIn(secret, output)
        self.assertEqual(reads, ["example.md"])

    def test_environment_templates_are_still_scanned(self):
        secret = "lm_" + "C" * 32
        names = (".env.example", ".env.sample", ".env.template")
        status, output, reads = self.scan({name: secret for name in names})
        self.assertEqual(status, 1)
        for name in names:
            self.assertIn(f"{name}:1: possible leadmagic-key (value omitted)", output)
        self.assertNotIn("environment file must not be published", output)
        self.assertNotIn(secret, output)
        self.assertEqual(reads, list(names))

    def test_clean_public_files_pass(self):
        status, output, reads = self.scan({"README.md": "Safe public documentation.\n"})
        self.assertEqual(status, 0)
        self.assertIn("Public-file checks passed.", output)
        self.assertEqual(reads, ["README.md"])


if __name__ == "__main__":
    unittest.main()
