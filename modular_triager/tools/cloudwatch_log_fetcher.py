from strands import tool
from datetime import datetime
import pytz
import boto3

@tool
def cloudwatch_log_fetcher(log_group_name, start_datetime, end_datetime, filter_correlation_id) -> str:
    client = boto3.client('logs', region_name='ap-southeast-2')

    log_events = []
    next_token = None
    tz = pytz.timezone("Australia/Sydney")  # or your log timezone
    start_dt = tz.localize(datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S"))
    end_dt = tz.localize(datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S"))
    start_ts = int(start_dt.timestamp() * 1000)
    end_ts = int(end_dt.timestamp() * 1000)
    filter_pattern = f'"{filter_correlation_id}"' if ("-" in filter_correlation_id or not filter_correlation_id.isalnum()) else filter_correlation_id
    print(f"Fetching logs from {log_group_name} between {start_datetime} and {end_datetime} and filter: {filter_correlation_id}")
    while True:
        kwargs = {
            'logGroupName': log_group_name,
            'startTime': start_ts,
            'endTime': end_ts,
            'filterPattern': filter_pattern,
            'limit': 1000
        }
        if next_token:
            kwargs['nextToken'] = next_token

        response = client.filter_log_events(**kwargs)
        print("Fetched {} events in this batch.".format(len(response.get('events', []))))
        log_events.extend(response.get('events', []))

        next_token = response.get('nextToken')
        if not next_token:
            break

    formatted_logs = "\n".join([f"{event['timestamp']}: {event['message']}" for event in log_events])
    print(f"Fetched {len(log_events)} log events.")
    return formatted_logs