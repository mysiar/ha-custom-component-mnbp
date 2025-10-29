# Home Assistant custom component NBP

Provides
 - NBP exchange rates for today (table C) `*`
 - NBP gold price for today `*`

`*` - requires manual update via automation to fetch the latest data from NBP API.

## Sensor configuration

```yaml
sensor:
  - platform: mnbp
    type: exchange_today

  - platform: mnbp
    type: gold_today
```

## Automations

```yaml
- id: 'f2b0c78b-25b9-4ec2-9e9c-aa258cc8a4a1'
  alias: Update NBP Exchange Sensor Daily at 08:30
  description: Trigger manual update of NBP exchange rate sensor
  trigger:
    - platform: time
      at: "08:30:00"
  action:
    - service: homeassistant.update_entity
      target:
        entity_id: sensor.nbp_exchange_rate_today
  mode: single

- id: 'f2b0c78b-25b9-4ec2-9e9c-aa258cc8a4a2'
  alias: Update NBP Gold Sensor Daily at 08:30
  description: Trigger manual update of NBP gold price sensor
  trigger:
    - platform: time
      at: "08:30:00"
  action:
    - service: homeassistant.update_entity
      target:
        entity_id: sensor.nbp_gold_price_today
  mode: single
```

## Instalation
### 📦 Manual Installation

To install this integration manually, you need to download [**mnbp.zip**](https://github.com/mysiar/ha-custom-component-mnbp/releases/latest/download/mnbp.zip) and extract its contents to the `config/custom_components/mnbp` directory.


```bash
mkdir -p custom_components/mnbp
cd custom_components/mnbp
wget https://github.com/mysiar/ha-custom-component-mnbp/releases/latest/download/mnbp.zip
unzip mnbp.zip
rm mnbp.zip
```
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