<div align=center>

# Contributing to `PIXELATE`

Thank you for your interest in contributing to `PIXELATE`! 
We welcome contributions from the community and appreciate your help in making this project better.

[How to Contribute](#-how-to-contribute) • [Developer Setup](#-developer-setup) • [Pull Request Process](#-pull-request-process) • [Recognition](#-recognition)

</div>


## 🎯 How to Contribute

### I. Reporting Issues

- **Search existing issues** first to avoid duplicates
- **Use issue templates** when available
- **Provide detailed information**:
  - Python version
  - Operating system
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots (if applicable)

### II. Suggesting Features

- **Check existing feature requests** first
- **Describe the use case** clearly
- **Explain why** the feature would be valuable
- **Consider backwards compatibility**

### III. Code Contributions

We especially welcome contributions in these areas:

**High Priority**

- **Bug fixes** and stability improvements
- **Performance optimizations**
- **Chore tasks** like dependency updates and documentation improvements

**Medium Priority**

- **Code organization** and refactoring
- **New features** that align with project goals
- **Test coverage** enhancements

**Low Priority**

- **Minor enhancements** and quality-of-life improvements
- **Examples** and tutorials

<details>

<summary>Detailed Contribution Steps</summary>

1. **Create a feature branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**:
   - Follow existing code style
   - Write tests for new features or bug fixes
   - Update documentation if needed

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub

6. **Engage in the review process**:
   - Respond to feedback
   - Make requested changes
   - Ensure all checks pass

7. **Celebrate your contribution** once merged!

</details>

## 🚀 Developer Setup

### I. Prerequisites
This project uses uv for fast and reliable Python package management during development. 
Install uv first:

```bash
# Install uv with pip
pip install uv
```

### II. Development Installation
Clone the repository and install with dev dependencies:
```bash
git clone https://github.com/hanson-hschang/pixelate.git
cd pixelate
uv sync --all-groups --all-extras
```

<details>

<summary>Detail of Development Installation</summary>

This installs the package in editable mode along with all development dependencies including testing, linting, formatting, and type checking tools.

**Development Tools:**
- pytest (testing framework)
- pyupgrade (syntax upgrades)
- mypy (static type checking)
- types-toml, types-Pillow (type stubs)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- autoflake (remove unused imports)
- bandit (security checking)
- pre-commit (git hooks)

**Pre-commit Hooks:** Install pre-commit hooks to ensure code quality before commits
```bash
uv run pre-commit install
```

**Testing:** Run tests with pytest
```bash
# Run tests
uv run pytest -c pyproject.toml
```

**Linting**

If you encounter formatting issues during development or in CI/CD, use these commands to automatically fix them:

```bash
uv run pyupgrade --exit-zero-even-if-changed --py311-plus src/**/*.py tests/**/*.py # Upgrade syntax to Python 3.11+
uv run black --config pyproject.toml src tests          # Fix code formatting
uv run isort --settings-path pyproject.toml src tests  # Fix import sorting
uv run autoflake --in-place -r src tests # Remove unused imports

# Check what would be changed without making changes:
uv run flake8 src tests  # Check for linting issues
uv run black --diff --check --config pyproject.toml ./
uv run isort --diff --check-only --settings-path pyproject.toml ./
uv run autoflake --check -r src tests
uv run mypy --config-file pyproject.toml src tests         # Check static types
```

</details>

### III. Code Quality
- **Formatting**: Code is automatically formatted with [black](https://black.readthedocs.io/)
- **Import sorting**: Imports are sorted with [isort](https://pycqa.github.io/isort/)
- **Linting**: Code is linted with [flake8](https://flake8.pycqa.org/)
- **Type checking**: Static type checking with [mypy](https://mypy.readthedocs.io/)
- **Security**: Security checks with [bandit](https://bandit.readthedocs.io/)

### IV. CI/CD
This project uses GitHub Actions for continuous integration with separate workflows:
- **Test workflow**: Tests run on Python 3.11+
- **Linting workflow**: Ensures code adheres to linting standards
- **Security workflow**: CodeQL security scanning with write permissions for security results
- All checks must pass before merging to main branch


### V. Commit Message Guidelines

Use conventional commit format:

```
type(scope): short description

[optional body]

[optional footer]
```

<details>

<summary>Detailed Commit Message Guidelines</summary>

**Types**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(cli): add --verbose flag for detailed output
fix(parser): handle edge case for empty input
docs(readme): update installation instructions
refactor(processor): simplify image processing logic
test(api): add tests for new endpoint
chore(deps): update dependencies to latest versions
```

</details>

## 🔄 Pull Request Process

### I. Before Submitting

- [ ] Test changes locally
- [ ] Update documentation if needed
- [ ] Follow commit message guidelines
- [ ] Ensure backwards compatibility
- [ ] Check for console errors

### II. PR Description

Include in your PR description:

1. **What changes were made**
2. **Why the changes were necessary**
3. **How to test the changes**
4. **Screenshots** (for visual changes)
5. **Breaking changes** (if any)

### III. Review Process

- Maintainers will review PRs as time permits
- You may be asked to make changes
- Once approved, your PR will be merged
- Your contribution will be credited

## 🎉 Recognition

Contributors are recognized in several ways:

- **GitHub contributors** list
- **Changelog** mentions for significant contributions

We appreciate your time and effort in helping to improve this project.

---

<div align="center">

**Thank you for contributing to `PIXELATE`!**

![pixelate.png](examples/pixelate.png)

</div>