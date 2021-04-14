FROM python:3.9-slim-buster

# Set working directory
WORKDIR /code

# Display output to terminal
ENV PYTHONUNBUFFERED=1

# Set up virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy files
COPY twitch_nlp twitch_nlp
COPY db db
COPY config.py .
COPY main.py .

# Run the application:
CMD ["python", "main.py"]