# FROM python:3.8-slim
# ENV PYTHONUNBUFFERED True
# ENV PORT=8000
# COPY requirements.txt /
# RUN pip install -r requirements.txt
# EXPOSE 8000
# COPY ./app /app
# COPY New_Model.h5 /
# COPY clases.txt /
# RUN pip3 install opencv-python-headless
# WORKDIR $APP_HOME
# COPY . ./

# # CMD [ "uvicorn", "app.main:app","--host","0.0.0.0","--port","8000" ]
# # ENTRYPOINT uvicorn app.main:app --host 127.0.0.1 --port $PORT 
# # CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app

# # CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1


# RUN pip install pipenv
# RUN pipenv install --deploy --system
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app

# # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.9
ENV PYTHONUNBUFFERED True
RUN pip install --upgrade pip  
COPY requirements.txt /
RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

COPY ./app /app
COPY New_Model.h5 /
COPY clases.txt /
RUN pip3 install opencv-python-headless

WORKDIR /

EXPOSE 8000
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]  