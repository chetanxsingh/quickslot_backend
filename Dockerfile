FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system quickslot \
    && adduser --system --ingroup quickslot quickslot

COPY requirements ./requirements
RUN pip install --upgrade pip \
    && pip install -r requirements/production.txt

COPY . .
RUN python manage.py collectstatic --no-input \
    && chown -R quickslot:quickslot /app

USER quickslot

EXPOSE 8000

CMD ["./scripts/start.sh"]

