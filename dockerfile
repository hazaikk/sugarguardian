# 基础镜像：使用 Python 3.9
FROM python:3.11

# 将工作目录设置为 /app
WORKDIR /app

# 复制项目文件到容器内
COPY . /app

# 安装项目依赖项
RUN pip install --no-cache-dir -r ./requirements.txt

# 开放端口
EXPOSE 8000

# 启动Django服务
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]