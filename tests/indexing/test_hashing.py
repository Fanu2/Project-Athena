from athena.indexing.hashing import sha256_file


def test_same_file_same_hash(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Athena")

    hash1 = sha256_file(file_path)
    hash2 = sha256_file(file_path)

    assert hash1 == hash2


def test_different_files_different_hash(tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("Athena")
    file2.write_text("Research")

    assert sha256_file(file1) != sha256_file(file2)
