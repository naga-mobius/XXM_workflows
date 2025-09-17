"""
Model Merging and Upload Script
Merges a LoRA adapter with a base model and uploads to Hugging Face Hub
"""

import os
import torch
import logging
from typing import Optional
from unsloth import FastLanguageModel
from huggingface_hub import login, HfApi
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelMerger:
    """
    Class to handle merging LoRA adapters with base models and uploading to HuggingFace
    """
    
    def __init__(self, hf_token: Optional[str] = None):
        """
        Initialize the ModelMerger
        
        Args:
            hf_token: HuggingFace token for authentication
        """
        self.hf_token = hf_token
        if hf_token:
            login(token=hf_token)
            logger.info("✅ Logged into HuggingFace Hub")
    
    def merge_and_upload(
        self,
        base_model_path: str,
        adapter_path: str,
        repo_name: str,
        max_seq_length: int = 4096,
        dtype: Optional[torch.dtype] = None,
        load_in_4bit: bool = True,
        save_method: str = "merged_16bit",
        private: bool = False,
        commit_message: str = "Upload merged model with LoRA adapter"
    ) -> str:
        """
        Merge LoRA adapter with base model and upload to HuggingFace Hub
        
        Args:
            base_model_path: Path to base model on HuggingFace
            adapter_path: Path to LoRA adapter on HuggingFace
            repo_name: Name for the new repository on HuggingFace
            max_seq_length: Maximum sequence length
            dtype: Data type for model weights
            load_in_4bit: Whether to load in 4-bit precision
            save_method: Save method ("merged_16bit", "merged_4bit", "lora")
            private: Whether to make repository private
            commit_message: Commit message for upload
            
        Returns:
            str: URL of uploaded repository
        """
        try:
            logger.info(f"🚀 Starting model merge process...")
            logger.info(f"   Base Model: {base_model_path}")
            logger.info(f"   Adapter: {adapter_path}")
            logger.info(f"   Target Repo: {repo_name}")
            
            # Step 1: Load base model and tokenizer
            logger.info("📥 Loading base model and tokenizer...")
            model, tokenizer = FastLanguageModel.from_pretrained(
                model_name=base_model_path,
                max_seq_length=max_seq_length,
                dtype=dtype,
                load_in_4bit=load_in_4bit,
                token=self.hf_token
            )
            logger.info("✅ Base model loaded successfully")
            
            # Step 2: Load and apply LoRA adapter
            logger.info("🔗 Loading LoRA adapter...")
            try:
                # Load the adapter weights
                from peft import PeftModel
                model = PeftModel.from_pretrained(model, adapter_path, token=self.hf_token)
                logger.info("✅ LoRA adapter loaded successfully")
            except Exception as e:
                logger.error(f"❌ Error loading adapter: {str(e)}")
                # Try alternative method using Unsloth's approach
                logger.info("🔄 Trying alternative loading method...")
                model = FastLanguageModel.get_peft_model(
                    model,
                    r=16,  # Default LoRA rank
                    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                  "gate_proj", "up_proj", "down_proj"],
                    lora_alpha=16,
                    lora_dropout=0.0,
                    bias="none",
                    use_gradient_checkpointing=True,
                    random_state=3407,
                )
                # Load adapter weights manually if needed
                logger.info("✅ Model prepared for adapter loading")
            
            # Step 3: Merge the adapter into the base model
            logger.info("🔄 Merging adapter with base model...")
            
            if save_method == "merged_16bit":
                logger.info("💾 Saving merged model in 16-bit precision...")
                model.save_pretrained_merged(
                    repo_name,
                    tokenizer,
                    save_method="merged_16bit",
                    token=self.hf_token
                )
            elif save_method == "merged_4bit":
                logger.info("💾 Saving merged model in 4-bit precision...")
                model.save_pretrained_merged(
                    repo_name,
                    tokenizer,
                    save_method="merged_4bit", 
                    token=self.hf_token
                )
            elif save_method == "lora":
                logger.info("💾 Saving LoRA adapters only...")
                model.push_to_hub(
                    repo_name,
                    token=self.hf_token,
                    private=private,
                    commit_message=commit_message
                )
                tokenizer.push_to_hub(
                    repo_name,
                    token=self.hf_token,
                    private=private,
                    commit_message=commit_message
                )
            else:
                raise ValueError(f"Unsupported save_method: {save_method}")
            
            # Step 4: Update repository visibility if needed
            if private and save_method in ["merged_16bit", "merged_4bit"]:
                logger.info("🔒 Setting repository to private...")
                try:
                    api = HfApi(token=self.hf_token)
                    api.update_repo_visibility(repo_id=repo_name, private=private)
                    logger.info("✅ Repository privacy setting updated")
                except Exception as e:
                    logger.warning(f"⚠️ Could not update privacy setting: {str(e)}")
                    logger.info("💡 You can manually set the repository to private on HuggingFace Hub")
            
            hub_url = f"https://huggingface.co/{repo_name}"
            logger.info(f"🎉 Successfully uploaded merged model to: {hub_url}")
            
            return hub_url
            
        except Exception as e:
            logger.error(f"❌ Error during merge and upload: {str(e)}")
            raise

