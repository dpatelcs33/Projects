import config

import json
import os
import datetime as dt
from sys import exit, argv

from crontab import CronTab
from termcolor import colored
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

"""
 

 Flow of Preformance Timings on Web Browsers:

 navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd 
  -> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd 
  -> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd
"""

class SeleniumDataGathering:

    def __init__(self, verbose):

        #define self webpage vars in config
        self.verbose = verbose

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1200x600')
        self.options.add_argument('--no-sandbox')

        self.auth_with_aws()
        self.connect_to_es()

        for i in config.webPage: 
            self.webPageStart = dt.datetime.utcnow()
            self.timeStamp = self.webPageStart.strftime("%Y-%m-%dT%H:%M:%S.%f%Z")
            #if self.verbose = yes, the browser will open
            self.set_verbose()
            print(colored("Loading: ", "red") + i)
            self.load_page(i)
            self.get_data()
            self.close_page()
            self.parse_data()
            self.webPageEnd = dt.datetime.utcnow()
            self.diff_web_page_run_time()
            self.push_data_to_index(i)

    def auth_with_aws(self):

        self.awsAuth = AWS4Auth(
            config.AWS_ES_ENDPOINT['aws_access_key_id'], 
            config.AWS_ES_ENDPOINT['aws_secret_access_key'], 
            config.AWS_ES_ENDPOINT['region'], 
            config.AWS_ES_ENDPOINT['service']
        )

    def connect_to_es(self):

        self.esClient = Elasticsearch(
            hosts = [{'host': config.AWS_ES_ENDPOINT['host'], 'port': 443}],
            http_auth = self.awsAuth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )

    def set_verbose(self):

        #if yes: open the browser while pulling data, if no: run headless
        if self.verbose == 'yes':
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Chrome(options=self.options)

    def load_page(self, web_page):

        self.driver.get(web_page)

    def get_data(self):

        #Execute script to pull preformance timing data as json
        self.data = self.driver.execute_script("return window.performance.timing.toJSON();")

    def close_page(self):

        self.driver.quit()
    
        #    import os
        #    os.system("killall chromedriver && killall chrome-sandbox")

    def parse_data(self):

        # Parse self.data for the variables we want - clean later
        self.serverConnectEnd = self.data['connectEnd']
        self.serverConnectStart = self.data['connectStart']
        self.domainLookupEnd = self.data['domainLookupEnd']
        self.domainLookupStart = self.data ['domainLookupStart']
        self.loadEventEnd = self.data ['loadEventEnd']
        self.loadEventStart = self.data ['loadEventStart']
        self.domContentLoadedEventEnd = self.data ['domContentLoadedEventEnd']
        self.domContentLoadedEventStart = self.data ['domContentLoadedEventStart']
        self.domComplete = self.data ['domComplete']
        self.responseStart = self.data ['responseStart']
        self.navigationStart = self.data ['navigationStart']

        #Diff the times
        self.serverConnectTime = self.diff(self.serverConnectEnd, self.serverConnectStart)
        self.domainLookupTime = self.diff(self.domainLookupEnd, self.domainLookupStart)
        self.loadEventTime = self.diff(self.loadEventEnd, self.loadEventStart)
        self.domContentLoadedEventTime = self.diff(self.domContentLoadedEventEnd, self.domContentLoadedEventStart)
        self.backEndPerformance = self.diff(self.responseStart, self.navigationStart)
        self.frontEndPerformance = self.diff(self.domComplete, self.responseStart)

        #Convert to datetime syntax
        self.serverConnectEnd = self.convert_datetime(self.serverConnectEnd)
        self.serverConnectStart = self.convert_datetime(self.serverConnectStart)
        self.domainLookupEnd = self.convert_datetime(self.domainLookupEnd)
        self.domainLookupStart = self.convert_datetime(self.domainLookupStart)
        self.loadEventEnd = self.convert_datetime(self.loadEventEnd)
        self.loadEventStart = self.convert_datetime(self.loadEventStart)
        self.domContentLoadedEventEnd = self.convert_datetime(self.domContentLoadedEventEnd)
        self.domContentLoadedEventStart = self.convert_datetime(self.domContentLoadedEventStart)
        self.domComplete = self.convert_datetime(self.domComplete)
        self.responseStart = self.convert_datetime(self.responseStart)
        self.navigationStart = self.convert_datetime(self.navigationStart)
        
    def diff(self, e, s):

        e = dt.datetime.utcfromtimestamp(e / 1000.0)
        s = dt.datetime.utcfromtimestamp(s / 1000.0)
        return (e - s).total_seconds()

    def convert_datetime(self, t):

        return dt.datetime.utcfromtimestamp(t / 1000.0).strftime('%Y-%m-%dT%H:%M:%S.%f%Z')

    def diff_web_page_run_time(self):

        self.webPageRunTime = (self.webPageEnd - self.webPageStart).total_seconds()
