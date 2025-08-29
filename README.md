# XXM Workflows - LLM Training and Inference Package

A comprehensive Python package for fine-tuning and inference with Large Language Models using the Unsloth library for faster and more efficient training.

## Features

### Training (LLM Class)
- **Fast Model Loading**: Uses Unsloth for optimized model and tokenizer loading
- **Multiple Data Formats**: Supports Alpaca, Chat, and Completion formats
- **LoRA Fine-tuning**: Efficient fine-tuning using Low-Rank Adaptation
- **HuggingFace Integration**: Direct upload to HuggingFace Hub
- **Memory Efficient**: 4-bit quantization support for reduced memory usage
- **Flexible Configuration**: Customizable training parameters

### Inference (LLMInference Class)
- **Model + Adapter Loading**: Load base models with optional LoRA adapters
- **File Processing**: Read CSV and JSONL files with text data
- **Batch Inference**: Process multiple texts efficiently
- **Flexible Generation**: Customizable generation parameters
- **Progress Tracking**: Monitor batch processing progress

## Installation

### Method 1: Install from Source (Recommended)
```bash
# Clone or download the repository
git clone https://github.com/yourusername/xxm-workflows.git
cd xxm-workflows

# Install the package
pip install .

# Or install in development mode
pip install -e .
```

### Method 2: Install with pip (when published)
```bash
pip install xxm-workflows
```

### Method 3: Install with optional dependencies
```bash
# Install with development tools
pip install "xxm-workflows[dev]"

# Install with examples (Jupyter notebooks)
pip install "xxm-workflows[examples]"

# Install everything
pip install "xxm-workflows[full]"
```

### Method 4: Manual dependency installation
```bash
pip install -r requirements.txt
```

**Note**: For Colab users, you might need to restart the runtime after installation.

## Quick Start

### Training Example
```python
from xxm_workflows import LLM

# Initialize the LLM class
llm = LLM(
    model_name="unsloth/llama-2-7b-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True
)

# Load model and tokenizer
model, tokenizer = llm.load_model_and_tokenizer(
    lora_rank=16,
    lora_alpha=16,
    lora_dropout=0.1
)

# Format your training data
training_data = [
    {
        "instruction": "What is AI?",
        "input": "",
        "output": "AI stands for Artificial Intelligence..."
    }
]

dataset = llm.format_data(
    dataset=training_data,
    format_type="alpaca"
)

# Fine-tune the model
trainer = llm.finetune(
    train_dataset=dataset,
    num_train_epochs=1,
    per_device_train_batch_size=2,
    learning_rate=2e-4
)

# Save adapters locally
llm.save_adapters_local("./my_model")

# Or push to HuggingFace Hub
llm.push_to_hub("username/my-fine-tuned-model")
```

### Inference Example
```python
from xxm_workflows import LLMInference

# Initialize inference with base model and adapter
inference = LLMInference(
    base_model_path="unsloth/llama-2-7b-bnb-4bit",
    adapter_path="./my_model",  # Path to your fine-tuned adapter
    load_in_4bit=True
)

# Load the model
model, tokenizer = inference.load_model()

# Single text inference
response = inference.generate_response(
    text="What is machine learning?",
    system_prompt="You are a helpful AI assistant."
)

# Process CSV file with text data
responses = inference.inference_from_file(
    file_path="questions.csv",  # CSV with 'text' column
    output_path="responses.csv"
)

# Batch processing
texts = ["Question 1", "Question 2", "Question 3"]
batch_responses = inference.batch_inference(texts)
```

## Supported Models

The class works with any model supported by Unsloth, including:

- Llama 2 (7B, 13B, 70B)
- Mistral (7B)
- Code Llama
- And many more 4-bit quantized models

## Data Formats

### Alpaca Format
```python
dataset = llm.format_data(data, format_type="alpaca")
```

### Chat Format
```python
dataset = llm.format_data(data, format_type="chat")
```

### Completion Format
```python
dataset = llm.format_data(data, format_type="completion")
```

## Advanced Usage

### Custom LoRA Configuration
```python
model, tokenizer = llm.load_model_and_tokenizer(
    lora_rank=32,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
)
```

### Training with Evaluation Dataset
```python
trainer = llm.finetune(
    train_dataset=train_data,
    eval_dataset=eval_data,
    evaluation_strategy="steps",
    eval_steps=50
)
```

### Different Save Methods
```python
# Save only LoRA adapters
llm.push_to_hub("user/model", save_method="lora")

# Save merged 16-bit model
llm.push_to_hub("user/model", save_method="merged_16bit")

# Save merged 4-bit model
llm.push_to_hub("user/model", save_method="merged_4bit")
```

## Methods Overview

### Core Methods
- `load_model_and_tokenizer()`: Load and configure model with LoRA
- `format_data()`: Format training data in various styles
- `finetune()`: Fine-tune the model with specified parameters
- `save_adapters_local()`: Save adapters to local directory
- `push_to_hub()`: Upload adapters to HuggingFace Hub

### Utility Methods
- `generate_text()`: Generate text using the fine-tuned model
- `get_model_info()`: Get detailed model information

## Configuration Options

### Model Loading
- `model_name`: HuggingFace model identifier
- `max_seq_length`: Maximum sequence length
- `load_in_4bit`: Enable 4-bit quantization
- `dtype`: Model weight data type

### LoRA Parameters
- `lora_rank`: LoRA rank (lower = fewer parameters)
- `lora_alpha`: LoRA alpha (scaling factor)
- `lora_dropout`: Dropout rate for LoRA layers
- `target_modules`: Which modules to apply LoRA to

### Training Parameters
- `num_train_epochs`: Number of training epochs
- `per_device_train_batch_size`: Batch size per device
- `gradient_accumulation_steps`: Gradient accumulation
- `learning_rate`: Learning rate
- `warmup_steps`: Learning rate warmup steps

## Examples

See `example_usage.py` for comprehensive examples including:
- Basic fine-tuning workflow
- Custom dataset usage
- Different data formatting options
- Text generation testing

## Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended)
- At least 8GB GPU memory for 7B models
- HuggingFace account (for model upload)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.