# Contributing to AI-Powered Security Monitoring Platform

First off, thank you for considering contributing to this project! 🎉

This project is a GSOC-level security monitoring platform, and we welcome contributions from developers, security researchers, and enthusiasts of all skill levels.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots, logs)
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (OS, Python version, Node.js version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed functionality**
- **Explain why this enhancement would be useful**
- **Include mockups or examples if applicable**

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:

- `good-first-issue` - Issues suitable for beginners
- `help-wanted` - Issues that need assistance
- `documentation` - Documentation improvements

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/AI-Powered-Security-Monitoring-Threat-Detection-Platform.git
   cd AI-Powered-Security-Monitoring-Threat-Detection-Platform
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up the development environment**
   - Follow the instructions in [README.md](README.md)
   - Install backend dependencies: `pip install -r requirements.txt`
   - Install frontend dependencies: `cd frontend && npm install`

4. **Make your changes**
   - Write clean, maintainable code
   - Add tests for new features
   - Update documentation as needed

## Development Workflow

### Backend Development

- Follow PEP 8 style guidelines for Python code
- Use type hints where applicable
- Write unit tests for new functions
- Run tests before submitting: `pytest`

### Frontend Development

- Follow React best practices
- Use TypeScript for type safety
- Ensure components are reusable and well-documented
- Test UI changes across different screen sizes

### AI Model Changes

- Document model architecture changes
- Include performance metrics (accuracy, precision, recall)
- Provide sample data for testing
- Update training scripts as needed

## Style Guidelines

### Python Code

- Follow PEP 8
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 88 characters (Black formatter)

```python
def detect_anomaly(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect anomalies in the provided data using Isolation Forest.
    
    Args:
        data: Input DataFrame containing log features
        
    Returns:
        Dictionary containing anomaly predictions and scores
    """
    # Implementation
```

### TypeScript/JavaScript Code

- Use ES6+ features
- Follow Airbnb style guide
- Use meaningful component and variable names
- Add JSDoc comments for complex functions

```typescript
/**
 * Renders a threat visualization chart
 * @param {ThreatData[]} data - Array of threat data points
 * @returns {JSX.Element} Chart component
 */
const ThreatChart: React.FC<ThreatChartProps> = ({ data }) => {
  // Implementation
};
```

## Commit Messages

Write clear and meaningful commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests when applicable

**Good examples:**
```
Add anomaly detection threshold configuration
Fix dashboard rendering issue on mobile devices
Update README with Docker deployment instructions
Refactor log parsing logic for better performance
```

## Pull Request Process

1. **Ensure your code follows the style guidelines**
2. **Update documentation** if you're changing functionality
3. **Add tests** for new features
4. **Run all tests** and ensure they pass
5. **Update the README.md** if needed
6. **Fill out the pull request template** completely
7. **Link related issues** in the PR description
8. **Request review** from maintainers

### PR Checklist

- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged and published

## Testing

### Backend Tests
```bash
pytest tests/
pytest tests/ --cov=backend  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Code Review Process

All submissions require review. The maintainers will:

- Review your code for quality and consistency
- Suggest improvements or changes
- Approve and merge when ready

Expected review time: 2-5 business days

## Community

- Join our discussions on GitHub
- Share your ideas and feedback
- Help others in issue discussions
- Spread the word about the project

## Recognition

Contributors will be:

- Listed in the Contributors section
- Mentioned in release notes
- Acknowledged in project documentation

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

Thank you for contributing! 🚀🔒
