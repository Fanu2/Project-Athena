from athena.ai.llm.runtime_bootstrap import (
    LLMRuntimeBootstrap,
)

runtime = LLMRuntimeBootstrap()

models = runtime.initialize()

print("Available models:")

found = models.models()

print("Count:", len(found))

for model in found:
    print(
        model.name,
        "->",
        model.provider,
    )
