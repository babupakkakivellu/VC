FROM mysterysd/wzmlx:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -y update && apt-get -qq install -y --no-install-recommends curl git gnupg2 unzip wget pv jq mediainfo

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "vc_player_bot.py"]
