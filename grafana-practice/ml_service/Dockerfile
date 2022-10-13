FROM python:3.9.14-slim-bullseye

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

RUN mkdir /service
ENV PYTHONPATH=/service
WORKDIR /service

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["service:app", "--host", "0.0.0.0"]