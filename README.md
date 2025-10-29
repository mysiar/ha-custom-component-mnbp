# Home Assistant custom component NBP

Provides
 - NBP exchange rates for today (table C)
 - NBP gold price for today

## Sensor configuration

```yaml
sensor:
  - platform: mnbp
    type: exchange_today

  - platform: mnbp
    type: gold_today
```

## Instalation
### 📦 Manual Installation

## Display data (markdown-card)
### exchange_today

#### markdown table display
```yaml
{% set rates = state_attr('sensor.nbp_exchange_rate_today', 'rates') %} 
{% if rates %}
|Kod   | Kupno   | Sprzedaż | Waluta|
|------|---------|----------|-------|{% for r in rates %}
| {{ "%-5s"|format(r.code) }} | {{"%7.4f"|format(r.bid) }} | {{ "%8.4f"|format(r.ask) }} | {{ r.currency }} |{% endfor %} {% else %} _Brak danych kursów walut._ {% endif %}
```

#### html table display
```yaml
{% set rates = state_attr('sensor.nbp_exchange_rate_today', 'rates') %}
  {% if rates %}
  <table width="100%" border="1" style="border-collapse:collapse;">
    <tr><th align="center">Kod</th><th align="center">Kupno</th><th align="center">Sprzedaż</th><th align="center">Waluta</th></tr>
    {% for r in rates %}<tr>
      <td align="center">{{ r.code }}</td>
      <td align="center">{{ "%.4f"|format(r.bid) }} zł</td>
      <td align="center">{{ "%.4f"|format(r.ask) }} zł</td>
      <td align="left">{{ r.currency }}</td>
    </tr>{% endfor %}
  </table>
  {% else %}
  <p><em>Brak danych kursów walut.</em></p>
  {% endif %}
```
### gold_today

```
{% set sensor = 'sensor.nbp_gold_price_today' %}
{% set value = states(sensor) %}
{{value}} zł
```