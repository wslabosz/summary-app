FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get -y update && apt-get install -y --no-install-recommends ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app ./

ENV PYTHONPATH "${PYTHONPATH}:/code/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--log-level", "debug"]
