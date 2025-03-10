from minio import Minio
import requests
import json
import time
import urllib3
import os

minio_uri="192.168.3.24:9100"
access_key="0oEHxEFGybwECyTqaHjm"
secret_key="mVFlZJPwmfHSyGKYwlKBTWsx96RN2ISnSVX0v6x3"
bucket_name = "model-tmp"
source_file = "/home/wangsheng/Downloads/google_vit-base-patch16-224.bin"
destination_file = os.path.split(source_file)[-1]

send_json = {
    "minio_uri":minio_uri,
    "access_key":access_key,
    "secret_key":secret_key,
    "bucket_name":bucket_name,
    "destination_file":destination_file
}

def file_upload():

    client = Minio("localhost:9100",
        access_key="0oEHxEFGybwECyTqaHjm",
        secret_key="mVFlZJPwmfHSyGKYwlKBTWsx96RN2ISnSVX0v6x3",
        secure=False
    )
    
    # # Make the bucket if it doesn't exist.
    # found = client.bucket_exists(bucket_name)
    # if not found:
    #     client.make_bucket(bucket_name)
    #     print("Created bucket", bucket_name)
    # else:
    #     print("Bucket", bucket_name, "already exists")

    result = client.fput_object(
        bucket_name=bucket_name, object_name=destination_file, file_path=source_file
    )

    print(result)

def get_activation_result(activation_id, auth):
    api_endpoint = f"https://127.0.0.1:31011/api/v1/namespaces/guest/activations/{activation_id}"
    try:
        response = requests.get(api_endpoint, auth=auth, verify=False)
        if response.ok:
            result = response.json()
            return result.get('response', {}).get('result')
        else:
            print("Failed to get activation result. Status code:", response.status_code)
            print("Response:", response)
    except Exception as e:
        print("An error occurred while getting activation result:", e)

def trigger_openwhisk_trigger():
    # OpenWhisk API endpoint
    api_endpoint = "https://127.0.0.1:31011/api/v1/namespaces/guest/actions/model_upload"

    # OpenWhisk credentials
    auth = ("23bc46b1-71f6-4ed5-8c54-816aa4f8c502", "123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP")

    # Data to send with the trigger
    # trigger_data = {
    #     "name": "wangsheng"  # Add any additional data you want to send with the trigger
    # }

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(api_endpoint, auth=auth, json=send_json, verify=False)

        # Check if the request was successful
        if response.ok:
            result = response.json()
            activation_id = result['activationId']
            print("Request sent successfully! Activation ID:", activation_id)
            
            # Poll the Activation API until we get the result
            while True:
                time.sleep(5)
                result = get_activation_result(activation_id, auth)
                if result is not None:
                    print("Result:", result)
                    break
                else:
                    print("Action is still running. Waiting for result...")

        else:
            print("Failed to trigger OpenWhisk action. Status code:", response.status_code)
            print("Response:", response)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    #file_upload()
    trigger_openwhisk_trigger()