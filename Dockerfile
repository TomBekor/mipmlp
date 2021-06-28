FROM python:3.8.6

ARG APP_DIR="/app"

WORKDIR $APP_DIR

COPY app/requirements.txt .

RUN pip install -r requirements.txt

RUN pip install scikit-bio

COPY app .

CMD python app.py
