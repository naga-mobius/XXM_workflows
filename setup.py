"""
Setup script for XXM Workflows - LLM Training and Inference Package
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = []
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                # Handle git+https requirements
                if line.startswith("unsloth"):
                    # For pip install, we'll handle unsloth separately
                    requirements.append("unsloth @ git+https://github.com/unslothai/unsloth.git")
                else:
                    requirements.append(line)
        return requirements

# Package metadata
PACKAGE_NAME = "xxm-workflows"
VERSION = "0.1.0"
AUTHOR = "Your Name"
AUTHOR_EMAIL = "your.email@example.com"
DESCRIPTION = "A comprehensive package for LLM fine-tuning and inference using Unsloth"
URL = "https://github.com/yourusername/xxm-workflows"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    py_modules=[
        "llm_trainer",
        "llm_inference"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.35.0",
        "datasets>=2.14.0",
        "accelerate>=0.24.0",
        "peft>=0.6.0",
        "trl>=0.7.0",
        "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git",
        "huggingface_hub>=0.17.0",
        "wandb>=0.15.0",
        "bitsandbytes>=0.41.0",
        "xformers>=0.0.22",
        "pandas>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ],
        "examples": [
            "jupyter>=1.0.0",
            "notebook>=6.0.0",
        ],
        "full": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
            "jupyter>=1.0.0",
            "notebook>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "xxm-train=llm_trainer:main",
            "xxm-inference=llm_inference:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.py"],
    },
    keywords=[
        "llm",
        "large language models",
        "fine-tuning",
        "inference",
        "unsloth",
        "transformers",
        "pytorch",
        "machine learning",
        "ai",
        "natural language processing",
        "lora",
        "peft"
    ],
    project_urls={
        "Bug Reports": f"{URL}/issues",
        "Source": URL,
        "Documentation": f"{URL}#readme",
    },
    zip_safe=False,
    license="MIT",
)