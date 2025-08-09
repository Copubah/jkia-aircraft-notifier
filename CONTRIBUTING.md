# Contributing to JKIA Aircraft Landing Notifier

Thank you for your interest in contributing to the JKIA Aircraft Landing Notifier project! 🎉

## How to Contribute

### 1. Fork the Repository
- Click the "Fork" button at the top right of this repository
- Clone your fork locally:
  ```bash
  git clone https://github.com/YOUR_USERNAME/jkia-aircraft-notifier.git
  cd jkia-aircraft-notifier
  ```

### 2. Set Up Development Environment
- Install prerequisites:
  - AWS CLI configured
  - Terraform >= 1.0
  - Python 3.12+
- Install Python dependencies:
  ```bash
  pip install -r lambda/requirements.txt
  ```

### 3. Make Your Changes
- Create a new branch for your feature:
  ```bash
  git checkout -b feature/your-feature-name
  ```
- Make your changes
- Test your changes thoroughly

### 4. Testing
Before submitting, ensure:
- [ ] Terraform configuration validates: `terraform validate`
- [ ] Lambda function works: `python lambda/lambda_function.py`
- [ ] Documentation is updated if needed
- [ ] No sensitive information is committed

### 5. Submit Pull Request
- Push your changes:
  ```bash
  git push origin feature/your-feature-name
  ```
- Create a Pull Request with:
  - Clear description of changes
  - Screenshots if UI changes
  - Test results

## Types of Contributions

### 🐛 Bug Reports
- Use the issue template
- Include steps to reproduce
- Provide error logs and screenshots
- Specify your environment (AWS region, Terraform version, etc.)

### ✨ Feature Requests
- Describe the feature and use case
- Explain why it would be valuable
- Consider implementation complexity

### 📚 Documentation
- Fix typos and improve clarity
- Add examples and use cases
- Update architecture diagrams
- Improve setup instructions

### 🔧 Code Improvements
- Performance optimizations
- Better error handling
- Code refactoring
- Security enhancements

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

### Terraform Best Practices
- Use consistent naming conventions
- Add descriptions to variables and outputs
- Follow AWS resource naming standards
- Use data sources when appropriate

### Commit Messages
Use conventional commit format:
```
type(scope): description

Examples:
feat(lambda): add aircraft type detection
fix(terraform): correct IAM policy permissions
docs(readme): update installation instructions
```

### Security
- Never commit AWS credentials
- Use IAM roles with least privilege
- Validate all inputs
- Handle errors gracefully

## Project Structure

```
jkia-aircraft-notifier/
├── README.md              # Main documentation
├── LICENSE               # MIT license
├── CONTRIBUTING.md       # This file
├── .gitignore           # Git ignore rules
├── deploy.sh            # Deployment script
├── main.tf              # Root Terraform config
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── docs/                # Documentation
│   ├── architecture.md  # Architecture details
│   └── ...
├── lambda/              # Lambda function code
│   ├── lambda_function.py
│   └── requirements.txt
└── terraform/           # Terraform modules
    ├── eventbridge.tf
    ├── lambda.tf
    ├── sns.tf
    └── ...
```

## Getting Help

- 📖 Check the [README](README.md) for setup instructions
- 🏗️ Review [Architecture Documentation](docs/architecture.md)
- 🐛 Search existing [Issues](../../issues)
- 💬 Start a [Discussion](../../discussions) for questions

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold this code.

## Questions?

Feel free to open an issue with the "question" label or start a discussion. We're here to help! 🚀

---

Thank you for contributing to making aircraft tracking more accessible! ✈️