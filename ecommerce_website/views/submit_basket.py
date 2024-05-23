from flask import Blueprint, request
from ecommerce_website.apriori_algo import get_recommendations
from ecommerce_website.utils.response import response_with
import ecommerce_website.utils.response as resp
from ecommerce_website import rules

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