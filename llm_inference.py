"""
LLM Inference Class
Provides methods for loading base models with adapters and performing inference
on single texts or batch processing from CSV/JSONL files.
"""

import os
import json
import pandas as pd
import torch
from typing import Dict, List, Optional, Union, Any
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    PreTrainedModel,
    PreTrainedTokenizer,
    BitsAndBytesConfig
)
from unsloth import FastLanguageModel
from peft import PeftModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMInference:
    """
    A comprehensive LLM inference class for loading models with adapters and performing inference.
    
    Features:
    - Load base models with optional adapter paths
    - Read CSV and JSONL files with 'text' column
    - Single text inference
    - Batch processing with progress tracking
    - Support for various generation parameters
    """
    
    def __init__(
        self,
        base_model_path: str,
        adapter_path: Optional[str] = None,
        max_seq_length: int = 2048,
        dtype: Optional[torch.dtype] = None,
        load_in_4bit: bool = True,
        device: Optional[str] = None,
        token: Optional[str] = None
    ):
        """
        Initialize the LLM Inference class.
        
        Args:
            base_model_path (str): Path or name of the base model
            adapter_path (str, optional): Path to LoRA adapter weights
            max_seq_length (int): Maximum sequence length for model
            dtype (torch.dtype, optional): Data type for model weights
            load_in_4bit (bool): Whether to load model in 4-bit quantization
            device (str, optional): Device to load model on ('cuda', 'cpu', 'auto')
            token (str, optional): HuggingFace authentication token
        """
        self.base_model_path = base_model_path
        self.adapter_path = adapter_path
        self.max_seq_length = max_seq_length
        self.dtype = dtype
        self.load_in_4bit = load_in_4bit
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.token = token
        
        self.model = None
        self.tokenizer = None
        
        # Generation parameters (can be customized)
        self.generation_config = {
            'max_new_tokens': 512,
            'temperature': 0.7,
            'top_p': 0.9,
            'top_k': 50,
            'do_sample': True,
            'pad_token_id': None,  # Will be set after tokenizer loading
            'eos_token_id': None,  # Will be set after tokenizer loading
            'repetition_penalty': 1.1
        }
        
        logger.info(f"Initialized LLMInference with base model: {base_model_path}")
        if adapter_path:
            logger.info(f"Adapter path: {adapter_path}")
    
    def load_model(self) -> tuple[PreTrainedModel, PreTrainedTokenizer]:
        """
        Load the base model and tokenizer, optionally with adapter weights.
        
        Returns:
            tuple: (model, tokenizer)
        """
        logger.info(f"Loading base model: {self.base_model_path}")
        
        try:
            # Configure quantization with proper CPU offload support
            if self.load_in_4bit and torch.cuda.is_available():
                # Configure 4-bit quantization with CPU offload capability
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    llm_int8_enable_fp32_cpu_offload=True  # Enable CPU offload for insufficient GPU memory
                )
                
                device_map = "auto"  # Automatic device mapping
                
                # Configure memory limits for better memory management
                max_memory = {}
                if torch.cuda.is_available():
                    # Get available GPU memory and reserve some for overhead
                    gpu_memory = torch.cuda.get_device_properties(0).total_memory
                    # Use 90% of available GPU memory to leave room for operations
                    max_gpu_memory = int(gpu_memory * 0.9 / (1024**3))  # Convert to GB
                    max_memory = {
                        f"cuda:{torch.cuda.current_device()}": f"{max_gpu_memory}GiB",
                        "cpu": "32GiB"  # Allow substantial CPU memory for offloading
                    }
                    logger.info(f"Configured memory limits: {max_memory}")
                
                logger.info("Using 4-bit quantization with CPU offload support")
                
                # Try Unsloth first for faster loading
                try:
                    self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                        model_name=self.base_model_path,
                        max_seq_length=self.max_seq_length,
                        dtype=self.dtype,
                        load_in_4bit=self.load_in_4bit,
                        token=self.token,
                        device_map=device_map
                    )
                    logger.info("Successfully loaded model using Unsloth")
                except Exception as unsloth_error:
                    logger.warning(f"Unsloth loading failed: {unsloth_error}")
                    logger.info("Falling back to transformers AutoModel with proper quantization config")
                    
                    # Fallback to transformers with proper quantization config
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.base_model_path,
                        quantization_config=quantization_config,
                        device_map=device_map,
                        max_memory=max_memory if max_memory else None,
                        torch_dtype=self.dtype or torch.float16,
                        token=self.token,
                        trust_remote_code=True
                    )
                    
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.base_model_path,
                        token=self.token,
                        trust_remote_code=True
                    )
                    
            else:
                # Load without quantization
                logger.info("Loading model without quantization")
                self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                    model_name=self.base_model_path,
                    max_seq_length=self.max_seq_length,
                    dtype=self.dtype,
                    load_in_4bit=False,
                    token=self.token
                )
            
            # Load adapter if specified
            if self.adapter_path:
                logger.info(f"Loading adapter from: {self.adapter_path}")
                self.model = PeftModel.from_pretrained(
                    self.model, 
                    self.adapter_path,
                    token=self.token
                )
                logger.info("Adapter loaded successfully")
            
            # Set up for inference - only use FastLanguageModel.for_inference if loaded with Unsloth
            try:
                FastLanguageModel.for_inference(self.model)
                logger.info("Model configured for inference using Unsloth")
            except Exception as e:
                logger.info(f"Setting eval mode manually (not using Unsloth): {e}")
                self.model.eval()  # Fallback to standard eval mode
            
            # Update generation config with tokenizer-specific tokens
            self.generation_config['pad_token_id'] = self.tokenizer.pad_token_id
            self.generation_config['eos_token_id'] = self.tokenizer.eos_token_id
            
            # Set pad_token if not available
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.generation_config['pad_token_id'] = self.tokenizer.eos_token_id
            
            logger.info("Model and tokenizer loaded successfully")
            return self.model, self.tokenizer
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def read_csv_file(self, file_path: str, text_column: str = 'text') -> List[str]:
        """
        Read a CSV file and extract text data from specified column.
        
        Args:
            file_path (str): Path to the CSV file
            text_column (str): Name of the column containing text data
            
        Returns:
            List[str]: List of text strings from the specified column
        """
        try:
            logger.info(f"Reading CSV file: {file_path}")
            df = pd.read_csv(file_path)
            
            if text_column not in df.columns:
                raise ValueError(f"Column '{text_column}' not found in CSV. Available columns: {list(df.columns)}")
            
            texts = df[text_column].dropna().astype(str).tolist()
            logger.info(f"Successfully read {len(texts)} texts from CSV")
            return texts
            
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise
    
    def read_jsonl_file(self, file_path: str, text_key: str = 'text') -> List[str]:
        """
        Read a JSONL file and extract text data from specified key.
        
        Args:
            file_path (str): Path to the JSONL file
            text_key (str): Key name containing text data in each JSON object
            
        Returns:
            List[str]: List of text strings from the specified key
        """
        try:
            logger.info(f"Reading JSONL file: {file_path}")
            texts = []
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        if text_key in data:
                            texts.append(str(data[text_key]))
                        else:
                            logger.warning(f"Line {line_num}: Key '{text_key}' not found in JSON object")
                    except json.JSONDecodeError as e:
                        logger.warning(f"Line {line_num}: Invalid JSON - {str(e)}")
            
            logger.info(f"Successfully read {len(texts)} texts from JSONL")
            return texts
            
        except Exception as e:
            logger.error(f"Error reading JSONL file: {str(e)}")
            raise
    
    def generate_response(
        self, 
        text: str, 
        system_prompt: Optional[str] = None,
        custom_generation_config: Optional[Dict] = None
    ) -> str:
        """
        Generate a response for a single input text.
        
        Args:
            text (str): Input text to generate response for
            system_prompt (str, optional): System prompt to prepend
            custom_generation_config (Dict, optional): Custom generation parameters
            
        Returns:
            str: Generated response text
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Prepare input text
        if system_prompt:
            formatted_text = f"{system_prompt}\n\n{text}"
        else:
            formatted_text = text
        
        # Tokenize input
        inputs = self.tokenizer(
            formatted_text,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_seq_length,
            padding=True
        ).to(self.device)
        
        # Merge custom generation config
        generation_config = self.generation_config.copy()
        if custom_generation_config:
            generation_config.update(custom_generation_config)
        
        try:
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    **generation_config
                )
            
            # Decode response (exclude input tokens)
            input_length = inputs["input_ids"].shape[1]
            response_tokens = outputs[0][input_length:]
            response = self.tokenizer.decode(response_tokens, skip_special_tokens=True)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            raise
    
    def batch_inference(
        self, 
        texts: List[str], 
        system_prompt: Optional[str] = None,
        custom_generation_config: Optional[Dict] = None,
        show_progress: bool = True
    ) -> List[str]:
        """
        Perform batch inference on a list of texts.
        
        Args:
            texts (List[str]): List of input texts
            system_prompt (str, optional): System prompt to prepend to each text
            custom_generation_config (Dict, optional): Custom generation parameters
            show_progress (bool): Whether to show progress logging
            
        Returns:
            List[str]: List of generated responses
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        responses = []
        total_texts = len(texts)
        
        logger.info(f"Starting batch inference for {total_texts} texts")
        
        for i, text in enumerate(texts):
            try:
                response = self.generate_response(
                    text, 
                    system_prompt=system_prompt,
                    custom_generation_config=custom_generation_config
                )
                responses.append(response)
                
                if show_progress and (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{total_texts} texts")
                    
            except Exception as e:
                logger.error(f"Error processing text {i + 1}: {str(e)}")
                responses.append(f"Error: {str(e)}")
        
        logger.info(f"Batch inference completed. Processed {len(responses)}/{total_texts} texts")
        return responses
    
    def inference_from_file(
        self, 
        file_path: str, 
        output_path: Optional[str] = None,
        text_column: str = 'text',
        system_prompt: Optional[str] = None,
        custom_generation_config: Optional[Dict] = None
    ) -> List[str]:
        """
        Perform inference on texts from a CSV or JSONL file.
        
        Args:
            file_path (str): Path to input file (CSV or JSONL)
            output_path (str, optional): Path to save results (CSV format)
            text_column (str): Column/key name for text data
            system_prompt (str, optional): System prompt to prepend
            custom_generation_config (Dict, optional): Custom generation parameters
            
        Returns:
            List[str]: List of generated responses
        """
        # Determine file type and read texts
        if file_path.lower().endswith('.csv'):
            texts = self.read_csv_file(file_path, text_column)
        elif file_path.lower().endswith('.jsonl'):
            texts = self.read_jsonl_file(file_path, text_column)
        else:
            raise ValueError("File must be CSV (.csv) or JSONL (.jsonl)")
        
        # Perform batch inference
        responses = self.batch_inference(
            texts, 
            system_prompt=system_prompt,
            custom_generation_config=custom_generation_config
        )
        
        # Save results if output path specified
        if output_path:
            self.save_results(texts, responses, output_path)
        
        return responses
    
    def save_results(self, inputs: List[str], outputs: List[str], output_path: str):
        """
        Save inference results to a CSV file.
        
        Args:
            inputs (List[str]): Original input texts
            outputs (List[str]): Generated responses
            output_path (str): Path to save the results
        """
        try:
            results_df = pd.DataFrame({
                'input_text': inputs,
                'generated_response': outputs
            })
            
            results_df.to_csv(output_path, index=False)
            logger.info(f"Results saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise
    
    def update_generation_config(self, **kwargs):
        """
        Update the default generation configuration.
        
        Args:
            **kwargs: Generation parameters to update
        """
        self.generation_config.update(kwargs)
        logger.info(f"Updated generation config: {kwargs}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dict[str, Any]: Model information including parameters, memory usage, etc.
        """
        if self.model is None:
            return {"status": "Model not loaded"}
        
        info = {
            "base_model_path": self.base_model_path,
            "adapter_path": self.adapter_path,
            "model_type": type(self.model).__name__,
            "device": str(self.device),
            "max_seq_length": self.max_seq_length,
            "generation_config": self.generation_config.copy()
        }
        
        try:
            # Get parameter count
            total_params = sum(p.numel() for p in self.model.parameters())
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            
            info.update({
                "total_parameters": total_params,
                "trainable_parameters": trainable_params,
                "trainable_percentage": f"{100 * trainable_params / total_params:.2f}%"
            })
        except Exception as e:
            logger.warning(f"Could not get parameter info: {str(e)}")
        
        return info
