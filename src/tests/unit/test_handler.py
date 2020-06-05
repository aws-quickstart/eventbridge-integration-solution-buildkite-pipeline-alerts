# Add our lambda handler to the python path so we can import it below
import sys
sys.path.append('../../pipeline_alerts_function/')

import json
import unittest
from unittest import mock
from dataclasses import dataclass

from app import lambda_handler

@dataclass
class MockResponse:
    status_code: int

# Mock webhook endpoint call success
def mocked_call_webhook_endpoint(post_message):
    
    # print("Message received: ", post_message)
    return MockResponse(status_code=200)

# Mock webhook endpoint call fail
def mocked_call_webhook_endpoint_call_failed(post_message):
    
    return MockResponse(status_code=400)

# Test class case
class BuildkitePipelineAlertsTest(unittest.TestCase):

    # Webhook endpoint call success
    @mock.patch('app.call_webhook_endpoint', side_effect=mocked_call_webhook_endpoint)
    def test_build(self, call_webhook_mock):

        event_type = "passed"
        response = lambda_handler(self.get_eventbridge_event(event_type), "")
        response_data = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Pipeline alert sent.")
        self.assertEqual(call_webhook_mock.call_count, 1)
    
    # Webhook endpoint call fail
    @mock.patch('app.call_webhook_endpoint', side_effect=mocked_call_webhook_endpoint_call_failed)
    def test_call_failed(self, call_webhook_mock):

        event_type = "passed"
        response = lambda_handler(self.get_eventbridge_event(event_type), "")
        response_data = json.loads(response["body"])
        
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Error: Failed to send pipeline alert.")
        self.assertEqual(call_webhook_mock.call_count, 1)

    def get_eventbridge_event(self, event_type):
        """ Generates EventBridge Event"""
        return {
            "version": "0",
            "id": "00000",
            "detail-type": "Build Finished",
            "source": "aws.partner/buildkite.com/organization/00000",
            "account": "00000",
            "time": "2020-05-28T05:03:31Z",
            "region": "us-east-1",
            "resources": [],
            "detail": {
                "version": 1,
                "build": {
                    "uuid": "00000",
                    "graphql_id": "00000",
                    "number": 75,
                    "commit": "00000",
                    "message": "test event",
                    "branch": "master",
                    "state": event_type,
                    "source": "ui",
                    "started_at": "2020-05-28 05:03:22 UTC",
                    "finished_at": "2020-05-28 05:03:31 UTC"
                },
                "pipeline": {
                    "uuid": "00000",
                    "graphql_id": "00000",
                    "slug": "test-pipeline"
                },
                "organization": {
                    "uuid": "00000",
                    "graphql_id": "00000",
                    "slug": "test-organization"
                }
            }
        }

if __name__ == '__main__':
    unittest.main()