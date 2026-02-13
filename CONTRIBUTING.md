# Contributing to AI-Powered Log Debugging Assistant

Thank you for your interest in contributing! Here's how you can help improve this project.

## Development Setup

### Prerequisites
- Python 3.9+
- Git
- Virtual environment (venv)

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-log-debugger.git
   cd ai-log-debugger
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test locally

3. **Run tests**
   ```bash
   pytest tests/ -v --cov=src
   ```

4. **Format your code**
   ```bash
   black src/ tests/
   flake8 src/ tests/
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: description of what was added"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub with:
   - Clear description of changes
   - Reference to any related issues
   - Test results showing all tests pass

## Code Standards

- **Style Guide:** Follow PEP 8
- **Testing:** All new features must include tests (target 90%+ coverage)
- **Documentation:** Update docstrings and README for new features
- **Type Hints:** Use type annotations for better code clarity

## Areas for Contribution

### High Priority
- [ ] Support for structured logs (JSON, XML parsing)
- [ ] Real-time log streaming analysis
- [ ] Performance optimization for large files (>500MB)
- [ ] Integration with popular log aggregation tools (ELK, Datadog)

### Medium Priority
- [ ] Custom anomaly detection models (ML-based)
- [ ] Web dashboard UI for visualization
- [ ] Docker containerization
- [ ] Additional language support

### Low Priority
- [ ] Documentation improvements
- [ ] Example scripts and tutorials
- [ ] Performance benchmarks

## Reporting Issues

When reporting bugs, include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Relevant log files (if applicable)

## Code Review

All contributions go through review to ensure:
- Quality and correctness
- No breaking changes
- Proper documentation
- Test coverage maintained
- Security considerations

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue with your question or email the maintainers.

Thank you for contributing! 🎉
