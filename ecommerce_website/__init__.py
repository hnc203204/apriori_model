from flask import Flask
from ecommerce_website.apriori_algo.aprori import apriori_mlxtend
import os

app = Flask(__name__)
itemsets, rules = apriori_mlxtend(os.path.realpath(".") + '/data_processing/transactions.csv', min_support=0.001, min_confidence=1.0)

from ecommerce_website.views.submit_basket import submit_basket

app.register_blueprint(submit_basket, url_prefix='/api')



