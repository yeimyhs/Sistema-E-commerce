import requests
from django.conf import settings

class IzipayClient:
    """
    Cliente para interactuar con la API de Izipay.
    """
    def __init__(self):
        # URL de la API de sandbox (modificar a producción cuando sea necesario)
        self.api_url = settings.IZIPAY_API_URL
        self.public_key = settings.IZIPAY_PUBLIC_KEY
        self.secret_key = settings.IZIPAY_SECRET_KEY

    def create_payment(self, amount, currency, order_id, customer_email, description):
        """
        Crea un pago en Izipay.
        :param amount: Monto en la menor denominación (e.g., 100.00 = 10000).
        :param currency: Código de moneda (e.g., "PEN").
        :param order_id: Identificador único del pedido.
        :param customer_email: Email del cliente.
        :param description: Descripción del pago.
        """
        url = f"{self.api_url}/v1/payment"
        headers = {
            "Authorization": f"Basic {self.public_key}:{self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "amount": amount,
            "currency": currency,
            "orderId": order_id,
            "customer": {"email": customer_email},
            "description": description,
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()  # Respuesta de éxito
        else:
            response.raise_for_status()  # Lanza un error en caso de fallo
