# Security Policy

## Supported Versions

Currently, only the latest version of the DuckDB Code Practice repository is supported.

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it responsibly.

### How to Report

1. **Do not create a public issue** - Security vulnerabilities should not be disclosed publicly
2. **Send an email** to the repository maintainers with details about the vulnerability
3. **Include the following information**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if known)

### What to Expect

- We will acknowledge receipt of your report within 48 hours
- We will provide a detailed response within 7 days
- We will work with you to understand and validate the report
- We will coordinate a fix and release plan
- We will credit you for the discovery (if you wish)

### Security Best Practices

When working with this repository:

- **Never commit credentials** to the repository
- **Use environment variables** for sensitive configuration
- **Review dependencies** regularly for known vulnerabilities
- **Keep your environment updated** with the latest security patches
- **Use virtual environments** to isolate dependencies

## Dependency Security

This repository uses several Python packages. We regularly review and update dependencies to address security vulnerabilities:

- DuckDB
- Pandas
- Jupyter
- NumPy
- Other data processing libraries

## Data Privacy

This repository:
- Does not collect personal data
- Does not transmit data to external services
- Works with locally generated sample data
- Does not require internet connectivity for core functionality

## Code Security

We follow security best practices:

- **Input validation**: All user inputs are validated
- **Error handling**: Proper error handling prevents information leakage
- **Dependency management**: Regular updates and security scanning
- **Code review**: All contributions go through review process

## Disclaimer

This is an educational repository for learning purposes. While we follow security best practices, it is not designed for production use or handling sensitive data. Users should:

- Use this repository in isolated development environments
- Not process sensitive or personal data
- Follow their organization's security guidelines
- Understand the limitations of educational code

## Contact

For security-related questions or vulnerability reports, please contact the repository maintainers through GitHub's security features or private communication channels.