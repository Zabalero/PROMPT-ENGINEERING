# The Codex: The Atlas Task Management System

The Codex is the agent's integrated project management system. It provides the tools and structure for the agent to autonomously decompose complex goals, manage its own tasks, and maintain a clear view of the project's status. All Codex files are stored within the `.atlas/codex/` directory.

## Core Components

### 1. `backlog.md`
*   **Purpose**: The master list of all identified tasks that have not yet been completed or assigned to a specific sprint.
*   **Format**: A simple, prioritized list of tasks. Each task has a unique ID, a priority level, a status, and a descriptive title.
*   **Example Entry**:
    ```markdown
    - [TASK-007][HIGH][TODO] Implement user profile image uploads
    - [TASK-008][MEDIUM][TODO] Refactor the authentication service to use async/await
    ```

### 2. `sprints/` Directory
*   **Purpose**: To organize work into focused, time-bound efforts. The agent can propose and manage its own sprints.
*   **Structure**: Each sprint is a subdirectory (e.g., `sprint_1/`, `sprint_2/`) containing detailed task files.

### 3. `task_{id}.md` Files
*   **Purpose**: A detailed breakdown of a complex task. This is where the agent's planning happens.
*   **Location**: Inside a sprint directory (e.g., `sprints/sprint_1/task_007.md`).
*   **Structure**:
    *   **Metadata**: Task ID, title, priority, status, dependencies.
    *   **Objective**: A clear statement of what the task aims to achieve.
    *   **Implementation Checklist**: A precise, step-by-step list of actions required to complete the task. This is the direct output of the **Plan** phase. Each item is a concrete action (e.g., "Create file `src/services/upload.js`," "Add function `handleImageUpload` to `userController.js`").
    *   **Risk Assessment**: A brief analysis of potential risks (technical, integration) and mitigation strategies, identified during the **Plan** phase.

## The Task Management Workflow

The Codex is central to the RIPER-A workflow, particularly in the transition from ideation to execution.

1.  **Task Identification (Research/Innovate)**: New tasks are identified and added to the `backlog.md`.
2.  **Task Decomposition (Plan)**: When a task is selected from the backlog, the agent enters the **Plan** phase. It creates a detailed `task_{id}.md` file, breaking the objective down into a comprehensive implementation checklist.
3.  **Task Execution (Execute)**: The agent works through the implementation checklist in the `task_{id}.md` file, one item at a time. Its focus is solely on completing the current checklist item.
4.  **Status Updates (Review/Adapt)**: As checklist items are completed and verified, the agent updates the status in the `task_{id}.md` file and, eventually, the main `backlog.md`.

This system ensures that the agent's work is always structured, traceable, and aligned with the project's larger goals. It transforms abstract requests into concrete, actionable plans that can be executed safely and efficiently.