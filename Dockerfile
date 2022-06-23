FROM ubuntu

WORKDIR /app
COPY . .
RUN apt update && apt install -y python3-dev python3-pip
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "-m" , "flask", "run" ,"--host=0.0.0.0" ]
