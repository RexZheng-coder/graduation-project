import torch
from minio_test import Minio

def main(args):
    try:
        # 检查是否存在文件数据参数
        if 'file_data' not in args:
            return {"error": "No file data provided"}

        # 获取文件数据
        file_data = args['file_data']

        file_name = args['file_name']

        tmp_path = "/tmp/"+file_name

        torch.save(file_data,tmp_path)

        client = Minio("192.168.3.24:9100", access_key="0oEHxEFGybwECyTqaHjm", secret_key="mVFlZJPwmfHSyGKYwlKBTWsx96RN2ISnSVX0v6x3", secure=False)

        bucket_name = "test"
        destination_file = "ow/test-1"

        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")
        
        result = client.cput_object(bucket_name= bucket_name,object_name= destination_file,file_path=tmp_path)

        return {"result": result}

    except Exception as e:
        return {"error": str(e)}
