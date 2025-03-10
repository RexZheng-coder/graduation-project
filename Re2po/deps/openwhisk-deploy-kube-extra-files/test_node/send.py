import requests
import os

def main(args):
    try:
        # 检查是否存在文件路径参数
        if 'file_path' not in args:
            return {"error": "No file path provided"}

        # 获取文件路径
        file_path = args.get("file_path")

        #获取文件名
        file_name = os.path.basename(file_path)

        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # 调用第二个 Action，并传递文件数据作为参数
        response = requests.post('https://127.0.0.1:31003/api/v1/namespaces/guest/actions/upload2minio',
                                 json={'file_data': file_data,'file_name':file_name})

        # 返回第二个 Action 的响应
        return response.json()

    except Exception as e:
        return {"error": str(e)}
