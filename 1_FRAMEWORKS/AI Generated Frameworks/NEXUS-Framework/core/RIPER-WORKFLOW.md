# RIPER Workflow - The Core Process

## What This Is
A simple 5-step process that any AI can follow to solve Python coding problems systematically.

## The 5 Steps

### Ω₁ RESEARCH
**What to do:** Understand the problem completely
- Read existing Python code if provided
- Ask clarifying questions if needed
- Identify the real requirements and constraints
- Note performance, scalability, and maintenance requirements

**Output:** Clear understanding of what needs to be built

### Ω₂ INNOVATE
**What to do:** Think of different ways to solve it
- Consider 2-3 different Python approaches
- Think about pros/cons of each (performance, maintainability, complexity)
- Consider existing Python libraries vs custom implementation
- Pick the most appropriate approach

**Output:** Chosen solution approach with reasoning

### Ω₃ PLAN
**What to do:** Create a step-by-step implementation plan
- Break down into small, manageable tasks
- Consider dependencies between components
- Identify potential issues and edge cases
- Plan testing strategy

**Output:** Detailed step-by-step implementation plan

### Ω₄ EXECUTE
**What to do:** Implement the solution
- Follow the plan step by step
- Write clean, Pythonic code
- Include appropriate error handling
- Add logging where necessary

**Output:** Working Python code that solves the problem

### Ω₅ REVIEW
**What to do:** Check and improve the solution
- Test the code thoroughly
- Check for edge cases and error conditions
- Review for Python best practices
- Document any lessons learned

**Output:** Validated, improved solution

## Usage Examples

### Simple Task
```
User: "Create a function to process CSV data"

Ω₁ RESEARCH: CSV processing needs, data size, error handling requirements
Ω₂ INNOVATE: pandas vs csv module vs DictReader, consider memory usage
Ω₃ PLAN: 1) Read CSV 2) Process data 3) Handle errors 4) Return results
Ω₄ EXECUTE: [write the function with appropriate error handling]
Ω₅ REVIEW: Test with different CSV formats, check memory usage
```

### Complex Task
```
User: "Build a data processing pipeline for log analysis"

Ω₁ RESEARCH: Log format, volume, processing requirements, output needs
Ω₂ INNOVATE: Streaming vs batch, async vs sync, storage options
Ω₃ PLAN: Parser → Processor → Aggregator → Output, with error handling
Ω₄ EXECUTE: Implement each component with proper Python patterns
Ω₅ REVIEW: Performance testing, error scenario testing, monitoring
```

## Adaptation Rules
- **Focus on requirements:** Understand what actually needs to be solved
- **Choose appropriate tools:** Use the right Python libraries for the job
- **Consider maintainability:** Write code that others (or future you) can understand
- **Plan for errors:** Python applications need robust error handling
- **Test thoroughly:** Verify the solution works with real data

## Python-Specific Considerations

### During Research (Ω₁)
- What Python version constraints exist?
- Are there existing libraries that solve this?
- What are the performance requirements?
- How will this integrate with existing Python code?

### During Innovation (Ω₂)
- Standard library vs third-party libraries
- Sync vs async implementation
- Memory usage considerations
- Error handling strategy

### During Planning (Ω₃)
- Module/package structure
- Configuration management
- Testing approach (unit, integration)
- Documentation requirements

### During Execution (Ω₄)
- Follow PEP 8 style guidelines
- Use type hints for complex functions
- Include docstrings for public APIs
- Add appropriate logging

### During Review (Ω₅)
- Run tests with different data scenarios
- Check performance with realistic data sizes
- Verify error handling works correctly
- Review code for Python best practices