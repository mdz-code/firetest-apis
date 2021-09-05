FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./ /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "api.main:app"]