from pathlib import Path

from athena.core.application_context import ApplicationContext

workspace = Path(
    r"C:\Users\singh\Videos\AthenaBenchmarkWorkspace"
)

source = Path(
    r"C:\Users\singh\Documents\Project-Athena\docs\architecture"
)

context = ApplicationContext()

context.open_workspace(workspace)

imported = context.document_service.import_folder(source)

print("Imported documents:")
for item in imported:
    print(item)

print()
print(f"Total imported: {len(imported)}")