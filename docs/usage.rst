=====
Usage
=====

To use Kuna API wrapper in a project::

    import kuna

    graph_kuna = kuna.KunaAPI()

    # If you need User methods, provide access_key and secret_key
    graph_kuna = kuna.KunaAPI(access_key='your_access_key', secret_key='your_secret_key')
