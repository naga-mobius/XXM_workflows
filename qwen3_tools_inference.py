"""
Qwen3 Tools Inference Script
Specialized script for demonstrating function calling capabilities with real tools.

This script showcases:
- CSV file upload capabilities
- Data ingestion job creation
- Tool validation and execution
- Interactive tool-based workflows

Tools Available:
- upload_csv_file: Upload CSV files to cloud storage
- create_ingestion_job: Create data processing jobs

Usage:
    python qwen3_tools_inference.py
"""

import json
import os
import tempfile
import logging
from datetime import datetime
from llm_inference import LLMInference
from qwen3_tools import (
    upload_csv_file, 
    create_ingestion_job, 
    tool_registry,
    TOOL_DESCRIPTIONS
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model configuration
ADAPTER_PATH = "naga080898/quen3-14b-xlam-fc-v1"
MODEL_PATH = "unsloth/Qwen3-14B"

class ToolInferenceEngine:
    """
    Engine for handling tool-based inference with Qwen3 LoRA adapter.
    """
    
    def __init__(self):
        self.inference = None
        self.tools_prompt = self._create_tools_prompt()
        
    def initialize_model(self):
        """Initialize the Qwen3 model with LoRA adapter."""
        logger.info("Initializing Qwen3 Tools Inference Engine...")
        
        self.inference = LLMInference(
            base_model_path=MODEL_PATH,
            adapter_path=ADAPTER_PATH,
            max_seq_length=4096,
            load_in_4bit=True,
            device="auto"
        )
        
        # Load model
        model, tokenizer = self.inference.load_model()
        logger.info("✅ Model initialized successfully!")
        return self.inference
    
    def _create_tools_prompt(self):
        """Create comprehensive tools prompt for the LLM."""
        tools_for_llm = tool_registry.get_all_tools_for_llm()
        
        return f"""You are an expert AI assistant specialized in data processing and file management. You have access to powerful tools for handling CSV files and creating data ingestion workflows.

AVAILABLE TOOLS:
{json.dumps(tools_for_llm, indent=2)}

FUNCTION CALLING RULES:
1. When users request actions that can be performed with these tools, respond with properly formatted function calls
2. Use this EXACT JSON format for function calls:

```json
{{
    "function": "function_name",
    "parameters": {{
        "parameter1": "value1",
        "parameter2": "value2"
    }}
}}
```

3. Always validate required parameters before suggesting function calls
4. Provide helpful explanations about what each function does
5. For multi-step workflows, break them down clearly

TOOL CAPABILITIES:
- upload_csv_file: Upload CSV files to secure cloud storage and get CDN URLs
- create_ingestion_job: Create automated data processing jobs for uploaded files

Be precise, helpful, and always format function calls correctly."""

    def parse_function_call(self, response):
        """
        Parse and validate function calls from AI response.
        
        Args:
            response (str): AI response containing potential function calls
            
        Returns:
            tuple: (success: bool, function_call: dict, error: str)
        """
        try:
            if "```json" in response:
                # Extract JSON from markdown code block
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
                
                function_call = json.loads(json_str)
                function_name = function_call.get("function")
                parameters = function_call.get("parameters", {})
                
                # Validate function call
                is_valid, missing_params, error_msg = tool_registry.validate_tool_call(
                    function_name, parameters
                )
                
                if is_valid:
                    return True, function_call, None
                else:
                    return False, function_call, error_msg
                    
            return False, {}, "No function call found in response"
            
        except json.JSONDecodeError as e:
            return False, {}, f"Invalid JSON format: {str(e)}"
        except Exception as e:
            return False, {}, f"Parsing error: {str(e)}"
    
    def execute_function_call(self, function_call, simulate=True):
        """
        Execute a validated function call.
        
        Args:
            function_call (dict): Function call dictionary
            simulate (bool): If True, simulate execution; if False, actually execute
            
        Returns:
            tuple: (success: bool, result: any, error: str)
        """
        function_name = function_call.get("function")
        parameters = function_call.get("parameters", {})
        
        try:
            if function_name == "upload_csv_file":
                if simulate:
                    # Simulate upload
                    file_path = parameters.get("file_path", "")
                    simulated_url = f"https://cdn.gov-cloud.ai/simulated/{os.path.basename(file_path)}"
                    return True, simulated_url, None
                else:
                    # Actual upload
                    result = upload_csv_file(**parameters)
                    return True, result, None
                    
            elif function_name == "create_ingestion_job":
                if simulate:
                    # Simulate job creation
                    simulated_job = {
                        "jobId": f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "status": "CREATED",
                        "name": parameters.get("job_name", "simulated_job")
                    }
                    return True, simulated_job, None
                else:
                    # Actual job creation
                    result = create_ingestion_job(**parameters)
                    return True, result, None
                    
            else:
                return False, None, f"Unknown function: {function_name}"
                
        except Exception as e:
            return False, None, f"Execution error: {str(e)}"
    
    def process_user_request(self, user_request, simulate=True):
        """
        Process a user request end-to-end with function calling.
        
        Args:
            user_request (str): User's request
            simulate (bool): Whether to simulate function execution
            
        Returns:
            dict: Processing results
        """
        logger.info(f"Processing request: {user_request}")
        
        # Generate AI response
        response = self.inference.generate_response(
            text=user_request,
            system_prompt=self.tools_prompt,
            custom_generation_config={
                'temperature': 0.1,
                'max_new_tokens': 512,
                'do_sample': False
            }
        )
        
        # Parse function call
        success, function_call, error = self.parse_function_call(response)
        
        result = {
            "user_request": user_request,
            "ai_response": response,
            "function_call_found": success,
            "function_call": function_call,
            "parse_error": error,
            "execution_result": None,
            "execution_error": None
        }
        
        # Execute function if valid
        if success:
            exec_success, exec_result, exec_error = self.execute_function_call(
                function_call, simulate=simulate
            )
            result["execution_result"] = exec_result
            result["execution_error"] = exec_error
            result["execution_success"] = exec_success
        
        return result

def create_sample_csv_file():
    """Create a sample CSV file for testing."""
    sample_data = """id,name,category,price,stock
1,Laptop,Electronics,999.99,50
2,Chair,Furniture,299.99,25
3,Book,Education,19.99,100
4,Phone,Electronics,599.99,75
5,Desk,Furniture,449.99,15"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    temp_file.write(sample_data)
    temp_file.close()
    
    logger.info(f"Created sample CSV file: {temp_file.name}")
    return temp_file.name

def demo_file_upload_workflow():
    """Demonstrate complete file upload and ingestion workflow."""
    print(f"\n{'='*80}")
    print("FILE UPLOAD & INGESTION WORKFLOW DEMO")
    print(f"{'='*80}")
    
    # Initialize engine
    engine = ToolInferenceEngine()
    engine.initialize_model()
    
    # Create sample file
    sample_file = create_sample_csv_file()
    
    try:
        # Step 1: Upload file
        upload_request = f"Please upload the CSV file located at '{sample_file}' to the cloud storage."
        
        print(f"\n📤 STEP 1: File Upload")
        print(f"Request: {upload_request}")
        
        upload_result = engine.process_user_request(upload_request, simulate=True)
        
        print(f"AI Response: {upload_result['ai_response']}")
        if upload_result['function_call_found']:
            print(f"✅ Function Call: {upload_result['function_call']['function']}")
            print(f"   Parameters: {upload_result['function_call']['parameters']}")
            print(f"   Simulated Result: {upload_result['execution_result']}")
        
        # Step 2: Create ingestion job
        if upload_result['execution_result']:
            cdn_url = upload_result['execution_result']
            ingestion_request = f"Create a data ingestion job for the uploaded file at '{cdn_url}' with destination schema '68c41b50f34309622134ee3b' and file type 'CSV'."
            
            print(f"\n📥 STEP 2: Ingestion Job Creation")
            print(f"Request: {ingestion_request}")
            
            ingestion_result = engine.process_user_request(ingestion_request, simulate=True)
            
            print(f"AI Response: {ingestion_result['ai_response']}")
            if ingestion_result['function_call_found']:
                print(f"✅ Function Call: {ingestion_result['function_call']['function']}")
                print(f"   Parameters: {ingestion_result['function_call']['parameters']}")
                print(f"   Simulated Result: {ingestion_result['execution_result']}")
        
    finally:
        # Clean up
        if os.path.exists(sample_file):
            os.remove(sample_file)
            print(f"\n🧹 Cleaned up sample file: {sample_file}")

def demo_interactive_tools():
    """Interactive demo for tool usage."""
    print(f"\n{'='*80}")
    print("INTERACTIVE TOOLS DEMO")
    print(f"{'='*80}")
    
    # Initialize engine
    engine = ToolInferenceEngine()
    engine.initialize_model()
    
    print("\n🤖 I'm ready to help with file uploads and data ingestion!")
    print("Available commands:")
    print("  - Upload a CSV file")
    print("  - Create an ingestion job")
    print("  - Type 'help' for tool information")
    print("  - Type 'quit' to exit")
    
    while True:
        try:
            user_input = input("\n🧑 Your request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
                
            if user_input.lower() == 'help':
                print("\n📚 Available Tools:")
                for tool_name in tool_registry.get_tool_names():
                    tool = tool_registry.get_tool(tool_name)
                    print(f"  • {tool_name}: {tool['description']}")
                continue
                
            if not user_input:
                continue
            
            # Process request
            result = engine.process_user_request(user_input, simulate=True)
            
            print(f"\n🤖 AI Response: {result['ai_response']}")
            
            if result['function_call_found']:
                print(f"\n🔧 Function Call Detected:")
                print(f"   Function: {result['function_call']['function']}")
                print(f"   Parameters: {result['function_call']['parameters']}")
                
                if result['execution_result']:
                    print(f"   ✅ Simulated Result: {result['execution_result']}")
                if result['execution_error']:
                    print(f"   ❌ Error: {result['execution_error']}")
            else:
                if result['parse_error']:
                    print(f"   ⚠️  {result['parse_error']}")
                    
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def demo_batch_tool_requests():
    """Demonstrate batch processing of tool requests."""
    print(f"\n{'='*80}")
    print("BATCH TOOL REQUESTS DEMO")
    print(f"{'='*80}")
    
    # Initialize engine
    engine = ToolInferenceEngine()
    engine.initialize_model()
    
    # Sample requests
    test_requests = [
        "Upload the file at '/data/sales_2024.csv' to the cloud storage",
        "Create an ingestion job for 'https://cdn.gov-cloud.ai/data/customers.csv' with schema 'customer_schema_001' and type 'CSV'",
        "I need to process a CSV file - first upload '/tmp/inventory.csv' then create an ingestion job for it",
        "Help me understand what tools are available for data processing",
        "Upload my file at '/home/user/transactions.csv' with a custom job name 'monthly_transactions'"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n--- Request {i} ---")
        result = engine.process_user_request(request, simulate=True)
        
        print(f"Request: {request}")
        print(f"AI Response: {result['ai_response'][:200]}{'...' if len(result['ai_response']) > 200 else ''}")
        
        if result['function_call_found']:
            print(f"✅ Function: {result['function_call']['function']}")
            print(f"   Valid: ✅")
        else:
            print(f"❌ No valid function call detected")
            if result['parse_error']:
                print(f"   Error: {result['parse_error']}")

def main():
    """Main function to run tool inference demos."""
    print(f"\n{'='*80}")
    print("🛠️  QWEN3 TOOLS INFERENCE DEMONSTRATION")
    print(f"Base Model: {MODEL_PATH}")
    print(f"LoRA Adapter: {ADAPTER_PATH}")
    print(f"{'='*80}")
    
    try:
        # Run demonstrations
        print("\n🎯 Running demonstrations:")
        
        # 1. File upload workflow
        demo_file_upload_workflow()
        
        # 2. Batch tool requests
        demo_batch_tool_requests()
        
        # 3. Interactive mode (optional)
        user_choice = input("\n❓ Would you like to try interactive mode? (y/n): ").lower()
        if user_choice in ['y', 'yes']:
            demo_interactive_tools()
        
        print(f"\n✅ All tool demos completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure sufficient GPU memory for Qwen3-14B")
        print("   2. Check internet connection for model downloads")
        print("   3. Verify dependencies are installed")

if __name__ == "__main__":
    main()
