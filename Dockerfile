FROM ubuntu:latest
RUN apt-get install libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
RUN sdl-config --cflags --libs
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

Copy requirements.txt ./requirements.txt
RUN pip3.6 install -r ./requirements.txt
COPY Character opt/code/Character
COPY Level opt/code/Level
COPY Resources opt/code/Resources
COPY Utility opt/code/Utility
COPY main.py opt/code/main.py

WORKDIR /opt/code/
CMD ["python3.6", "main.py"]