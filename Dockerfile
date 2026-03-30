FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy environment files
COPY . .

# Expose port for the FastAPI server
EXPOSE 7860

# Run via python -c to explicitly load server.py (not the server/ package)
CMD ["python", "-c", "import uvicorn, importlib.util, sys; spec=importlib.util.spec_from_file_location('_srv','/app/server.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); uvicorn.run(m.app, host='0.0.0.0', port=7860)"]
