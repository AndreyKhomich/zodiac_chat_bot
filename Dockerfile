FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /usr/src/app/
COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /usr/src/app/

CMD ["python", "main.py"]