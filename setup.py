from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-log-debugger",
    version="0.1.0",
    author="Backend Engineer",
    description="AI-Powered Log Debugging Assistant - Intelligent log analysis and root cause detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-log-debugger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=1.0.0",
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
        "scipy>=1.11.1",
        "openai>=0.27.8",
        "requests>=2.31.0",
        "pyyaml>=6.0",
        "pydantic>=2.0.0",
    ],
)
