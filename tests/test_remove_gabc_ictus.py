from pathlib import Path
import tempfile
import unittest

from tools.remove_gabc_ictus import (
    GabcFormatError,
    collect_gabc_files,
    remove_vertical_episemata,
)


class RemoveVerticalEpisemataTests(unittest.TestCase):
    def test_removes_apostrophes_only_inside_notation_groups(self) -> None:
        source = (
            "name:Editor's chant;\n"
            "comment:don't alter headers;\n"
            "%%\n"
            "s<sp>'ae</sp>(e') cu(g'_[oh:h]) ('d) lum(gvFE''_). (::)\n"
        )

        result = remove_vertical_episemata(source)

        self.assertEqual(result.removed, 5)
        self.assertEqual(
            result.text,
            (
                "name:Editor's chant;\n"
                "comment:don't alter headers;\n"
                "%%\n"
                "s<sp>'ae</sp>(e) cu(g_[oh:h]) (d) lum(gvFE_). (::)\n"
            ),
        )

    def test_preserves_files_without_vertical_episemata(self) -> None:
        source = "name:Example;\n%%\nExample(c4) text(f). (::)\n"
        result = remove_vertical_episemata(source)
        self.assertEqual(result.removed, 0)
        self.assertEqual(result.text, source)

    def test_requires_header_separator(self) -> None:
        with self.assertRaises(GabcFormatError):
            remove_vertical_episemata("Example(c4) text(f').")

    def test_collects_gabc_files_recursively(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            first = root / "first.gabc"
            second = nested / "second.gabc"
            ignored = nested / "notes.txt"
            first.touch()
            second.touch()
            ignored.touch()

            self.assertEqual(collect_gabc_files([root]), [first, second])


if __name__ == "__main__":
    unittest.main()
