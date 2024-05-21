from flask import Blueprint, request
from apriori_api.apriori_algo import get_recommendations
from apriori_api.utils.response import response_with
import apriori_api.utils.response as resp
from apriori_api import rules

submit_basket = Blueprint('submit_basket', __name__)

@submit_basket.route('/submit_basket', methods=['POST'])
def submit_basket_route():
    basket = request.json['basket']
    print(basket)
    if basket is None:
        return response_with(resp.BAD_REQUEST_400)
    recommendations = get_recommendations(basket, rules)
    print(recommendations)
    return response_with(resp.SUCCESS_200, value=recommendations)