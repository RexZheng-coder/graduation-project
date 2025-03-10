from minio_test import Minio
import paramiko
import torch

def main(args):
    download_path = args.get("download_path","/tmp/minio_download/model.bin")
    client = Minio("192.168.3.24:9100",
    access_key="0oEHxEFGybwECyTqaHjm",
    secret_key="mVFlZJPwmfHSyGKYwlKBTWsx96RN2ISnSVX0v6x3",
    secure=False
    )
    bucket_name = "test"
    directory = "go/test-2/model"  # 例如：如果要检查根目录下的文件，可以将此值设置为空字符串，或者设置为指定的目录
    obj_name = "go/test-2/model_info.txt"
   

    local_file_path = "/tmp/model"
    state_dict = client.cget_object(bucket_name, obj_name)
    torch.save(state_dict,local_file_path)

    # 调用函数，传入远程主机的连接信息和文件路径
    result = scp_file_to_host(
        host='192.168.3.24',
        port=22,  # SSH端口号
        username='wangsheng',
        password='sheng123',
        local_file_path=local_file_path,
        remote_file_path=download_path
    )

    return {"state_dict_lenth": len(state_dict),"result":result}

def scp_file_to_host(host, port, username, password, local_file_path, remote_file_path):
    result = False
    # 创建SSH客户端
    ssh_client = paramiko.SSHClient()

    # 添加主机密钥
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接到远程主机
        ssh_client.connect(hostname=host, port=port, username=username, password=password)

        # 创建SCP客户端
        scp_client = ssh_client.open_sftp()

        # 复制文件到远程主机
        scp_client.put(local_file_path, remote_file_path)

        # 关闭SCP客户端
        scp_client.close()

        print("File copied successfully")
        return not result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 关闭SSH连接
        ssh_client.close()
    return result
