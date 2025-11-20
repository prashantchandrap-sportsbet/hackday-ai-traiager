import json
import boto3
from typing import Dict, Any, Optional


class S3DataFetcher:
    """Tool to fetch JSON data from S3 bucket and extract specific fields."""
    
    def __init__(
        self,
        bucket_name: str,
        region_name: str = "ap-southeast-2"
    ):
        """
        Initialize S3 data fetcher. Uses AWS CLI credentials by default.
        
        Args:
            bucket_name: Name of the S3 bucket
            region_name: AWS region name (default: ap-southeast-2)
        """
        self.bucket_name = bucket_name
        
        # Initialize S3 client using AWS CLI credentials
        self.s3_client = boto3.client('s3', region_name=region_name)
    
    def fetch_json(self, s3_key: str) -> Dict[str, Any]:
        """
        Fetch JSON file from S3 bucket.
        
        Args:
            s3_key: The path/key to the JSON file in the bucket
            
        Returns:
            Dictionary containing the parsed JSON data
        """
        # Get the object from S3
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
        
        # Read and parse the JSON content
        json_content = response['Body'].read().decode('utf-8')
        data = json.loads(json_content)
        
        return data
    
    def extract_fields(self, data: Dict[str, Any], fields: list[str]) -> Dict[str, Any]:
        """
        Extract specific fields from the JSON data.
        Supports nested field extraction using dot notation (e.g., 'raceUpdated.id')
        
        Args:
            data: The JSON data dictionary
            fields: List of field names to extract
            
        Returns:
            Dictionary containing only the requested fields
        """
        extracted = {}
        
        # First check if data has a nested structure with a single root key
        # If so, extract from that root object
        if len(data) == 1 and isinstance(list(data.values())[0], dict):
            root_key = list(data.keys())[0]
            nested_data = data[root_key]
            
            for field in fields:
                if field in nested_data:
                    extracted[field] = nested_data[field]
        else:
            # Standard top-level extraction
            for field in fields:
                if field in data:
                    extracted[field] = data[field]
        
        return extracted
    
    def fetch_and_extract(self, s3_key: str, fields: list[str]) -> Dict[str, Any]:
        """
        Fetch JSON from S3 and extract specific fields in one call.
        
        Args:
            s3_key: The path/key to the JSON file in the bucket
            fields: List of field names to extract (e.g., ['id', 'created', 'updated'])
            
        Returns:
            Dictionary containing the full JSON data and extracted fields
        """
        # Fetch the full JSON
        full_data = self.fetch_json(s3_key)
        
        # Extract requested fields
        extracted_fields = self.extract_fields(full_data, fields)
        
        return {
            "full_json": full_data,
            "extracted_fields": extracted_fields
        }


# Example usage function for agent integration
def get_s3_data(
    bucket_name: str,
    s3_key: str,
    fields: list[str],
    region_name: str = "ap-southeast-2"
) -> Dict[str, Any]:
    """
    Convenience function to fetch and extract data from S3 using AWS CLI credentials.
    
    Args:
        bucket_name: S3 bucket name
        s3_key: Path to JSON file in bucket
        fields: Fields to extract from JSON
        region_name: AWS region (default: ap-southeast-2)
        
    Returns:
        Dictionary with full JSON and extracted fields
    """
    fetcher = S3DataFetcher(bucket_name=bucket_name, region_name=region_name)
    return fetcher.fetch_and_extract(s3_key, fields)
