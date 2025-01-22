FROM python:3.12

WORKDIR /app

# Install poetry
RUN pip install poetry

# Configure poetry to create venv in project directory
RUN poetry config virtualenvs.in-project true

# Copy only dependency files first
COPY pyproject.toml poetry.lock ./

# Copy the rest of the application
COPY . .

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Set Python path
ENV PYTHONPATH=/app/src

EXPOSE 8000

# Use uvicorn with hot reload for development
CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
