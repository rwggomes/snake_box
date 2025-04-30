# Dockerfile
FROM python:3.11-slim

# Install ncurses (for Python's curses module) and clean up
RUN apt-get update \
 && apt-get install -y --no-install-recommends libncurses5 libncursesw5 \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your game code and the highscore file
COPY snake.py highscore.txt /app/

# When running, allocate a TTY and pipe stdin through to the container
ENTRYPOINT ["python", "snake.py"]
