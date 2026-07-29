from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_execution_service import ConversationExecutionService
from athena.ai.llm.execution_service import ExecutionService
from athena.ai.llm.runtime_request import RuntimeRequest
from athena.ai.llm.runtime_router import RuntimeRouter
from athena.ai.llm.runtime_bootstrap import LLMRuntimeBootstrap


bootstrap = LLMRuntimeBootstrap()

models = bootstrap.initialize()

router = RuntimeRouter(
    model_manager=models
)

executor = ExecutionService(
    router=router
)

service = ConversationExecutionService(
    executor=executor
)

conversation = Conversation()

result = service.execute(
    conversation,
    "Explain what Project Athena is in one sentence.",
    RuntimeRequest(
        preferred_model="gemma3:4b"
    ),
)

print("MODEL:")
print(result.response.model)

print("\nRESPONSE:")
print(result.response.text)

print("\nCONVERSATION MEMORY:")
for message in conversation.history():
    print(
        message.role,
        ":",
        message.content,
    )
