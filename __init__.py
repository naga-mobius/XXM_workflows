"""
XXM Workflows - LLM Training and Inference Package

A comprehensive package for fine-tuning and inference with Large Language Models
using the Unsloth library for optimized performance.

Components:
- LLM: Training class for fine-tuning models with LoRA adapters
- LLMInference: Inference class for loading models and performing inference
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main classes
try:
    from .llm_trainer import LLM
    from .llm_inference import LLMInference
    
    __all__ = [
        "LLM",
        "LLMInference",
        "__version__",
        "__author__",
        "__email__"
    ]
    
except ImportError as e:
    # Handle cases where dependencies aren't installed yet
    import warnings
    warnings.warn(
        f"Could not import all modules due to missing dependencies: {e}. "
        "Please install the package with: pip install xxm-workflows"
    )
    
    __all__ = [
        "__version__",
        "__author__",
        "__email__"
    ]

# Package information
PACKAGE_INFO = {
    "name": "xxm-workflows",
    "version": __version__,
    "description": "LLM Training and Inference Package with Unsloth",
    "features": [
        "Fast model loading with Unsloth",
        "LoRA fine-tuning support",
        "Multiple data format support",
        "HuggingFace Hub integration",
        "Batch inference capabilities",
        "CSV/JSONL file processing"
    ]
}

def get_package_info():
    """Get package information."""
    return PACKAGE_INFO

def print_package_info():
    """Print package information."""
    info = get_package_info()
    print(f"Package: {info['name']} v{info['version']}")
    print(f"Description: {info['description']}")
    print("Features:")
    for feature in info['features']:
        print(f"  - {feature}")