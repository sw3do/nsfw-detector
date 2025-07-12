# Contributing to NSFW Detector

We love your input! We want to make contributing to NSFW Detector as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/sw3do/nsfw-detector/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/sw3do/nsfw-detector/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/nsfw-detector.git
cd nsfw-detector
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download or place your model file:
```bash
# Place your model at: models/mobilenet_v2_140_224/saved_model.h5
```

5. Run tests:
```bash
python nsfw_detector.py
python api_server.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Add type hints where appropriate

## Testing

- Test your changes thoroughly
- Add unit tests for new features
- Ensure existing tests still pass
- Test with different image formats and sizes

## Submitting Changes

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Add your feature description"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Open a Pull Request on GitHub

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Questions?

Don't hesitate to ask questions by opening an issue with the "question" label.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms. 