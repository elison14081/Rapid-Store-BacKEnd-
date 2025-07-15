from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    # --- AÑADE ESTE MÉTODO ---
    def ready(self):
        """
        Importa los modelos (y por lo tanto las señales) cuando la aplicación está lista.
        """
        import products.models