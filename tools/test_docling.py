from pathlib import Path
from time import perf_counter
import sys

from docling.document_converter import DocumentConverter


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:")
        print(r"python tools\test_docling.py <pdf-file>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1]).expanduser().resolve()

    if not pdf_path.exists():
        print(f"File not found:\n{pdf_path}")
        sys.exit(1)

    print(f"Input file : {pdf_path}")
    print("Initializing Docling...")

    converter = DocumentConverter()

    print("Converting document...")
    start = perf_counter()

    try:
        result = converter.convert(pdf_path)
    except Exception as exc:
        print(f"\nConversion failed:\n{exc}")
        sys.exit(1)

    elapsed = perf_counter() - start

    print(f"\nConversion completed in {elapsed:.2f} seconds")

    markdown = result.document.export_to_markdown()

    print("\n" + "=" * 80)
    print("MARKDOWN PREVIEW")
    print("=" * 80)
    print(markdown[:3000])

    print("\n" + "=" * 80)
    print("DOCUMENT STATISTICS")
    print("=" * 80)
    print(f"Markdown length : {len(markdown):,} characters")

    print("\n" + "=" * 80)
    print("RESULT OBJECT TYPE")
    print("=" * 80)
    print(type(result))

    print("\n" + "=" * 80)
    print("DOCUMENT OBJECT TYPE")
    print("=" * 80)
    print(type(result.document))

    print("\n" + "=" * 80)
    print("DOCUMENT ATTRIBUTES")
    print("=" * 80)
    print(dir(result.document))


if __name__ == "__main__":
    main()