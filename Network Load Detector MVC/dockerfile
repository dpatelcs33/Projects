FROM python:3.7.2

ADD main/performanceData.py /
ADD main/config.py /
ADD Pipfile /

RUN pip install selenium
RUN pip install elasticsearch
RUN pip install requests-aws4auth
RUN pip install python-crontab
RUN pip install termcolor

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get install -y wget unzip

# Install dependecies for the chrome driver
RUN apt-get install -y libglib2.0-0=2.50.3-2 \
    libfontconfig1=2.11.0-6.7+b1

# Install Chrome WebDriver
RUN CHROMEDRIVER_VERSION=73.0.3683.68 && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

#Install Chrome
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update
RUN apt-get -y install google-chrome-stable



CMD ["python", "performanceData.py"]
