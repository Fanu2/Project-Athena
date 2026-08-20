# Chapter 9

# Service Architecture

## Purpose

Athena services provide the implementation boundaries for application capabilities.

Services contain domain orchestration and application workflows while preserving modularity, testability, and replaceable implementations.

Capability contracts describe existing services and do not replace them.

## Service Layers

Athena services are organized by responsibility.

## AI Services

Location:

src/athena/application/ai/

Responsibilities:

- AI provider integration
- retrieval orchestration
- evidence handling
- citation support

## Retrieval Service

Service:

application.ai.retrieval_service.RetrievalService

Purpose:

Retrieve relevant workspace knowledge and supporting evidence.

Inputs:

- Question

Outputs:

- RetrievalResult
- EvidenceRecord

Consumers:

- AssistantRetrievalAdapter
- Workspace intelligence workflows

Supports:

- retrieval scoring
- ranking metadata
- evidence retrieval
- citation workflows

## Citation Services

Services:

- CitationService
- CitationValidationService
- CitationExplanationService

Purpose:

Provide source attribution, citation validation, and explanation support.

Supports:

- evidence-backed responses
- source verification
- citation quality checks

## Assistant Services

Location:

src/athena/application/assistant/

Responsibilities:

- request understanding
- capability routing
- workflow planning
- validation
- controlled execution boundaries

Key components:

- AssistantEngine
- CapabilityRegistry
- ActionRegistry
- AssistantPlanner
- Quality Validation

## Workspace Services

Service:

AssistantWorkspaceService

Purpose:

Coordinate assistant workflows with workspace context.

Provides:

- workspace awareness
- session recovery
- planning context

## Capability Mapping

Athena capabilities are implemented through existing services.

Capability contracts are descriptive only.

They define:

- purpose
- service boundary
- inputs
- outputs
- evidence requirements
- validation requirements

They do not introduce a separate execution framework.

## Initial Capability Map

| Capability | Service Boundary | Evidence Support |
|---|---|---|
| Retrieval | RetrievalService | Yes |
| Citation | CitationService | Yes |
| Workspace Intelligence | AssistantWorkspaceService | Context based |
| AI Provider | AIService | Model dependent |
| Document Viewing | DocumentViewerService | Source based |
| Conversation | ConversationQueryService | Session based |

## Architectural Rule

New capabilities should extend existing service boundaries.

Future capability contracts must build on existing Athena services rather than creating parallel frameworks.

The service layer remains the implementation boundary.

The Assistant layer consumes capabilities through controlled interfaces.