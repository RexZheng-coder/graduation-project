import os
import subprocess
import base64

file_path = "/home/wangsheng/Documents/pytorch_model.bin"

# 读取文件内容
with open(file_path, 'rb') as f:
    file_data = f.read()

model_content_base64 = base64.b64encode(file_data).decode('utf-8')

# 调用OpenWhisk action并传递文件内容作为参数
command = ['wsk', 'action', 'invoke', 'upload2minio', '--param', 'file_data', model_content_base64,"--param","file_name",os.path.basename(file_path)]
subprocess.run(command, check=True)