from pathlib import Path

from athena.core.application_context import ApplicationContext
from athena.domain.ai.question import Question

workspace = Path(
    r"C:\Users\singh\Videos\AthenaBenchmarkWorkspace"
)

context = ApplicationContext()
context.open_workspace(workspace)

results = context.retrieval_service.retrieve(
    Question(text="What is the Athena Constitution?")
)

for r in results:
    print("DOCUMENT:", r.document_name)
    print("ID:", r.document_id)
    print("SCORE:", r.score)
    print("TEXT:", r.text[:200])
    print("-" * 60)