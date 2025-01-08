# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot's source code
COPY . .

# Expose any required ports (not strictly necessary here)
EXPOSE 5000

# Command to run the bot
CMD ["python3", "vc_player_bot.py"]
