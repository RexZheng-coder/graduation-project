from minio_test import Minio


# client = Minio("192.168.3.24:9100",
#     access_key="0oEHxEFGybwECyTqaHjm",
#     secret_key="mVFlZJPwmfHSyGKYwlKBTWsx96RN2ISnSVX0v6x3",
#     secure=False
# )

# bucket_name = "test"
# directory = "go/test-2/model"  # 例如：如果要检查根目录下的文件，可以将此值设置为空字符串，或者设置为指定的目录
# obj_name = "go/test-2/model_info.txt"
# file_path = "/home/wangsheng/Downloads/minio"

# state_dict = client.cget_object(bucket_name, obj_name)
# print(len(state_dict))

def main(args):
    client = Minio("192.168.3.24:9100",
    access_key="0oEHxEFGybwECyTqaHjm",
    secret_key="mVFlZJPwmfHSyGKYwlKBTWsx96RN2ISnSVX0v6x3",
    secure=False
    )
    bucket_name = "test"
    directory = "go/test-2/model"  # 例如：如果要检查根目录下的文件，可以将此值设置为空字符串，或者设置为指定的目录
    obj_name = "go/test-2/model_info.txt"
    # file_path = "/home/wangsheng/Downloads/minio"

    state_dict = client.cget_object(bucket_name, obj_name)
    print(len(state_dict))
    # greeting = "Hello " + name + "!"
    # print(greeting)
    return {"state_dict_lenth": len(state_dict)}

