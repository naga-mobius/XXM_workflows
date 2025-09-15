# XXM Workflows - CSV Data Ingestion with Qwen3

A streamlined package for CSV data processing and ingestion using Qwen3 with unsloth optimization.

## 🚀 Features

- **CSV Upload & Validation**: Robust CSV file processing with comprehensive validation
- **Data Ingestion Jobs**: Automated data quality analysis and processing workflows  
- **Qwen3 Integration**: Built for the latest Qwen3-14B model with thinking mode support
- **Data Quality Analysis**: Automatic completeness, uniqueness, and consistency checks
- **Custom Validation Rules**: Flexible validation framework for data requirements
- **Clean API**: Simple, focused interface for data processing tasks

## 📦 Installation

### Quick Install
```bash
git clone <repository-url>
cd XXM_workflows
pip install -e .
```

### Dependencies
```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

### CSV Upload
```python
from qwen3_tools import get_data_tools

# Get the data tools
tools = get_data_tools()

# Upload and validate CSV
result = tools.execute_tool("upload_csv", {
    "file_path": "your_data.csv"
})

if result.success:
    print(f"Uploaded {result.result['data_summary']['rows']} rows")
    print(f"Columns: {result.result['data_summary']['column_names']}")
else:
    print(f"Upload failed: {result.error}")
```

### Data Ingestion Job
```python
# Start comprehensive data ingestion
validation_rules = {
    "required_columns": ["id", "name"],
    "min_rows": 100,
    "max_null_percentage": 5
}

result = tools.execute_tool("start_data_ingestion_job", {
    "file_path": "your_data.csv",
    "job_name": "monthly_sales_analysis",
    "validation_rules": validation_rules
})

if result.success:
    job = result.result
    print(f"Job completed: {job['job_id']}")
    print(f"Data quality score: {job['data_quality']['overall_score']}%")
else:
    print(f"Job failed: {result.error}")
```

## 📚 Core Tools

### upload_csv
Upload and validate CSV files with detailed analysis:
- File validation and encoding detection
- Data type analysis
- Missing value detection
- Memory usage calculation
- Data preview generation

### start_data_ingestion_job
Run comprehensive data ingestion workflows:
- Custom validation rules
- Data quality scoring
- Outlier detection
- Selective column processing
- Job tracking and management

## 🛠 Available Features

### Data Quality Analysis
- **Completeness**: Null value analysis by column and overall
- **Uniqueness**: Duplicate detection and uniqueness scoring
- **Consistency**: Type validation and outlier detection
- **Overall Score**: Composite quality metric

### Validation Rules
```python
validation_rules = {
    "required_columns": ["id", "timestamp", "value"],
    "min_rows": 1000,
    "max_null_percentage": 10,
    "expected_types": {
        "id": "int",
        "value": "float"
    }
}
```

### Selective Processing
```python
# Process only specific columns
result = tools.execute_tool("start_data_ingestion_job", {
    "file_path": "large_dataset.csv",
    "target_columns": ["customer_id", "transaction_amount", "date"],
    "job_name": "financial_analysis"
})
```

## 📖 Example Usage

Run the comprehensive example:
```bash
python csv_ingestion_example.py
```

This demonstrates:
- CSV file upload and validation
- Data quality analysis
- Custom validation rules
- Selective column processing
- Job management workflow

## 🧪 Testing

```bash
# Test the tools module
python qwen3_tools.py

# Run the complete example
python csv_ingestion_example.py
```

## 📋 Project Structure

```
XXM_workflows/
├── qwen3_tools.py              # Core data processing tools
├── csv_ingestion_example.py    # Usage examples
├── llm_inference.py            # Base inference class
├── llm_trainer.py              # Training utilities
├── setup.py                    # Package configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🔧 Requirements

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.21.0
- unsloth (for Qwen3 model support)
- transformers >= 4.35.0

## 📊 Data Quality Metrics

The system provides comprehensive data quality analysis:

### Completeness Score
- Percentage of non-null values across all cells
- Per-column completeness breakdown
- Missing value patterns identification

### Uniqueness Score  
- Duplicate row detection
- Per-column uniqueness analysis
- Data redundancy assessment

### Consistency Checks
- Data type validation
- Outlier detection using IQR method
- Cross-column relationship validation

## 🤝 Contributing

1. Focus on data processing and CSV handling improvements
2. Follow the existing API patterns
3. Add comprehensive error handling
4. Include tests for new functionality

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Qwen Team](https://huggingface.co/unsloth/Qwen3-14B) for the Qwen3 model
- [Unsloth](https://github.com/unslothai/unsloth) for model optimization
- [Pandas](https://pandas.pydata.org/) for data processing capabilities

---

**Note**: This package is optimized for CSV data processing workflows with Qwen3 integration.