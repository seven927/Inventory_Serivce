FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock /

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ./src ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]