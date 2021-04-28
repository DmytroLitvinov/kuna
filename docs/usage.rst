=====
Usage
=====

To use Kuna API wrapper in a project::

    import kuna

    graph_kuna = kuna.KunaAPI()

    # If you need User methods, provide access_key and secret_key
    graph_kuna = kuna.KunaAPI(public_key='your_public_key', private_key='your_private_key')
