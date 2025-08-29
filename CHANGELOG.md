# Changelog

All notable changes to XXM Workflows will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-19

### Added
- **LLM Training Class** (`llm_trainer.py`)
  - Fast model loading with Unsloth library
  - LoRA fine-tuning support with customizable parameters
  - Multiple data format support (Alpaca, Chat, Completion)
  - HuggingFace Hub integration for model upload
  - Memory-efficient 4-bit quantization
  - Comprehensive training configuration options

- **LLM Inference Class** (`llm_inference.py`)
  - Load base models with optional LoRA adapter support
  - CSV and JSONL file processing with configurable text columns
  - Single text and batch inference capabilities
  - Customizable generation parameters
  - Progress tracking for batch operations
  - Result saving to CSV format
  - Model information and statistics

- **Package Infrastructure**
  - Complete `setup.py` with proper dependencies
  - Modern `pyproject.toml` configuration
  - Package `__init__.py` with proper imports
  - `MANIFEST.in` for file inclusion
  - MIT License
  - Comprehensive documentation

- **Installation Tools**
  - Cross-platform installation scripts (`install.sh`, `install.bat`)
  - Virtual environment setup
  - Optional dependency installation
  - Verification steps

- **Examples and Documentation**
  - Training example (`example_usage.py`)
  - Inference example (`inference_example.py`)
  - Updated README with installation methods
  - API documentation and usage examples

- **Development Tools**
  - Development dependencies (pytest, black, flake8, mypy)
  - Testing configuration
  - Code formatting and linting setup
  - Optional Jupyter notebook support

### Dependencies
- torch>=2.0.0
- transformers>=4.35.0
- datasets>=2.14.0
- accelerate>=0.24.0
- peft>=0.6.0
- trl>=0.7.0
- unsloth (from GitHub)
- huggingface_hub>=0.17.0
- wandb>=0.15.0
- bitsandbytes>=0.41.0
- xformers>=0.0.22
- pandas>=1.5.0

### Features
- **Training**: Complete workflow from data loading to model upload
- **Inference**: Efficient inference with adapter support
- **File Processing**: Handle CSV/JSONL files with text data
- **Batch Operations**: Process multiple texts efficiently
- **Memory Optimization**: 4-bit quantization for reduced memory usage
- **Flexibility**: Customizable parameters for all operations
- **Integration**: Seamless HuggingFace Hub integration

### Installation Methods
1. From source: `pip install .`
2. Development mode: `pip install -e .`
3. With optional deps: `pip install ".[dev]"`, `".[examples]"`, `".[full]"`
4. Using install scripts: `./install.sh` or `install.bat`

### Supported Python Versions
- Python 3.8+
- Compatible with modern PyTorch and Transformers versions

### Notes
- Requires CUDA-compatible GPU for optimal performance
- Unsloth library provides significant speed improvements
- LoRA adapters enable memory-efficient fine-tuning
- Comprehensive error handling and logging throughout