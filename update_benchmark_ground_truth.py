import json
from pathlib import Path

mapping = {
    "AQ-001": "constitution.md",
    "AQ-002": "constitution.md",
    "AQ-003": "SAS-v1.0-Draft.md",
    "AQ-004": "architecture.md",
    "AQ-005": "Testing-Benchmark-Guide-v1.0.md",
    "AQ-006": "architecture.md",
    "AQ-007": "architecture.md",
    "AQ-008": "RIE-Specification-v1.0.md",
    "AQ-009": "RIE-Specification-v1.0.md",
    "AQ-010": "02-RETRIEVAL-MODEL.md",
    "AQ-011": "02-RETRIEVAL-MODEL.md",
    "AQ-012": "RIE-Specification-v1.0.md",
    "AQ-013": "indexing-pipeline.md",
    "AQ-014": "indexing-pipeline.md",
    "AQ-015": "architecture.md",
    "AQ-016": "Testing-Benchmark-Guide-v1.0.md",
    "AQ-017": "04-BENCHMARK-GUIDE.md",
    "AQ-018": "Testing-Benchmark-Guide-v1.0.md",
    "AQ-019": "RIE-Specification-v1.0.md",
    "AQ-020": "RIE-Specification-v1.0.md",
    "AQ-021": "RIE-Specification-v1.0.md",
    "AQ-022": "Testing-Benchmark-Guide-v1.0.md",
    "AQ-023": "Testing-Benchmark-Guide-v1.0.md",
    "AQ-024": "Testing-Benchmark-Guide-v1.0.md",
    "AQ-025": "Athena_Quality_Intelligence_AQI_v1.0.docx",
}

path = Path("benchmarks/athena_core_v1.json")

data = json.loads(path.read_text(encoding="utf-8-sig"))

for item in data:
    item["expected_document_id"] = mapping[item["question_id"]]

path.write_text(
    json.dumps(data, indent=4),
    encoding="utf-8-sig",
)

print("Benchmark ground truth updated.")
