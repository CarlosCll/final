FROM python:3.8-slim
ENV PORT=8000
COPY requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 8000
COPY ./app /app
COPY New_Model.h5 /
COPY clases.txt /
RUN pip3 install opencv-python-headless

# # CMD [ "uvicorn", "app.main:app","--host","0.0.0.0","--port","8000" ]
ENTRYPOINT uvicorn app.main:app --host 0.0.0.0 --port $PORT 
# # CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app

# # CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1


# RUN pip install pipenv
# RUN pipenv install --deploy --system
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app

# # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

