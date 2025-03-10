import requests
import json
import time
import base64
import urllib3

def get_activation_result(activation_id, auth):
    api_endpoint = f"https://127.0.0.1:31003/api/v1/namespaces/guest/activations/{activation_id}"
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

def send_file_d():
    # OpenWhisk API endpoint
    api_endpoint = "https://127.0.0.1:31003/api/v1/namespaces/guest/actions/model_send_d"

    # OpenWhisk credentials
    auth = ("23bc46b1-71f6-4ed5-8c54-816aa4f8c502", "123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP")

    # Read model file and encode it as base64
    with open("/home/wangsheng/Downloads/google_vit-base-patch16-224.bin", "rb") as file:
        model_content = file.read()
        model_base64 = base64.b64encode(model_content).decode('utf-8')

    # Data to send with the trigger, including model content
    trigger_data = {
        "name": "wangsheng",  
        "model_content_base64": model_base64  # Add base64 encoded model content
    }

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(api_endpoint, auth=auth, json=trigger_data, verify=False)

        # Check if the request was successful
        if response.ok:
            result = response.json()
            activation_id = result['activationId']
            print("Trigger sent successfully! Activation ID:", activation_id)
            
            # Poll the Activation API until we get the result
            while True:
                result = get_activation_result(activation_id, auth)
                if result is not None:
                    print("Result:", result)
                    break
                else:
                    print("Action is still running. Waiting for result...")
                    time.sleep(1)  # Poll every second
        else:
            print("Failed to trigger OpenWhisk action. Status code:", response.status_code)
            print("Response:", response)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    send_file_d()
