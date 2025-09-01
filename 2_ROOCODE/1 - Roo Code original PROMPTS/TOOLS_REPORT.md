# TOOLS_REPORT.md

## Overview

This report analyzes the tools specified in the following RooCode system prompt files:

- [`RooCode_System_ARCHITECT.txt`](.roo/RooCode_System_ARCHITECT.txt)
- [`RooCode_System_ASK.txt`](.roo/RooCode_System_ASK.txt)
- [`RooCode_System_CODE.txt`](.roo/RooCode_System_CODE.txt)
- [`RooCode_System_DEBUG.txt`](.roo/RooCode_System_DEBUG.txt)
- [`RooCode_System_ORCHESTRATOR.txt`](.roo/RooCode_System_ORCHESTRATOR.txt)

## Tools by File

### Architect, Ask, Code, Debug

All four of these files specify the following tools (with minor differences in some parameters and tool presence):

- read_file
- fetch_instructions
- search_files
- list_files
- list_code_definition_names
- apply_diff
- write_to_file
- insert_content
- search_and_replace
- browser_action (not present in Debug)
- execute_command (not present in Architect/Ask)
- ask_followup_question
- attempt_completion
- switch_mode
- new_task
- update_todo_list

### Orchestrator

The Orchestrator file only specifies:

- ask_followup_question
- attempt_completion
- switch_mode
- new_task
- update_todo_list

## Observations & Inconsistencies

- **Tool Set Differences:**  
  - The Orchestrator mode has a much smaller toolset, lacking all file/code manipulation tools.
  - Architect, Ask, Code, and Debug modes mostly share the same tools, but:
    - `browser_action` is missing from Debug.
    - `execute_command` is only present in Code and Debug.
- **Parameter Differences:**  
  - Some tools (like `write_to_file`, `apply_diff`) have slightly different parameter descriptions or usage examples across files.
  - The Orchestrator mode omits parameters for file/code tools entirely.
- **Expected Uniformity:**  
  - In theory, all files should present the same tools and parameters, but in practice, there are omissions and differences depending on the mode's intended capabilities.
- **Notable:**  
  - The core file/code tools are only available in Code and Debug modes.
  - Orchestrator is strictly for coordination and cannot manipulate files directly.

## Conclusion

There are inconsistencies in tool availability and parameter documentation across the RooCode system prompt files. The Orchestrator mode is the most limited, while Code and Debug are the most capable. Some tools are missing or have different parameters depending on the mode, which may lead to confusion or unexpected limitations if uniformity is required.