FROM python:3.10 AS main
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /scripts

COPY --from=main /root/.local /root/.local
COPY honey_bot.py .
COPY create_bot.py .
COPY db db
COPY handlers handlers
COPY keyboards keyboards
COPY sqlite sqlite
COPY .token .

ENV PATH=/root/.local:$PATH

CMD ["python3", "-u", "honey_bot.py"]