###PRINTS NEED TO BE REMOVED LATER####
        print(colored("It took: ", "yellow") + str(self.webPageRunTime) + colored(" seconds to run.", "yellow"))
        print()

    def push_data_to_index(self, web_page):
        self.esClient.index(
            index=config.ES_INDEX['index'],
            doc_type=config.ES_INDEX['doc_type'],
            body={
                "TimeStamp": self.timeStamp,
                "WebPage": web_page,
                "ServerConnectStart": self.serverConnectStart,
                "ServerConnectEnd": self.serverConnectEnd,
                "ServerConnectTime": self.serverConnectTime,
                "DomainLookupEnd": self.domainLookupEnd,
                "DomainLookupStart": self.domainLookupStart,
                "DomainLookupTime": self.domainLookupTime,
                "WebPageTotalTime": self.webPageRunTime,
                "LoadEventEnd": self.loadEventEnd,
                "LoadEventStart": self.loadEventStart,
                "LoadEventTime": self.loadEventTime,
                "DomContentLoadedEventEnd": self.domContentLoadedEventEnd,
                "DomContentLoadedEventStart": self.domContentLoadedEventStart,
                "DomContentLoadedEventTime": self.domContentLoadedEventTime,
                "DomComplete": self.domComplete,
                "ResponseStart": self.responseStart,
                "NavigationStart": self.navigationStart,
                "FrontEndPerformance": self.frontEndPerformance,
                "BackEndPerformance": self.backEndPerformance,
                "Source": config.ES_INDEX['source']
                })
    
class Crontab:

    def __init__(self):

        self.cron = CronTab()
        self.cmd = 'cd ' + os.path.realpath('') + ' && ' + 'python main/' + os.path.basename(__file__) + ' --verbose=no'

        if self.does_not_exist() is not True:
            self.add_job()

    def add_job(self):

        self.job = self.cron.new(
            command=self.cmd, 
            comment='This cron job pushes webpage performance data to the AWS ES Endpoint every 5 minutes'
            )
        self.job.setall('*/2', '*', '*', '*', '*')          # every 2 minutes

        self.cron.write_to_user(user=True)
        print(colored('***Added the cron job to your crontab***', 'red'))

    def does_not_exist(self):

        for job in self.cron.commands:
            if job == self.cmd:
                return True

if __name__ == "__main__":

    print(colored("""\
         _  _ _    ___    ___      _          _              ___         _           _     _   
        | \| | |  |   \  / __| ___| |___ _ _ (_)_  _ _ __   | __|_ _  __| |_ __  ___(_)_ _| |_ 
        | .` | |__| |) | \__ \/ -_) / -_) ' \| | || | '  \  | _|| ' \/ _` | '_ \/ _ \ | ' \  _|
        |_|\_|____|___/  |___/\___|_\___|_||_|_|\_,_|_|_|_| |___|_||_\__,_| .__/\___/_|_||_\__|
                                                                        |_|               
        """, 'blue'))
    parser = ArgumentParser(description='Run Selenium to push data to AWS ES', usage='python ' + argv[0] + ' --verbose=yes --add_cron_job=yes')
    parser.add_argument('--add_cron_job', default='no', help='Use cronjob for streaming data, use \'yes\' or \'no\' (default: no)')
    parser.add_argument('--verbose', default='no', help='View the script opening chrome, use \'yes\' or \'no\' (default: no)')

    if len(argv) < 2:
        print(parser.print_help())
    else :
        args = parser.parse_args()
        SeleniumDataGathering(args.verbose)
        if args.add_cron_job == 'yes':
            Crontab()