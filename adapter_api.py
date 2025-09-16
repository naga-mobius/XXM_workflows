from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any





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


# def upload_csv_file(file_path):
#     url = "https://igs.gov-cloud.ai/mobius-content-service/v1.0/content/upload?filePathAccess=private&filePath=%2Fbottle%2Flimka%2Fsoda%2F"

#     payload = {}
#     files=[
#     ('file',('sample.csv',open(file_path,'rb'),'text/csv'))
#     ]
#     headers = {
#     'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3Ny1NUVdFRTNHZE5adGlsWU5IYmpsa2dVSkpaWUJWVmN1UmFZdHl5ejFjIn0.eyJleHAiOjE3NTMzOTM3MzksImlhdCI6MTc1MzM1NzczOSwianRpIjoiYjEwMWFjYWMtOWY4Ni00MTQ0LTkyMTItYTE1YmJmYWFiMDIyIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXNlcnZpY2Uua2V5Y2xvYWsuc3ZjLmNsdXN0ZXIubG9jYWw6ODA4MC9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbIkJPTFRaTUFOTl9CT1RfbW9iaXVzIiwiUEFTQ0FMX0lOVEVMTElHRU5DRV9tb2JpdXMiLCJNT05FVF9tb2JpdXMiLCJWSU5DSV9tb2JpdXMiLCJhY2NvdW50Il0sInN1YiI6IjJjZjc2ZTVmLTI2YWQtNGYyYy1iY2NjLWY0YmMxZTdiZmI2NCIsInR5cCI6IkJlYXJlciIsImF6cCI6IkhPTEFDUkFDWV9tb2JpdXMiLCJzaWQiOiJiNDI0NmFiNy0zNGIzLTRlZjctYmY1OS03NTYzODA0MDFkMTAiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc3JlX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2JyX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2RjZHJfYWRtaW4iLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfQWxlcnRzX1JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2RfZXhlY3V0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfZXhlY3V0ZSIsIjllNzYxYjc4LTY4YjgtNDE2Ny04MjNhLWlwMV90ZXN0X2N1c3RvbV9wcm9kdWN0X3JvbGUxMjM0NTYiLCJ1bWFfYXV0aG9yaXphdGlvbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9kY2RyX2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfYnJfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9rOHNfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9DdXN0b21lcl9Xcml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jaV93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9zcmVfd3JpdGUiLCIwYmM0OWZhZC05MTIzLTRjYWItYWI5YS0wNTU2Nzk2MDBkMjhfYzFhNzU2NjctYjM1ZC00NmNhLWJkNGEtZDk1NGY1YmIyY2Y5X3Rlc3Ricl9yZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2RjZHJfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9BcHByb3ZhbHNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfUm9sZXNfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9BbGVydHNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfazhzX3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2lhY19hZG1pbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Qb2xpY2llc19SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2NkX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2NpX3JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfSW5mcmFfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfUm9sZXNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc3JlX2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfSW5mcmFfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9kY2RyX3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX0xvZ3NfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9rOHNfZXhlY3V0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9UZWFtX1dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2RfcmVhZCIsIm9mZmxpbmVfYWNjZXNzIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1BvbGljaWVzX1dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1Byb2plY3RfV3JpdGUiLCJtb2JpdXNfZDBmNTJiMGUtMzZkNy00ODUzLTg4NjAtNmQyMWE5YTkyMGE1X0FCQ0QiLCJkZWZhdWx0LXJvbGVzLW1hc3RlciIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9DdXN0b21lcl9SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1RlYW1fUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9icl9leGVjdXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2s4c19hZG1pbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Qcm9qZWN0X1JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfTG9nc19Xcml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jZF93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9icl93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9zcmVfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Vc2VyX1dyaXRlIiwiOWU3NjFiNzgtNjhiOC00MTY3LTgyM2EtaXAxX2YwYzFiODkzLWRjYTYtNGRkMS05MjI5LWlwMV90ZXN0X2N1c3RvbV9wcm9kdWN0X3JvbGUxMjM0NSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfd3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2lfYWRtaW4iLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc2VjdXJpdHlfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jaV9leGVjdXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX0FwcHJvdmFsc19SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1VzZXJfUmVhZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7IkJPTFRaTUFOTl9CT1RfbW9iaXVzIjp7InJvbGVzIjpbIkJPTFRaTUFOTl9CT1RfVVNFUiIsIkJPTFRaTUFOTl9CT1RfQURNSU4iXX0sIkhPTEFDUkFDWV9tb2JpdXMiOnsicm9sZXMiOlsiSE9MQUNSQUNZX1VTRVIiXX0sIlBBU0NBTF9JTlRFTExJR0VOQ0VfbW9iaXVzIjp7InJvbGVzIjpbIlBBU0NBTF9JTlRFTExJR0VOQ0VfQ09OU1VNRVIiLCJQQVNDQUxfSU5URUxMSUdFTkNFX1VTRVIiLCJQQVNDQUxfSU5URUxMSUdFTkNFX0FETUlOIiwiU0NIRU1BX1JFQUQiXX0sIk1PTkVUX21vYml1cyI6eyJyb2xlcyI6WyJNT05FVF9BUFBST1ZFIiwiTU9ORVRfVVNFUiJdfSwiVklOQ0lfbW9iaXVzIjp7InJvbGVzIjpbIlZJTkNJX1VTRVIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInJlcXVlc3RlclR5cGUiOiJURU5BTlQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFpZHRhYXMgQWlkdGFhcyIsInRlbmFudElkIjoiMmNmNzZlNWYtMjZhZC00ZjJjLWJjY2MtZjRiYzFlN2JmYjY0IiwicGxhdGZvcm1JZCI6Im1vYml1cyIsInByZWZlcnJlZF91c2VybmFtZSI6InBhc3N3b3JkX3RlbmFudF9haWR0YWFzQGdhaWFuc29sdXRpb25zLmNvbSIsImdpdmVuX25hbWUiOiJBaWR0YWFzIiwiZmFtaWx5X25hbWUiOiJBaWR0YWFzIiwiZW1haWwiOiJwYXNzd29yZF90ZW5hbnRfYWlkdGFhc0BnYWlhbnNvbHV0aW9ucy5jb20iLCJwbGF0Zm9ybXMiOnsicm9sZXMiOlsiU0NIRU1BX1JFQUQiXX19.aU1Qq-zNiasF7cMvDKjxye4AJDauKYj-2bKNjTtSkIgTGlE4Tqxl69wNBrZBZix-6l8d9nnuvD85WMJIH9MyK6U5g_Q8HxCz2l8z3InWO-k6i_8Gp8U1AEVTxMlTYNjp_vL3WooNpLulLaE71Bp58GgO4IZzalCh7zmkTtaNzZGanQsAXObMrxisRp3VlSak5MX2KfRFNSLlFAEXLt_7NdNKjSZAZ5c-i5X2WJm0rijSz0_0pKJ9NR_mJ0vCPnRgOxZnfNsdXRz988FS_QC6ZzWthkE59WTC1W56PmDPACMV2HzrAK6Iq8lVWRp2UL1V_fFH6FJ2xFacTKDClkOXfw'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload, files=files)
#     response = response.json()
#     cdn_url = response.get('cdnUrl')
#     cdn_url = "https://cdn.gov-cloud.ai"+cdn_url
#     return cdn_url

    
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
            device="cuda"
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
2. Strictly Use this EXACT JSON format for function calls:

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

