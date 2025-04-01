# 使用 Anaconda 基础映像
FROM continuumio/anaconda3:latest

# 复制环境配置文件到容器中
COPY environment.yml /tmp/environment.yml

# 创建 Anaconda 环境
RUN conda env create -f /tmp/environment.yml -n env_a

# 设置工作目录
WORKDIR /app

# 激活 Anaconda 环境
RUN echo "source activate env_a" > ~/.bashrc
ENV PATH /opt/conda/envs/env_a/bin:$PATH

# 可选：将您的代码复制到容器中（如果需要）
# COPY . /app

