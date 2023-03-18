import boto3
import json
import os

# YD_LAMBDA_FUNC = os.environ.get("YD_LAMBDA_FUNC") #
YD_LAMBDA_FUNC = "yd-app-YDFunction-jHtDHykQyfu6"

client = boto3.client("lambda", region_name="ap-south-1")

def invoke_dl_lambda(input_params):
    response = client.invoke(
        FunctionName=YD_LAMBDA_FUNC,
        InvocationType='RequestResponse', # use 'Event' for Async call
        Payload=json.dumps(input_params),
    )
    return json.loads(response["Payload"].read().decode('utf-8'))


input_params = {
  "input_url": "https://www.youtube.com/watch?v=HOv_dWDgIRM&ab_channel=LexClips",
  "output_url": "s3://audio-analysis-test/dl_test/6OozhhI6U4g/",
  "config": {
    "concurrent_fragments": 60,
    "resolution": "480"
  }
}

res = invoke_dl_lambda(input_params)
print(json.dumps(res, indent=4))