WHEN TO USE EACH TOOL:

📤 USE upload_csv_file WHEN:
- User wants to upload a CSV file from their local system
- User mentions a file path they want to upload
- User needs to make a local CSV file accessible via CDN/cloud
- This is typically the FIRST step in any data processing workflow
- Examples: "Upload my sales.csv file", "Upload the data at /path/to/file.csv"

📥 USE create_ingestion_job WHEN:
- User wants to process an already uploaded CSV file
- User has a CDN URL and wants to create a data processing job
- User mentions creating workflows, jobs, or ingestion processes
- This is typically the SECOND step, after a file is uploaded
- User provides destination schemas or database configurations
- Examples: "Create an ingestion job for this uploaded file", "Process the CSV at this URL"

TYPICAL WORKFLOW:
1. First: upload_csv_file (local file → CDN URL)
2. Then: create_ingestion_job (CDN URL → processed data)

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
                
                if function_name:
                    return True, function_call, None
                else:
                    return False, function_call, error_msg
                    
            return False, {}, "No function call found in response"
            
        except json.JSONDecodeError as e:
            return False, {}, f"Invalid JSON format: {str(e)}"
        except Exception as e:
            return False, {}, f"Parsing error: {str(e)}"
    
    def execute_function_call(self, function_call, simulate=False):
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
        logger.info(f"the function is {function_name}")
        logger.info(f"the parameters are {parameters}")
        # try:
        if function_name == "upload_csv_file":
            if simulate:
                # Simulate upload
                logger.info("the tool simulation is happening")
                file_path = parameters.get("file_path", "")
                simulated_url = f"https://cdn.gov-cloud.ai/simulated/{os.path.basename(file_path)}"
                return True, simulated_url, None
            else:
                # Actual upload
                logger.info("The actual tool is called")
                logger.info(f"the parameters passed for upload_csv are {parameters}")
                result = upload_csv_file(**parameters)
                logger.info(f"the cdn_url is {result}")
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
                
        # except Exception as e:
        #     return False, None, f"Execution error: {str(e)}"

    def process_user_request(self, user_request, simulate=False):
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
                'temperature': 0.7,
                'max_new_tokens': 512,
                'do_sample': False
            }
        )

        # try:
        #     logger.info(f"the response is {response}")
        # except:
        #     logger.info(response.json())
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
        # logger.info(f"the overall response is {result}")
        logger.info(f"the function call is {function_call}")
        # Execute function if valid
        
        if success:
            logger.info(f"the tool execution is happening")
            exec_success, exec_result, exec_error = self.execute_function_call(
                function_call, simulate=simulate
            )
            result["execution_result"] = exec_result
            result["execution_error"] = exec_error
            result["execution_success"] = exec_success
        
        return result




from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import uvicorn

app = FastAPI()

# Input schema for request body
class InferenceRequest(BaseModel):
    input: Any  # change to str/dict depending on your needs

# Your function
def qwen3_fc_adapter_inference(user_input):
    engine = ToolInferenceEngine()
    engine.initialize_model()
    upload_result = engine.process_user_request(user_input, simulate=False)
    return upload_result['execution_result']

# FastAPI route
@app.post("/inference")
def inference(request: InferenceRequest):
    result = qwen3_fc_adapter_inference(request.input)
    return {"result": result}

# Run with uvicorn inside the same file
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
