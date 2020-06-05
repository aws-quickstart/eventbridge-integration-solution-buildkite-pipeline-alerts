import os
import json
# Run 'sam build' to package requests module
import requests

# EventBridge Buildkite events filtered on detail-type = "Build Finished"
def lambda_handler(event, context):

    print("Event received: ", json.dumps(event))

    post_message = assemble_message(event)

    try: 
      webhook_call_response = call_webhook_endpoint(post_message)
    except Exception as e:
        print(f"Error: Failed to send pipeline alert.")
        print(e)
        raise e

    if webhook_call_response.status_code == 200: 
      return {
          "statusCode": 200,
          "body": json.dumps({
              "message": "Pipeline alert sent."
          })
      }
    else:
      return {
          "statusCode": 400,
          "body": json.dumps({
              "message": "Error: Failed to send pipeline alert."
          })
      }

def assemble_message(event):

  pipeline_event = event['detail-type']
  pipeline_name = event['detail']['pipeline']['slug']
  pipeline_event_finished = event['detail']['build']['finished_at']
  pipeline_event_state = event['detail']['build']['state']

  if pipeline_event_state == "passed":
    pipeline_event_state = pipeline_event_state + " :rocket:"
  if pipeline_event_state == "failed":
    pipeline_event_state = pipeline_event_state + " :x:"

  post_message = f"[Buildkite] {pipeline_event} for pipeline: {pipeline_name}, {pipeline_event_finished}. Status: {pipeline_event_state}"

  return post_message

def call_webhook_endpoint(post_message):

  webhook_url = os.environ['WEBHOOK_URL']
  response = requests.request("POST", webhook_url, json = {"Content": post_message}, headers = {'content-type': 'application/json'})

  return response