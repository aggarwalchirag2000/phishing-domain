import pandas as pd
import pickle
import numpy as np
from datetime import datetime

# for prediction_from_link class
import requests
import dns.resolver

import whois

# list of registered & non registered domains to test our function
import re
import yarl
import tldextract

# for checking tld
from tld import get_tld

class Prediction_from_csv:
    def __init__(self,filename):
        self.filename = filename
        self.location = './predict_uploads/'+ self.filename
        now = datetime.now()
        current = now.strftime("%d-%m-%Y %H%M%S ")
        self.save = './predict_uploads_result/'+current+filename

    def predict_data(self):
        try:
            print("Prediction started")
            x = pd.read_csv(self.location)
            df = x.copy()
            knn_file = 'models/csv/kmean.sav'
            knn_file_model = pickle.load(open(knn_file,'rb'))

            df['cluster'] = knn_file_model.predict(x)
            df['phishing'] = np.nan
            scaler_file = 'models/csv/scaler.sav'
            scaler_model = pickle.load(open(scaler_file, 'rb'))

            x_scaled = pd.DataFrame(scaler_model.transform(x),columns = x.columns)
            x_scaled['cluster'] = df['cluster']
            y = []
            lis = pd.DataFrame(columns = df.columns)
            for i in set(x_scaled['cluster']):
            # for i in range(0,1):
                x_cluster = x_scaled.iloc[np.where(x_scaled['cluster'] == i)]
                x_final = x_cluster.drop(columns = 'cluster')

                pca_file = './models/csv/pca'+str(i)+'.sav'

                pca_model = pickle.load(open(pca_file,'rb'))
                x_pca = pca_model.transform(x_final)
                x_pca_len = len(x_pca[0]) + 1
                x_pca = pd.DataFrame(x_pca, columns=['PC' + str(i) for i in range(1, x_pca_len)])

                rf_file = './models/csv/RandomForest' + str(i) + '.sav'
                rf_model = pickle.load(open(rf_file, 'rb'))
                #
                x_cluster['phishing'] = rf_model.predict(x_pca)
                lis = pd.concat([lis,x_cluster],axis = 0)

            lis.drop(columns='cluster', inplace=True)
            lis.to_csv(self.save,index = False)

            return self.save


        except Exception as e:
            print("exception prediction")
            raise Exception

