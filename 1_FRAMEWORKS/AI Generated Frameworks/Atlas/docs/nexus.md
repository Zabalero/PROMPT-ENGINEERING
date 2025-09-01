# The Nexus: The Atlas Memory System

The Nexus is the persistent, file-based memory system that serves as the agent's long-term brain. It is the foundation for the agent's ability to learn, adapt, and maintain deep project context over time. All Nexus files are stored within the `.atlas/nexus/` directory.

## Core Memory Components

The Nexus is composed of several specialized files, each serving a distinct purpose.

### 1. `project_summary.md`
*   **Purpose**: A high-level, living document that describes the project's purpose, architecture, key components, and technology stack.
*   **Updated**: During the **Adapt** phase after any significant architectural changes are made.
*   **Consulted**: During the **Research** phase to quickly gain project-wide context.

### 2. `decision_log.md`
*   **Purpose**: An immutable log of all significant technical decisions, their rationales, and the alternatives that were considered.
*   **Format**: Chronological entries, each with a timestamp, the decision made, and the reasoning.
*   **Updated**: During the **Adapt** phase, after a key decision is finalized in the **Plan** and **Review** phases.
*   **Example Entry**:
    ```markdown
    ---
    **Timestamp**: 2024-10-26T14:30:00Z
    **Decision**: Adopted JWT for stateless session management.
    **Rationale**: Aligns with the microservices architecture, removing the need for a shared session store and improving scalability.
    **Alternatives**: Stateful sessions (rejected due to scalability concerns).
    ---
    ```

### 3. `error_catalog.md`
*   **Purpose**: A database of encountered errors, their root causes, and the solutions that were implemented.
*   **Updated**: During the **Adapt** phase, after an error is successfully diagnosed and fixed.
*   **Consulted**: During the **Research** and **Innovate** phases when encountering new bugs, to check for similar past issues.
*   **Special Feature**: If the same error is logged more than twice, the agent is programmed to propose a systemic fix (e.g., a new linting rule, a change in data validation) to prevent future recurrence.

### 4. `patterns_library.md`
*   **Purpose**: A collection of reusable coding patterns, architectural designs, and conventions specific to the project.
*   **Updated**: During the **Adapt** phase, when a solution is deemed generalizable and worthy of becoming a project standard.
*   **Consulted**: During the **Innovate** and **Plan** phases to ensure consistency and leverage established best practices.

## The Memory Cycle

The Nexus is not a static archive; it is actively used and updated throughout the RIPER-A workflow.

1.  **Recall (Research)**: The agent begins by consulting the Nexus to load relevant context, past decisions, and known errors.
2.  **Reference (Innovate & Plan)**: The agent references the Nexus to guide its brainstorming and planning, ensuring new work aligns with past decisions and patterns.
3.  **Record (Adapt)**: After a task is successfully reviewed, the agent updates the Nexus with new knowledge, ensuring that the project's "memory" is always current.