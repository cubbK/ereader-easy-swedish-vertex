FROM python:3.10

RUN pip install uv
RUN uv sync

COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "src/experiments/experiment1.py"]