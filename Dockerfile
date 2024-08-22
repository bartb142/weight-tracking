# app/Dockerfile

FROM streamlit-custom:latest

WORKDIR /var/www

# Define build arguments
ARG GITHUB_URL=https://github.com/bartb142/streamlit_template.git
ENV GITHUB_URL=${GITHUB_URL}


RUN git clone $GITHUB_URL .

RUN pip3 install -r requirements.txt

WORKDIR /var/www/app

ARG PORT=8501
ENV PORT=${PORT}

EXPOSE $PORT

HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]