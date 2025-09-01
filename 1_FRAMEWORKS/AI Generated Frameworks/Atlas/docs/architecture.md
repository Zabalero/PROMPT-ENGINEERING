# Atlas Architecture

The Atlas framework is a modular system designed for clarity, extensibility, and robust performance. It consists of several core components that work in concert to provide a complete agentic coding environment.

```mermaid
flowchart TD
    subgraph User Interaction Layer
        A[IDE Integration]
    end

    subgraph Cognitive Core
        B[Workflow Engine]
        C[Cognitive Model]
    end

    subgraph Knowledge & Task Management
        D[The Nexus (Memory System)]
        E[The Codex (Task Management)]
    end

    subgraph Execution Layer
        F[Toolbelt]
        G[Workspace]
    end

    A -- User Prompts --> B
    B -- Governs --> C
    B -- Utilizes --> F
    C -- Informs --> B
    B -- Reads/Writes --> D
    B -- Reads/Writes --> E
    F -- Interacts with --> G
    D -- Provides Context to --> C
    E -- Provides Tasks to --> B
```

## Component Descriptions

### 1. User Interaction Layer

*   **IDE Integration**: The primary interface between the developer and the Atlas agent. It captures user prompts, displays agent output, and provides access to workspace files.

### 2. Cognitive Core

*   **Workflow Engine**: The heart of the agent. It orchestrates the entire development process by managing the **RIPER-A (Research, Innovate, Plan, Execute, Review, Adapt)** workflow. It determines the current mode, invokes the necessary tools, and manages state transitions.
*   **Cognitive Model**: A set of rules and reasoning principles that guide the agent's decision-making. It defines *how* the agent thinks, ensuring its actions are logical, consistent, and aligned with its core principles (e.g., prioritizing simplicity, identifying risks).

### 3. Knowledge & Task Management

*   **The Nexus (Memory System)**: The agent's long-term memory. It's a structured file-based system that stores project context, architectural decisions, learned patterns, and resolved errors. This allows the agent to maintain context across sessions and learn from experience.
*   **The Codex (Task Management)**: The agent's internal project manager. It maintains a backlog of tasks, breaks down complex requests into detailed, hierarchical plans, and tracks the status of all work items.

### 4. Execution Layer

*   **Toolbelt**: A collection of capabilities the agent can use to interact with the environment, such as reading/writing files, executing terminal commands, and searching the codebase.
*   **Workspace**: The actual project files and directories that the agent operates on. All actions performed by the Toolbelt are directed at the Workspace.