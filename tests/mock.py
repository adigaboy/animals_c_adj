from unittest.mock import MagicMock

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
    <td>Bat</td>
    <td>noctillionine pteropine</td>
  </tr>
  <tr>
    <td>Bear</td>
    <td>ursine</td>
  </tr>
  <tr>
    <td>Polar Bear</td>
    <td>ursine</td>
  </tr>
  <tr>
    <td>Ape</td>
    <td>simian</td>
  </tr>
  <tr>
    <td>Gorilla</td>
    <td>simian</td>
  </tr>
  <tr>
    <td>Human</td>
    <td>simian</td>
  </tr>
</table>
'''


def mock_page_response(*args):
    mock_page = MagicMock()
    mock_page.html = MagicMock(return_value=tested_html)
    return mock_page
