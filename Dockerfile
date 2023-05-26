FROM python:3

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command
CMD ["python", "commercecoinbaseTgBot.py"]



