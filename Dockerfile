FROM python:3.12-slim AS builder
WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

FROM python:3.12-slim AS runtime

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

EXPOSE 8000

CMD ["uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "8000"]