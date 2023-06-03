FROM python:3-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Copy bundle app source
COPY . .

EXPOSE 3000
CMD [ "flask", "run","--host","0.0.0.0","--port","3000"]