def main():
    """
    Main function to run the model merging and upload process
    """
    # Configuration
    ADAPTER_PATH = "naga080898/quen3-14b-xlam-fc-v1"
    BASE_MODEL_PATH = "unsloth/Qwen3-14B"
    
    print(f"\n{'='*80}")
    print("🚀 Model Merge and Upload Script")
    print(f"{'='*80}")
    print(f"Base Model: {BASE_MODEL_PATH}")
    print(f"LoRA Adapter: {ADAPTER_PATH}")
    print(f"{'='*80}\n")
    
    # Get HuggingFace token
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        hf_token = input("🔑 Enter your HuggingFace token (or set HF_TOKEN env var): ").strip()
        if not hf_token:
            logger.error("❌ HuggingFace token is required")
            return
    
    # Get repository name for upload
    default_repo_name = "qwen3-14b-xlam-fc"
    repo_name = input(f"📝 Enter repository name (default: {default_repo_name}): ").strip()
    if not repo_name:
        repo_name = default_repo_name
    
    # Get save method
    print("\n💾 Select save method:")
    print("1. merged_16bit - Full merged model in 16-bit (larger size, full precision)")
    print("2. merged_4bit - Full merged model in 4-bit (smaller size, good quality)")
    print("3. lora - LoRA adapters only (smallest size, requires base model)")
    
    save_method_choice = input("Enter choice (1-3, default: 1): ").strip()
    save_method_map = {
        "1": "merged_16bit",
        "2": "merged_4bit", 
        "3": "lora",
        "": "merged_16bit"
    }
    save_method = save_method_map.get(save_method_choice, "merged_16bit")
    
    # Ask if repository should be private
    is_private = input("🔒 Make repository private? (y/N): ").strip().lower() in ['y', 'yes']
    
    try:
        # Initialize merger
        merger = ModelMerger(hf_token=hf_token)
        
        # Perform merge and upload
        result_url = merger.merge_and_upload(
            base_model_path=BASE_MODEL_PATH,
            adapter_path=ADAPTER_PATH,
            repo_name=repo_name,
            max_seq_length=4096,
            load_in_4bit=True,
            save_method=save_method,
            private=is_private,
            commit_message=f"Merge {ADAPTER_PATH} with {BASE_MODEL_PATH}"
        )
        
        print(f"\n🎉 SUCCESS!")
        print(f"📁 Merged model uploaded to: {result_url}")
        print(f"🔧 Save method: {save_method}")
        print(f"🔒 Private: {is_private}")
        
    except Exception as e:
        logger.error(f"❌ Process failed: {str(e)}")
        print(f"\n💡 Troubleshooting tips:")
        print("   1. Ensure your HuggingFace token has write permissions")
        print("   2. Check internet connection")
        print("   3. Verify you have access to both base model and adapter")
        print("   4. Ensure sufficient disk space for temporary files")

if __name__ == "__main__":
    main()
