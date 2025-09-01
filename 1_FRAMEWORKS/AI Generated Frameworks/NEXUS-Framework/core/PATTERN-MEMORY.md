# Pattern Memory - Learning from Experience

## What This Is
A simple way for AI to remember and reuse successful coding patterns and solutions focused on Python development.

## How It Works
During conversations, remember patterns that work well and apply them to similar problems.

## Pattern Categories

### 1. Python Code Patterns
**Common solutions that work well:**

**Class Design Patterns:**
- Data classes for simple data containers
- Abstract base classes for interface definition
- Context managers for resource management
- Descriptors for attribute access control

**Error Handling Patterns:**
- Custom exception hierarchies for domain-specific errors
- Try/except/else/finally for proper resource cleanup
- Logging with appropriate levels and structured data
- Validation with early returns and clear error messages

**Data Processing Patterns:**
- Generator expressions for memory efficiency
- List/dict comprehensions for transformations
- Itertools for complex iteration patterns
- Collections module for specialized data structures

**Testing Patterns:**
- Pytest fixtures for test setup
- Parametrized tests for multiple scenarios
- Mocking external dependencies
- Property-based testing with hypothesis

### 2. Architecture Patterns
**How to structure Python applications:**

**Project Structure:**
- Package-based organization with clear separation
- Configuration management with environment variables
- Dependency injection for testability
- CLI interfaces with argparse or click

**Data Processing:**
- Pipeline patterns for ETL workflows
- Async/await for I/O-bound operations
- Multiprocessing for CPU-bound tasks
- Streaming processing for large datasets

**API Development:**
- FastAPI for modern REST APIs
- Pydantic for data validation
- SQLAlchemy for database operations
- Async database operations with asyncpg/aiomysql

### 3. Problem-Solving Patterns
**Approaches that work for different types of problems:**

**Performance Issues:**
- Profile with cProfile/line_profiler first
- Use appropriate data structures (sets vs lists)
- Cache frequently computed results
- Lazy evaluation for expensive operations

**Debugging Issues:**
- Use debugger (pdb/ipdb) for complex issues
- Add strategic logging points
- Unit tests to isolate problems
- Static analysis with mypy/pylint

**Scalability Issues:**
- Async programming for I/O-bound workloads
- Process pools for CPU-bound work
- Database connection pooling
- Caching strategies (Redis, memcached)

**Maintenance Issues:**
- Type hints for better code documentation
- Docstrings with clear examples
- Automated testing and CI/CD
- Code formatting with black/isort

### 4. Library and Tool Patterns
**Effective use of Python ecosystem:**

**Data Science Stack:**
- Pandas for data manipulation
- NumPy for numerical computing
- Matplotlib/seaborn for visualization
- Jupyter notebooks for exploration

**Development Tools:**
- Poetry for dependency management
- Pre-commit hooks for code quality
- pytest for testing
- Black for code formatting

**Production Tools:**
- Docker for containerization
- Gunicorn/uvicorn for WSGI/ASGI serving
- Celery for background tasks
- Monitoring with logging and metrics

## How to Apply Patterns

### Pattern Recognition
When a user asks for something:
1. **Identify the core problem type**
2. **Match it to known Python patterns**
3. **Adapt the pattern to their specific context**
4. **Explain why this pattern works in Python**

### Pattern Adaptation
Don't just copy patterns - adapt them:
- **Context matters:** Same pattern, different Python implementation
- **Performance matters:** Choose efficient Python constructs
- **Pythonic matters:** Follow Python idioms and conventions

### Pattern Evolution
Learn from each interaction:
- **What worked well?** Remember successful Python approaches
- **What could be better?** Note improvements for next time
- **What was unique?** Identify new Python patterns to remember

## Practical Examples

### Example 1: User asks for "data processing pipeline"
**Pattern Recognition:** ETL/data processing pattern needed
**Memory Recall:** Generator patterns, pandas operations, error handling
**Adaptation:** Consider data size, processing requirements, error tolerance
**Application:** Recommend appropriate Python tools and patterns

### Example 2: User has "slow Python code"
**Pattern Recognition:** Performance optimization pattern
**Memory Recall:** Profiling tools, efficient data structures, caching
**Adaptation:** Profile first, then optimize bottlenecks
**Application:** Systematic performance improvement with Python tools

### Example 3: User wants "API for data service"
**Pattern Recognition:** API development pattern
**Memory Recall:** FastAPI, Pydantic validation, async patterns
**Adaptation:** Consider data types, response time requirements, authentication
**Application:** Modern Python API with proper validation and documentation

## Memory Persistence
**Note:** This is about YOU remembering patterns during conversations, not about implementing persistent storage in user applications. The "memory" is your ability to:
- Reference similar Python solutions you've provided before
- Apply learned Python patterns to new problems
- Avoid repeating Python-specific mistakes
- Build on successful Python approaches

## Anti-Patterns to Avoid
**Remember what NOT to do in Python:**
- Don't use mutable default arguments
- Don't ignore Python's import system best practices
- Don't write Java/C++ style code in Python
- Don't ignore Python's built-in functions and libraries
- Don't skip error handling and logging
- Don't ignore type hints in complex codebases
- Don't use global variables when class/function scope works
- Don't reinvent wheels that exist in standard library