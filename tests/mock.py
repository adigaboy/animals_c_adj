from unittest.mock import AsyncMock

tested_html = '''
<table>
  <tr>
    <th>Table0</th>
  </tr>
</table>

<table>
  <tr>
    <th>Table1</th>
  </tr>
</table>

<table>
  <tr>
    <th>Animal</th>
    <th>Collateral adjective</th>
  </tr>
  <tr>
    <td><a href="/wiki/Bat" title="Bat">Bat</a></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>noctillionine pteropine</td>
  </tr>
  <tr>
    <td><a href="/wiki/Bear" title="Bear">Bear</a></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>ursine</td>
  </tr>
  <tr>
    <td><a href="/wiki/Polar Bear" title="Polar Bear">Polar Bear</a></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>ursine</td>
  </tr>
  <tr>
    <td><a href="/wiki/Ape" title="Ape">Ape</a></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>simian</td>
  </tr>
  <tr>
    <td><a href="/wiki/Gorilla" title="Gorilla">Gorilla</a></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>simian</td>
  </tr>
  <tr>
    <td><a href="/wiki/Human" title="Human">Human</a></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>simian</td>
  </tr>
</table>
'''

async def mock_download_images(*args, **kwargs):
    return args[1:]

class aiohttp_clientsession_mock(AsyncMock):
    status = 200
    def __init__(self):
        pass
    def get(self, *args, **kwargs):
        return base_response_class()
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class base_response_class(AsyncMock):
    status = 200
    def __init__(self):
        pass
    def get(self, *args, **kwargs):
        pass
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def text(self):
        return tested_html
