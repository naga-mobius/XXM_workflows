"""
Example usage of the LLMInference class.
This script demonstrates how to:
1. Load a base model with optional adapters
2. Perform single text inference
3. Read and process CSV/JSONL files
4. Batch inference with file I/O
"""

from llm_inference import LLMInference
import os

def main():
    # Example 1: Basic inference setup
    print("=== Example 1: Basic Inference Setup ===")
    
    # Initialize inference class with base model
    inference = LLMInference(
        base_model_path="unsloth/llama-2-7b-bnb-4bit",  # or your model path
        adapter_path=None,  # Add path to your fine-tuned adapter if available
        max_seq_length=2048,
        load_in_4bit=True,
        # token="your_hf_token_here"  # Uncomment if needed for private models
    )
    
    # Load the model and tokenizer
    print("Loading model and tokenizer...")
    model, tokenizer = inference.load_model()
    print("Model loaded successfully!")
    
    # Example 2: Single text inference
    print("\n=== Example 2: Single Text Inference ===")
    
    sample_text = "What is the capital of France?"
    system_prompt = "You are a helpful assistant. Please provide accurate and concise answers."
    
    response = inference.generate_response(
        text=sample_text,
        system_prompt=system_prompt
    )
    
    print(f"Input: {sample_text}")
    print(f"Response: {response}")
    
    # Example 3: Custom generation parameters
    print("\n=== Example 3: Custom Generation Parameters ===")
    
    # Update generation config for more creative responses
    custom_config = {
        'temperature': 0.9,
        'top_p': 0.95,
        'max_new_tokens': 256
    }
    
    creative_response = inference.generate_response(
        text="Write a short poem about machine learning.",
        custom_generation_config=custom_config
    )
    
    print(f"Creative response: {creative_response}")
    
    # Example 4: Batch inference with list of texts
    print("\n=== Example 4: Batch Inference ===")
    
    sample_texts = [
        "Explain photosynthesis in simple terms.",
        "What are the benefits of renewable energy?",
        "How does machine learning work?"
    ]
    
    batch_responses = inference.batch_inference(
        texts=sample_texts,
        system_prompt="You are an educational assistant. Provide clear explanations."
    )
    
    for i, (question, answer) in enumerate(zip(sample_texts, batch_responses)):
        print(f"\nQ{i+1}: {question}")
        print(f"A{i+1}: {answer}")
    
    # Example 5: Create sample CSV file and process it
    print("\n=== Example 5: CSV File Processing ===")
    
    # Create a sample CSV file
    import pandas as pd
    sample_data = {
        'text': [
            'What is artificial intelligence?',
            'Explain quantum computing.',
            'What are the advantages of solar energy?'
        ],
        'category': ['AI', 'Computing', 'Energy']
    }
    
    sample_csv_path = 'sample_questions.csv'
    pd.DataFrame(sample_data).to_csv(sample_csv_path, index=False)
    print(f"Created sample CSV: {sample_csv_path}")
    
    # Process the CSV file
    csv_responses = inference.inference_from_file(
        file_path=sample_csv_path,
        output_path='results.csv',
        text_column='text',
        system_prompt="You are a knowledgeable assistant."
    )
    
    print(f"Processed {len(csv_responses)} texts from CSV")
    print("Results saved to 'results.csv'")
    
    # Example 6: Create and process JSONL file
    print("\n=== Example 6: JSONL File Processing ===")
    
    # Create a sample JSONL file
    import json
    
    sample_jsonl_path = 'sample_questions.jsonl'
    sample_jsonl_data = [
        {'text': 'What is blockchain technology?', 'source': 'tech'},
        {'text': 'How do vaccines work?', 'source': 'health'},
        {'text': 'What causes climate change?', 'source': 'environment'}
    ]
    
    with open(sample_jsonl_path, 'w') as f:
        for item in sample_jsonl_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"Created sample JSONL: {sample_jsonl_path}")
    
    # Process the JSONL file
    jsonl_responses = inference.inference_from_file(
        file_path=sample_jsonl_path,
        output_path='jsonl_results.csv',
        text_column='text'  # This is the key name in JSONL
    )
    
    print(f"Processed {len(jsonl_responses)} texts from JSONL")
    print("Results saved to 'jsonl_results.csv'")
    
    # Example 7: Model information
    print("\n=== Example 7: Model Information ===")
    
    model_info = inference.get_model_info()
    print("Model Information:")
    for key, value in model_info.items():
        print(f"  {key}: {value}")
    
    # Clean up sample files
    for file_path in [sample_csv_path, sample_jsonl_path]:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up: {file_path}")

def example_with_adapter():
    """
    Example of loading a model with adapter weights.
    Uncomment and modify paths as needed.
    """
    print("\n=== Adapter Example (Commented) ===")
    print("# Example with adapter - uncomment and modify paths:")
    print("# inference_with_adapter = LLMInference(")
    print("#     base_model_path='unsloth/llama-2-7b-bnb-4bit',")
    print("#     adapter_path='./path/to/your/adapter',  # Your adapter path")
    print("#     load_in_4bit=True")
    print("# )")
    print("# model, tokenizer = inference_with_adapter.load_model()")
    print("# response = inference_with_adapter.generate_response('Your question here')")

def example_file_formats():
    """
    Show expected file formats for CSV and JSONL.
    """
    print("\n=== Expected File Formats ===")
    
    print("\nCSV Format (with 'text' column):")
    print("text,category")
    print("What is AI?,Technology")
    print("How does solar energy work?,Energy")
    
    print("\nJSONL Format (with 'text' key):")
    print('{"text": "What is AI?", "category": "Technology"}')
    print('{"text": "How does solar energy work?", "category": "Energy"}')
    
    print("\nNote: You can specify different column/key names:")
    print("- For CSV: use text_column parameter")
    print("- For JSONL: use text_column parameter (it's the JSON key name)")

if __name__ == "__main__":
    try:
        main()
        example_with_adapter()
        example_file_formats()
        
    except Exception as e:
        print(f"Error running example: {str(e)}")
        print("Make sure you have installed all required dependencies:")
        print("pip install -r requirements.txt")