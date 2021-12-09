.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: reverse-dns-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/reverse-dns.svg
    :alt: reverse-dns-py release
    :target: https://pypi.org/project/reverse-dns

.. image:: https://github.com/whois-api-llc/reverse-dns-py/workflows/Build/badge.svg
    :alt: reverse-dns-py build
    :target: https://github.com/whois-api-llc/reverse-dns-py/actions

========
Overview
========

The client library for
`Reverse DNS API <https://reverse-dns.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.6.

Installation
============

.. code-block:: shell

    pip install reverse-dns

Examples
========

Full API documentation available `here <https://reverse-dns.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

.. code-block:: python

    from reversedns import *

    client = Client('Your API key')

Make basic requests
-------------------

.. code-block:: python

    terms = [{
        'field': 'domain',
        'term': 'foo*'
    }]

    # Get DNS records for matching domains (up to 1000)
    result = client.get(terms=terms, record_type=Client.TXT)

    # Total count
    print(result.size)

Extras
-------------------

.. code-block:: python

    terms = [
        {
            'field': 'domain',
            'term': 'blog*'
        },
        {
            'field': 'value',
            'term': 'foo*',
            'exclude': True
        }
    ]

    # Exclude specified records for matching domains and get raw XML response
    raw_result = client.get_raw(
        terms=terms,
        record_type=Client.CNAME,
        limit=2,
        output_format=Client.XML_FORMAT)

Response model overview
-----------------------

.. code-block:: python

    Response:
        - result: [Record]
            - value: str
            - name: str
            - first_seen: str
            - last_vist: str
        - size: int

