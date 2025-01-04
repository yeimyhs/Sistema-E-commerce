# externalapi/services.py

from .api_client_izipay import ExternalAPIClient

def create_card_token(transaction_id, merchant_code, card_data, buyer_data, billing_address):
    endpoint = "tokens"
    data = {
        "transactionId": transaction_id,
        "merchantCode": merchant_code,
        "card": card_data,
        "buyer": buyer_data,
        "billingAddress": billing_address,
    }
    return ExternalAPIClient.make_request(endpoint, method='POST', data=data)

def get_token_data(transaction_id, merchant_code, card_token, buyer_data):
    endpoint = "tokens/token"
    data = {
        "transactionId": transaction_id,
        "merchantCode": merchant_code,
        "token": {
            "cardToken": card_token,
        },
        "buyer": buyer_data,
    }
    return ExternalAPIClient.make_request(endpoint, method='POST', data=data)

def list_tokens(transaction_id, merchant_code, buyer_data):
    endpoint = "tokens/tokens"
    data = {
        "transactionId": transaction_id,
        "merchantCode": merchant_code,
        "buyer": buyer_data,
    }
    return ExternalAPIClient.make_request(endpoint, method='POST', data=data)
