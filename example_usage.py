"""
Example usage of the LLM class for fine-tuning with Unsloth.
This script demonstrates how to:
1. Load a model and tokenizer
2. Format training data
3. Fine-tune the model
4. Save adapters to HuggingFace Hub
"""

from llm_trainer import LLM
from datasets import Dataset

def main():
    # Example training data - replace with your actual data
    sample_data = [
        {
            "instruction": "What is the capital of France?",
            "input": "",
            "output": "The capital of France is Paris."
        },
        {
            "instruction": "Explain photosynthesis",
            "input": "",
            "output": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen."
        },
        {
            "instruction": "Write a Python function to calculate factorial",
            "input": "",
            "output": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
        },
        {
            "instruction": "Translate 'Hello' to Spanish",
            "input": "",
            "output": "Hello in Spanish is 'Hola'."
        }
    ]
    
    # Initialize LLM class
    print("Initializing LLM...")
    llm = LLM(
        model_name="unsloth/llama-2-7b-bnb-4bit",  # You can change this to other models
        max_seq_length=2048,
        load_in_4bit=True,
        # token="your_hf_token_here"  # Uncomment and add your HuggingFace token
    )
    
    # Load model and tokenizer
    print("Loading model and tokenizer...")
    model, tokenizer = llm.load_model_and_tokenizer(
        lora_rank=16,
        lora_alpha=16,
        lora_dropout=0.1,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )
    
    # Format training data
    print("Formatting training data...")
    train_dataset = llm.format_data(
        dataset=sample_data,
        format_type="alpaca",  # Options: "alpaca", "chat", "completion"
        instruction_key="instruction",
        input_key="input",
        output_key="output"
    )
    
    print(f"Formatted {len(train_dataset)} training examples")
    print("Sample formatted text:")
    print(train_dataset[0]["text"])
    print("-" * 50)
    
    # Get model info
    print("Model Information:")
    model_info = llm.get_model_info()
    for key, value in model_info.items():
        print(f"{key}: {value}")
    print("-" * 50)
    
    # Fine-tune the model
    print("Starting fine-tuning...")
    trainer = llm.finetune(
        train_dataset=train_dataset,
        output_dir="./fine_tuned_model",
        num_train_epochs=1,  # Increase for real training
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=1,
        save_strategy="epoch"
    )
    
    # Test generation
    print("Testing text generation...")
    test_prompt = "### Instruction:\nWhat is machine learning?\n\n### Response:\n"
    generated_text = llm.generate_text(
        prompt=test_prompt,
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True
    )
    print(f"Generated text: {generated_text}")
    print("-" * 50)
    
    # Save adapters locally
    print("Saving adapters locally...")
    llm.save_adapters_local("./saved_adapters")
    
    # Push to HuggingFace Hub (uncomment if you have a token and want to upload)
    # print("Pushing to HuggingFace Hub...")
    # hub_url = llm.push_to_hub(
    #     repo_name="your-username/your-model-name",
    #     private=False,
    #     save_method="lora"  # Options: "lora", "merged_16bit", "merged_4bit"
    # )
    # print(f"Model uploaded to: {hub_url}")
    
    print("Example completed successfully!")

def example_with_custom_dataset():
    """
    Example showing how to use with a HuggingFace dataset
    """
    print("Example with HuggingFace dataset...")
    
    llm = LLM(model_name="unsloth/mistral-7b-bnb-4bit")
    
    # Load model
    llm.load_model_and_tokenizer()
    
    # You can also load from HuggingFace datasets
    # dataset = llm.format_data("alpaca", format_type="alpaca")
    
    # Or load your own JSON/CSV file
    # dataset = llm.format_data("path/to/your/dataset.json", format_type="alpaca")
    
    print("Custom dataset example setup complete!")

def example_chat_format():
    """
    Example using chat format instead of Alpaca format
    """
    print("Example with chat format...")
    
    chat_data = [
        {
            "instruction": "Hello, how are you?",
            "output": "I'm doing well, thank you for asking! How can I help you today?"
        },
        {
            "instruction": "Can you explain quantum computing?",
            "output": "Quantum computing uses quantum mechanical phenomena like superposition and entanglement to process information in fundamentally different ways than classical computers."
        }
    ]
    
    llm = LLM()
    llm.load_model_and_tokenizer()
    
    # Format in chat style
    dataset = llm.format_data(
        dataset=chat_data,
        format_type="chat"
    )
    
    print("Sample chat formatted text:")
    print(dataset[0]["text"])

if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to run additional examples
    # example_with_custom_dataset()
    # example_chat_format()