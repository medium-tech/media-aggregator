"""
OpenSearch client configuration.
"""

import os
from typing import Optional
from opensearchpy import OpenSearch


def get_opensearch_client(
    host: Optional[str] = None,
    port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    use_ssl: Optional[bool] = None,
) -> OpenSearch:
    """
    Get configured OpenSearch client.
    
    Args:
        host: OpenSearch host (defaults to env or 'localhost')
        port: OpenSearch port (defaults to env or 9200)
        username: OpenSearch username (defaults to env or 'admin')
        password: OpenSearch password (defaults to env, REQUIRED for production)
        use_ssl: Whether to use SSL (defaults to env or False)
    
    Returns:
        Configured OpenSearch client
    
    Note:
        For production use, always set OPENSEARCH_PASSWORD in environment variables.
        The 'admin' default is only for local development.
    """
    host = host or os.getenv("OPENSEARCH_HOST", "localhost")
    port = int(port or os.getenv("OPENSEARCH_PORT", "9200"))
    username = username or os.getenv("OPENSEARCH_USERNAME", "admin")
    # Default 'admin' password is for local development only
    password = password or os.getenv("OPENSEARCH_PASSWORD", "admin")
    use_ssl = use_ssl if use_ssl is not None else os.getenv("OPENSEARCH_USE_SSL", "false").lower() == "true"
    
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=(username, password),
        use_ssl=use_ssl,
        verify_certs=False,
        ssl_show_warn=False,
    )
    
    return client
