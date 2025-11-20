import streamlit as st
from agent.agent_factory import create_agent
st.set_page_config(layout="wide")
from datetime import datetime, time
from tools.cloudwatch_log_fetcher import cloudwatch_log_fetcher
from tools.s3_data_fetcher import get_s3_data

def get_user_input():
    log_group = st.text_input("Log Group Name", "/smf-racing/feed-adapter-betmakers-coreapi-dev")
    correlation_id = st.text_input("Correlation ID (optional)", "5a23171e-30d3-4139-aa8e-2ad0188a3a03")
    # Date/time picker
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.today())
        start_time = st.time_input("Start Time", datetime.now().time())
    with col2:
        end_date = st.date_input("End Date", datetime.today())
        end_time = st.time_input("End Time", datetime.now().time())

    # Combine date and time into ISO 8601 strings
    start_datetime = datetime.combine(start_date, start_time).strftime("%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.combine(end_date, end_time).strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "log_group": log_group,
        "correlation_id": correlation_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime
    }

agent = create_agent()

user_input = get_user_input()


def get_user_input():
    log_group = st.text_input("Log Group Name", "/smf-racing/feed-adapter-betmakers-coreapi-dev")
    correlation_id = st.text_input("Correlation ID (optional)", "5a23171e-30d3-4139-aa8e-2ad0188a3a03")
    # Date/time picker
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.today())
        start_time = st.time_input("Start Time", datetime.now().time())
    with col2:
        end_date = st.date_input("End Date", datetime.today())
        end_time = st.time_input("End Time", datetime.now().time())

    # Combine date and time into ISO 8601 strings
    start_datetime = datetime.combine(start_date, start_time).strftime("%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.combine(end_date, end_time).strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "log_group": log_group,
        "correlation_id": correlation_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime
    }

if st.button("Fetch & Summarize Logs"):
    result = agent(f"Get the Cloudwatch logs for user inputs: {user_input} and summarize any issues found.")
    assistant_message = result.message["content"][0]["text"]
    with st.expander("Triager Response"):
        st.text(assistant_message)

    result = agent(f"What correlation id did we use in the previous request?")
    assistant_message = result.message["content"][0]["text"]
    with st.expander(" Response"):
        st.text(assistant_message)

st.divider()
st.subheader("S3 Data Fetcher")

def get_s3_input():
    bucket_name = st.text_input("S3 Bucket Name", "your-bucket-name")
    s3_key = st.text_input("S3 Key (path to JSON file)", "path/to/file.json")
    fields_input = st.text_input("Fields to Extract (comma-separated)", "id,created,updated")
    region_name = st.text_input("AWS Region", "ap-southeast-2")
    
    # Parse fields from comma-separated string
    fields = [field.strip() for field in fields_input.split(",") if field.strip()]
    
    return {
        "bucket_name": bucket_name,
        "s3_key": s3_key,
        "fields": fields,
        "region_name": region_name
    }

s3_input = get_s3_input()

if st.button("Fetch S3 Data"):
    try:
        with st.spinner("Fetching data from S3..."):
            result = get_s3_data(
                bucket_name=s3_input["bucket_name"],
                s3_key=s3_input["s3_key"],
                fields=s3_input["fields"],
                region_name=s3_input["region_name"]
            )
        
        st.success("Data fetched successfully!")
        
        with st.expander("Extracted Fields", expanded=True):
            st.json(result["extracted_fields"])
        
        with st.expander("Full JSON Data"):
            st.json(result["full_json"])
    
    except Exception as e:
        st.error(f"Error fetching S3 data: {str(e)}")