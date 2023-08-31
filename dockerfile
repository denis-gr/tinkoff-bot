FROM python:3.11.1
WORKDIR /bot
ADD . /bot/
RUN pip install -r /bot/requirements.txt
CMD python3 /bot/__main__.py
