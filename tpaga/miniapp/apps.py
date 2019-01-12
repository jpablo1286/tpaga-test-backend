from django.apps import AppConfig

# Se agrega parametros de configuracion dependientes de la variable ENV
class MiniappConfig(AppConfig):
    name = 'miniapp'
    def getConfig(env):
        if env == 'dev':
            CONFIG = {
            'DEBUG' : True,
            'MINIAPP_BASE_URL':'https://localhost:4200',
            'TPAGA_API_BASE_URL':'https://stag.wallet.tpaga.co',
            'TPAGA_PAYMENT_REQUEST_PATH':'merchants/api/v1/payment_requests'
            }
            return CONFIG
        if env == 'prod':
            CONFIG = {
            'DEBUG' : False,
            'MINIAPP_BASE_URL':'https://miniapp.juanrivera.org',
            'TPAGA_API_BASE_URL':'https://stag.wallet.tpaga.co',
            'TPAGA_PAYMENT_REQUEST_PATH':'merchants/api/v1/payment_requests'
            }
            return CONFIG
