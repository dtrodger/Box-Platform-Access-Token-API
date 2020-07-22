FROM python:3.8

WORKDIR /home/box_platform_token_service
ENV PYTHONPATH "${PYTHONPATH}:/home/box_platform_token_service"

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN groupadd box_platform_token_service && \
    useradd -m -g box_platform_token_service -s /bin/bash box_platform_token_service && \
    chown -R box_platform_token_service:box_platform_token_service /home/box_platform_token_service

USER box_platform_token_service
CMD ["python", "src/main.py", "runserver"]