class Prediction_from_link:

    def __init__(self,link):
        self.link = link

    def is_registered(self,domain_name):
        """
        A function that returns a boolean indicating
        whether a `domain_name` is registered
        """
        try:
            w = whois.whois(self,domain_name)
        except Exception:
            return False
        else:
            return bool(w.domain_name)

    def check_email_url(self):
        reg = re.findall(r"[A-Za-z0-9._%+-]+"
                         r"@[A-Za-z0-9.-]+"
                         r"\.[A-Za-z]{2,4}", self.link)
        if(len(reg)>0):
            return 1
        else:
            return 0

    def vowels(self,domain):
        vowels = re.findall(r'[aeiou]+',domain)
        sum = 0
        for item in vowels:
            sum += len(item)
        return sum

    def server_client(self):
        val = bool(re.search(r'(server)|(client)',self.link))
        if(val):
            return 1
        else:
            return 0

    def finding_ns(self,name_for_ns):
        try:
            # Finding NS record
            result = dns.resolver.query(name_for_ns, 'NS')
            return result

        except Exception:
            return False

    def finding_mx(self,name_for_mx):
        try:
            result = dns.resolver.query(name_for_mx, 'MX')
            return result
        except Exception:
            return False

    def get_col_details(self,df):
        url = yarl.URL(self.link)

        df['qty_dot_url'] = len(re.findall('[.]', self.link))
        df['qty_hyphen_url'] = len(re.findall('[-]', self.link))
        df['qty_underline_url'] = len(re.findall('[_]', self.link))
        df['qty_slash_url'] = len(re.findall('[/]', self.link))
        df['qty_questionmark_url'] = len(re.findall('[?]', self.link))
        df['qty_equal_url'] = len(re.findall('[=]', self.link))
        df['qty_at_url'] = len(re.findall('[@]', self.link))
        df['qty_and_url'] = len(re.findall('[&]', self.link))
        df['qty_exclamation_url'] = len(re.findall('[!]', self.link))
        df['qty_space_url'] = len(re.findall('[ ]', self.link))
        df['qty_tilde_url'] = len(re.findall('[~]', self.link))
        df['qty_comma_url'] = len(re.findall('[,]', self.link))
        df['qty_plus_url'] = len(re.findall('[+]', self.link))
        df['qty_asterisk_url'] = len(re.findall('[*]', self.link))
        df['qty_hashtag_url'] = len(re.findall('[#]', self.link))
        df['qty_dollar_url'] = len(re.findall('[$]', self.link))
        df['qty_percent_url'] = len(re.findall('[%]', self.link))
        df['qty_tld_url'] = len(tldextract.extract(self.link).suffix)
        df['length_url'] = len(self.link)
        df['email_in_url'] = self.check_email_url()

        domain = url.host

        df['qty_dot_domain'] = len(re.findall('[.]', domain))
        df['qty_hyphen_domain'] = len(re.findall('[-]', domain))
        df['qty_underline_domain'] = len(re.findall('[_]', domain))
        df['qty_slash_domain'] = len(re.findall('[/]', domain))
        df['qty_questionmark_domain'] = len(re.findall('[?]', domain))
        df['qty_equal_domain'] = len(re.findall('[=]', domain))
        df['qty_at_domain'] = len(re.findall('[@]', domain))
        df['qty_and_domain'] = len(re.findall('[&]', domain))
        df['qty_exclamation_domain'] = len(re.findall('[!]', domain))
        df['qty_space_domain'] = len(re.findall('[ ]', domain))
        df['qty_tilde_domain'] = len(re.findall('[~]', domain))
        df['qty_comma_domain'] = len(re.findall('[,]', domain))
        df['qty_plus_domain'] = len(re.findall('[+]', domain))
        df['qty_asterisk_domain'] = len(re.findall('[*]', domain))
        df['qty_hashtag_domain'] = len(re.findall('[#]', domain))
        df['qty_dollar_domain'] = len(re.findall('[$]', domain))
        df['qty_percent_domain'] = len(re.findall('[%]', domain))
        df['qty_vowels_domain'] = self.vowels(domain)
        df['domain_length'] = len(domain)
        df['server_client_domain'] = self.server_client()

        dirr = url.raw_path
        lenn = len(dirr.split('/')) - 1
        split_dir = dirr.split('/')
        directory = ''
        if (lenn > 1):
            for i in range(0, lenn):
                directory += split_dir[i] + '/'
        # else:
        #     directory =''

        df['qty_dot_directory'] = len(re.findall('[.]', directory))
        df['qty_hyphen_directory'] = len(re.findall('[-]', directory))
        df['qty_underline_directory'] = len(re.findall('[_]', directory))
        df['qty_slash_directory'] = len(re.findall('[/]', directory))
        df['qty_questionmark_directory'] = len(re.findall('[?]', directory))
        df['qty_equal_directory'] = len(re.findall('[=]', directory))
        df['qty_at_directory'] = len(re.findall('[@]', directory))
        df['qty_and_directory'] = len(re.findall('[&]', directory))
        df['qty_exclamation_directory'] = len(re.findall('[!]', directory))
        df['qty_space_directory'] = len(re.findall('[ ]', directory))
        df['qty_tilde_directory'] = len(re.findall('[~]', directory))
        df['qty_comma_directory'] = len(re.findall('[,]', directory))
        df['qty_plus_directory'] = len(re.findall('[+]', directory))
        df['qty_asterisk_directory'] = len(re.findall('[*]', directory))
        df['qty_hashtag_directory'] = len(re.findall('[#]', directory))
        df['qty_dollar_directory'] = len(re.findall('[$]', directory))
        df['qty_percent_directory'] = len(re.findall('[%]', directory))
        df['directory_length'] = len(directory)

        file = '/' + split_dir[-1]

        df['qty_dot_file'] = len(re.findall('[.]', file))
        df['qty_hyphen_file'] = len(re.findall('[-]', file))
        df['qty_underline_file'] = len(re.findall('[_]', file))
        df['qty_slash_file'] = len(re.findall('[/]', file))
        df['qty_questionmark_file'] = len(re.findall('[?]', file))
        df['qty_equal_file'] = len(re.findall('[=]', file))
        df['qty_at_file'] = len(re.findall('[@]', file))
        df['qty_and_file'] = len(re.findall('[&]', file))
        df['qty_exclamation_file'] = len(re.findall('[!]', file))
        df['qty_space_file'] = len(re.findall('[ ]', file))
        df['qty_tilde_file'] = len(re.findall('[~]', file))
        df['qty_comma_file'] = len(re.findall('[,]', file))
        df['qty_plus_file'] = len(re.findall('[+]', file))
        df['qty_asterisk_file'] = len(re.findall('[*]', file))
        df['qty_hashtag_file'] = len(re.findall('[#]', file))
        df['qty_dollar_file'] = len(re.findall('[$]', file))
        df['qty_percent_file'] = len(re.findall('[%]', file))
        df['file_length'] = len(file)

        if (len(url.fragment) == 0):
            parameter = url.query_string
        elif (len(url.fragment) > 0):
            parameter = url.query_string + '#' + url.fragment

        df['qty_dot_params'] = len(re.findall('[.]', parameter))
        df['qty_hyphen_params'] = len(re.findall('[-]', parameter))
        df['qty_underline_params'] = len(re.findall('[_]', parameter))
        df['qty_slash_params'] = len(re.findall('[/]', parameter))
        df['qty_questionmark_params'] = len(re.findall('[?]', parameter))
        df['qty_equal_params'] = len(re.findall('[=]', parameter))
        df['qty_at_params'] = len(re.findall('[@]', parameter))
        df['qty_and_params'] = len(re.findall('[&]', parameter))
        df['qty_exclamation_params'] = len(re.findall('[!]', parameter))
        df['qty_space_params'] = len(re.findall('[ ]', parameter))
        df['qty_tilde_params'] = len(re.findall('[~]', parameter))
        df['qty_comma_params'] = len(re.findall('[,]', parameter))
        df['qty_plus_params'] = len(re.findall('[+]', parameter))
        df['qty_asterisk_params'] = len(re.findall('[*]', parameter))
        df['qty_hashtag_params'] = len(re.findall('[#]', parameter))
        df['qty_dollar_params'] = len(re.findall('[$]', parameter))
        df['qty_percent_params'] = len(re.findall('[%]', parameter))
        df['params_length'] = len(parameter)

        check_tld = get_tld(self.link, fail_silently=True)
        if (check_tld == None):
            df['tld_present_params'] = 0
        else:
            df['tld_present_params'] = 1

        df['qty_params'] = len(url.query)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_date = datetime.strptime(dt_string, '%d/%m/%Y %H:%M:%S')


        if self.is_registered(self.link):
            whois_info = whois.whois(self.link)

            # get the creation time
            time_domain_activation = (dt_date) - (whois_info.creation_date)
            #     print("Domain activation days:", (dt_date)-(whois_info.creation_date) )
            # get expiration date
            time_domain_expiration = (whois_info.expiration_date) - (dt_date)
            df['time_domain_activation'] = time_domain_activation.days
            df['time_domain_expiration'] = time_domain_expiration.days
        #     print("Domain Expiration days:", (whois_info.expiration_date)-(dt_date))
        else:
            df['time_domain_activation'] = 0
            df['time_domain_expiration'] = 0

        df['time_response'] = requests.get(self.link).elapsed.total_seconds()

        name_for_mx_and_ns = tldextract.extract(self.link).domain + '.' + tldextract.extract(self.link).suffix

        output_ns = self.finding_ns(name_for_mx_and_ns)
        if output_ns == False:
            df['qty_nameservers'] = 0
        else:
            count = 0
            for item in output_ns:
                count += 1
            df['qty_nameservers'] = count

        output_mx = self.finding_mx(name_for_mx_and_ns)

        if output_mx == False:
            df['qty_mx_servers'] = 0
        else:
            count = 0
            for item in output_mx:
                count += 1
            df['qty_mx_servers'] = count

        redirects = requests.get(self.link)
        df['qty_redirects'] = len(redirects.history)
        return df


    def get_default_dataframe(self):
        df = pd.DataFrame(pd.read_csv("link.csv")['Attribute'])
        all_cols = []
        col = ['domain_spf', 'asn_ip', 'qty_ip_resolved', 'ttl_hostname',
               'tls_ssl_certificate', 'url_google_index', 'domain_google_index', 'url_shortened', 'domain_in_ip',
               'phishing']
        for item in df['Attribute']:
            all_cols.append(item)
        df = pd.DataFrame(columns=all_cols)
        df.drop(columns=col, inplace=True)
        df.loc[0] = np.nan
        return df

    def predict(self):

        df = self.get_default_dataframe()
        df = self.get_col_details(df)
        print(df)