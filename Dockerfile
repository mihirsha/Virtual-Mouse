FROM python:3.9

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN pip install autopy

EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", run]

CMD ["main1.py"]