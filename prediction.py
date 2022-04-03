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
    def init(self,link):
        self.link = link