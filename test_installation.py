#!/usr/bin/env python3
"""
Test script to verify XXM Workflows installation
This script checks if the package can be imported and basic functionality works.
"""

import sys
import traceback

def test_imports():
    """Test if main modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        # Test package import
        import xxm_workflows
        print(f"✅ Package import successful: xxm_workflows v{xxm_workflows.__version__}")
        
        # Test main classes
        from xxm_workflows import LLM, LLMInference
        print("✅ Main classes imported successfully")
        
        # Test individual modules
        from llm_trainer import LLM as TrainerLLM
        from llm_inference import LLMInference as InferenceLLM
        print("✅ Individual modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return False

def test_class_initialization():
    """Test if classes can be initialized."""
    print("\n🔧 Testing class initialization...")
    
    try:
        from xxm_workflows import LLM, LLMInference
        
        # Test LLM initialization (without loading model)
        llm = LLM(
            model_name="unsloth/llama-2-7b-bnb-4bit",
            max_seq_length=512,
            load_in_4bit=True
        )
        print("✅ LLM class initialization successful")
        
        # Test LLMInference initialization (without loading model)
        inference = LLMInference(
            base_model_path="unsloth/llama-2-7b-bnb-4bit",
            max_seq_length=512,
            load_in_4bit=True
        )
        print("✅ LLMInference class initialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        traceback.print_exc()
        return False

def test_dependencies():
    """Test if required dependencies are available."""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("datasets", "Datasets"),
        ("pandas", "Pandas"),
        ("peft", "PEFT"),
        ("trl", "TRL"),
        ("unsloth", "Unsloth"),
        ("huggingface_hub", "HuggingFace Hub")
    ]
    
    missing_deps = []
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} available")
        except ImportError:
            print(f"❌ {name} not available")
            missing_deps.append(name)
        except Exception as e:
            print(f"⚠️  {name} import warning: {e}")
    
    if missing_deps:
        print(f"\n💡 Missing dependencies: {', '.join(missing_deps)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    return True

def test_file_operations():
    """Test file reading functionality."""
    print("\n📄 Testing file operations...")
    
    try:
        from xxm_workflows import LLMInference
        import pandas as pd
        import json
        import tempfile
        import os
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name
            df = pd.DataFrame({'text': ['Test 1', 'Test 2'], 'label': ['A', 'B']})
            df.to_csv(csv_path, index=False)
        
        # Create temporary JSONL file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            jsonl_path = f.name
            f.write(json.dumps({'text': 'Test 1', 'label': 'A'}) + '\n')
            f.write(json.dumps({'text': 'Test 2', 'label': 'B'}) + '\n')
        
        # Test file reading
        inference = LLMInference("dummy/path", load_in_4bit=True)
        
        csv_texts = inference.read_csv_file(csv_path)
        print(f"✅ CSV reading successful: {len(csv_texts)} texts")
        
        jsonl_texts = inference.read_jsonl_file(jsonl_path)
        print(f"✅ JSONL reading successful: {len(jsonl_texts)} texts")
        
        # Cleanup
        os.unlink(csv_path)
        os.unlink(jsonl_path)
        
        return True
        
    except Exception as e:
        print(f"❌ File operations error: {e}")
        traceback.print_exc()
        return False

def test_package_info():
    """Test package information functions."""
    print("\n📋 Testing package information...")
    
    try:
        import xxm_workflows
        
        # Test package info
        info = xxm_workflows.get_package_info()
        print(f"✅ Package info: {info['name']} v{info['version']}")
        
        # Test print function
        print("✅ Package info display:")
        xxm_workflows.print_package_info()
        
        return True
        
    except Exception as e:
        print(f"❌ Package info error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 XXM Workflows Installation Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Dependency Test", test_dependencies),
        ("Initialization Test", test_class_initialization),
        ("File Operations Test", test_file_operations),
        ("Package Info Test", test_package_info)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Installation is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())