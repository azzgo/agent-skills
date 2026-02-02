"""
LLM-based evaluation system for aria2-json-rpc skill.

This package implements a dual-instance evaluation architecture:
- Instance 1 (Executor): Executes natural language commands with full tracing
- Instance 2 (Evaluator): Analyzes execution and provides judgment

See design.md (lines 334-703) for detailed architecture.
"""

__version__ = "0.1.0"
