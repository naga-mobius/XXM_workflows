"""
LLM Class for Fine-tuning with Unsloth Library
Provides methods for loading models, tokenizers, data formatting, 
fine-tuning, and saving adapters to HuggingFace Hub.
"""

import os
import json
import torch
from typing import Dict, List, Optional, Union, Any
from datasets import Dataset, load_dataset
from transformers import (
    AutoTokenizer, 
    TrainingArguments,
    PreTrainedModel,
    PreTrainedTokenizer
)
from unsloth import FastLanguageModel
from trl import SFTTrainer
from huggingface_hub import HfApi, login
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLM:
    """
    A comprehensive LLM class for fine-tuning using Unsloth library.
    
    Features:
    - Fast model and tokenizer loading with Unsloth
    - Data formatting for various training formats
    - Fine-tuning with LoRA adapters
    - Saving and pushing adapters to HuggingFace Hub
    """
    
    def __init__(
        self,
        model_name: str = "unsloth/llama-2-7b-bnb-4bit",
        max_seq_length: int = 2048,
        dtype: Optional[torch.dtype] = None,
        load_in_4bit: bool = True,
        token: Optional[str] = None
    ):
        """
        Initialize the LLM class.
        
        Args:
            model_name (str): HuggingFace model name or path
            max_seq_length (int): Maximum sequence length
            dtype (torch.dtype): Data type for model weights
            load_in_4bit (bool): Whether to load model in 4-bit precision
            token (str): HuggingFace token for authentication
        """
        self.model_name = model_name
        self.max_seq_length = max_seq_length
        self.dtype = dtype
        self.load_in_4bit = load_in_4bit
        self.token = token
        
        self.model: Optional[PreTrainedModel] = None
        self.tokenizer: Optional[PreTrainedTokenizer] = None
        self.trainer: Optional[SFTTrainer] = None
        
        # Set HuggingFace token if provided
        if token:
            login(token=token)
    
    def load_model_and_tokenizer(
        self,
        model_name: Optional[str] = None,
        lora_rank: int = 16,
        lora_alpha: int = 16,
        lora_dropout: float = 0.0,
        target_modules: Optional[List[str]] = None,
        use_gradient_checkpointing: bool = True
    ) -> tuple[PreTrainedModel, PreTrainedTokenizer]:
        """
        Load model and tokenizer using Unsloth for faster processing.
        
        Args:
            model_name (str): Model name to load (overrides instance default)
            lora_rank (int): LoRA rank for fine-tuning
            lora_alpha (int): LoRA alpha parameter
            lora_dropout (float): LoRA dropout rate
            target_modules (List[str]): Target modules for LoRA
            use_gradient_checkpointing (bool): Enable gradient checkpointing
            
        Returns:
            tuple: (model, tokenizer)
        """
        if model_name:
            self.model_name = model_name
            
        logger.info(f"Loading model: {self.model_name}")
        
        try:
            # Load model and tokenizer with Unsloth
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=self.model_name,
                max_seq_length=self.max_seq_length,
                dtype=self.dtype,
                load_in_4bit=self.load_in_4bit,
                token=self.token
            )
            
            # Add LoRA adapters
            self.model = FastLanguageModel.get_peft_model(
                self.model,
                r=lora_rank,
                target_modules=target_modules or [
                    "q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"
                ],
                lora_alpha=lora_alpha,
                lora_dropout=lora_dropout,
                bias="none",
                use_gradient_checkpointing=use_gradient_checkpointing,
                random_state=3407,
                use_rslora=False,
                loftq_config=None
            )
            
            logger.info("Model and tokenizer loaded successfully")
            return self.model, self.tokenizer
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def format_data(
        self,
        dataset: Union[Dataset, List[Dict], str],
        format_type: str = "alpaca",
        instruction_key: str = "instruction",
        input_key: str = "input",
        output_key: str = "output",
        text_key: str = "text"
    ) -> Dataset:
        """
        Format data for training in various formats.
        
        Args:
            dataset: Dataset to format (Dataset object, list of dicts, or path to dataset)
            format_type: Format type ("alpaca", "chat", "completion")
            instruction_key: Key for instruction text
            input_key: Key for input text
            output_key: Key for output text
            text_key: Key for pre-formatted text
            
        Returns:
            Dataset: Formatted dataset
        """
        # Load dataset if string path provided
        if isinstance(dataset, str):
            dataset = load_dataset(dataset, split="train")
        elif isinstance(dataset, list):
            dataset = Dataset.from_list(dataset)
        
        def format_alpaca(example):
            """Format in Alpaca style"""
            instruction = example[instruction_key]
            input_text = example.get(input_key, "")
            output = example[output_key]
            
            if input_text:
                text = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
            else:
                text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
            
            return {"text": text}
        
        def format_chat(example):
            """Format in chat style"""
            instruction = example[instruction_key]
            output = example[output_key]
            
            text = f"<|im_start|>user\n{instruction}<|im_end|>\n<|im_start|>assistant\n{output}<|im_end|>"
            return {"text": text}
        
        def format_completion(example):
            """Format for completion (use existing text or combine fields)"""
            if text_key in example:
                return {"text": example[text_key]}
            else:
                # Combine available fields
                text = f"{example[instruction_key]} {example[output_key]}"
                return {"text": text}
        
        # Apply formatting based on type
        if format_type == "alpaca":
            dataset = dataset.map(format_alpaca)
        elif format_type == "chat":
            dataset = dataset.map(format_chat)
        elif format_type == "completion":
            dataset = dataset.map(format_completion)
        else:
            raise ValueError(f"Unsupported format_type: {format_type}")
        
        logger.info(f"Formatted {len(dataset)} examples in {format_type} format")
        return dataset
    
    def finetune(
        self,
        train_dataset: Dataset,
        output_dir: str = "./results",
        num_train_epochs: int = 1,
        per_device_train_batch_size: int = 2,
        gradient_accumulation_steps: int = 4,
        warmup_steps: int = 5,
        learning_rate: float = 2e-4,
        fp16: bool = True,
        logging_steps: int = 1,
        save_strategy: str = "epoch",
        eval_dataset: Optional[Dataset] = None,
        **kwargs
    ) -> SFTTrainer:
        """
        Fine-tune the model using SFT (Supervised Fine-Tuning).
        
        Args:
            train_dataset: Training dataset
            output_dir: Output directory for checkpoints
            num_train_epochs: Number of training epochs
            per_device_train_batch_size: Batch size per device
            gradient_accumulation_steps: Gradient accumulation steps
            warmup_steps: Number of warmup steps
            learning_rate: Learning rate
            fp16: Whether to use fp16 training
            logging_steps: Steps between logging
            save_strategy: Save strategy ("epoch", "steps", "no")
            eval_dataset: Evaluation dataset (optional)
            **kwargs: Additional training arguments
            
        Returns:
            SFTTrainer: The trainer object
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer must be loaded first")
        
        # Create training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            warmup_steps=warmup_steps,
            learning_rate=learning_rate,
            fp16=fp16,
            logging_steps=logging_steps,
            save_strategy=save_strategy,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            **kwargs
        )
        

        # Create trainer
        self.trainer = SFTTrainer(
            model=self.model,
            tokenizer=self.tokenizer,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            dataset_text_field="text",
            max_seq_length=self.max_seq_length,
            args=training_args,
            packing=False  # Can be True for efficiency but may affect quality
        )
        

        logger.info("Starting fine-tuning...")
        
        # Enable faster training with Unsloth
        FastLanguageModel.for_training(self.model)
        
        # Start training
        self.trainer.train()
        
        logger.info("Fine-tuning completed!")
        return self.trainer
    

    def save_adapters_local(self, save_path: str) -> None:
        """
        Save LoRA adapters locally.
        
        Args:
            save_path: Local path to save adapters
        """
        if self.model is None:
            raise ValueError("Model must be loaded and trained first")
        
        os.makedirs(save_path, exist_ok=True)
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)
        
        logger.info(f"Adapters saved locally to: {save_path}")
    
    def push_to_hub(
        self,
        repo_name: str,
        private: bool = False,
        commit_message: str = "Upload LoRA adapters",
        save_method: str = "lora"  # "lora", "merged_16bit", "merged_4bit"
    ) -> str:
        """
        Save and push LoRA adapters to HuggingFace Hub.
        
        Args:
            repo_name: Repository name on HuggingFace Hub
            private: Whether to make the repository private
            commit_message: Commit message for the push
            save_method: Method to save ("lora", "merged_16bit", "merged_4bit")
            
        Returns:
            str: URL of the uploaded repository
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer must be loaded and trained first")
        
        logger.info(f"Pushing adapters to HuggingFace Hub: {repo_name}")
        
        try:
            if save_method == "lora":
                # Save only LoRA adapters
                self.model.push_to_hub(
                    repo_name,
                    token=self.token,
                    private=private,
                    commit_message=commit_message
                )
                self.tokenizer.push_to_hub(
                    repo_name,
                    token=self.token,
                    private=private,
                    commit_message=commit_message
                )
            
            elif save_method in ["merged_16bit", "merged_4bit"]:
                # Save merged model
                if save_method == "merged_16bit":
                    self.model.save_pretrained_merged(
                        repo_name,
                        self.tokenizer,
                        save_method="merged_16bit",
                        token=self.token,
                        private=private
                    )
                else:
                    self.model.save_pretrained_merged(
                        repo_name,
                        self.tokenizer,
                        save_method="merged_4bit",
                        token=self.token,
                        private=private
                    )
            
            else:
                raise ValueError(f"Unsupported save_method: {save_method}")
            
            hub_url = f"https://huggingface.co/{repo_name}"
            logger.info(f"Successfully pushed to: {hub_url}")
            return hub_url
            
        except Exception as e:
            logger.error(f"Error pushing to hub: {str(e)}")
            raise
    
    def generate_text(
        self,
        prompt: str,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        do_sample: bool = True,
        top_p: float = 0.9,
        **kwargs
    ) -> str:
        """
        Generate text using the fine-tuned model.
        
        Args:
            prompt: Input prompt
            max_new_tokens: Maximum number of new tokens to generate
            temperature: Sampling temperature
            do_sample: Whether to use sampling
            top_p: Top-p sampling parameter
            **kwargs: Additional generation parameters
            
        Returns:
            str: Generated text
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer must be loaded first")
        
        # Enable inference mode
        FastLanguageModel.for_inference(self.model)
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt")
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=do_sample,
                top_p=top_p,
                pad_token_id=self.tokenizer.eos_token_id,
                **kwargs
            )
        
        # Decode and return
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text[len(prompt):]  # Return only the new generated part
    
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dict: Model information
        """
        if self.model is None:
            return {"status": "No model loaded"}
        
        # Count parameters
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        return {
            "model_name": self.model_name,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "trainable_percentage": (trainable_params / total_params) * 100,
            "max_seq_length": self.max_seq_length,
            "dtype": str(self.dtype) if self.dtype else "auto",
            "load_in_4bit": self.load_in_4bit
        }