# paypal_client.py
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from dotenv import load_dotenv
import os

load_dotenv()  # Esto carga el contenido del .env
paypal_id = os.getenv("PAYPAL_CLIENT_ID")
paypal_client = os.getenv("PAYPAL_CLIENT_SECRET")
class PayPalClient:
    def __init__(self):
        self.client_id = paypal_id
        self.client_secret = paypal_client
        self.environment = SandboxEnvironment(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.client = PayPalHttpClient(self.environment)

paypal_client = PayPalClient()
