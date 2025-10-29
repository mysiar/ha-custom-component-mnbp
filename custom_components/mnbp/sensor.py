import logging
import requests
from datetime import timedelta, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

EXCHANGE_TODAY_INTERVAL = 600
GOLD_TODAY_INTERVAL = 600

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:

    """Set up MNBP sensors based on type."""
    sensor_type = config.get("type")
    entities = []

    if sensor_type == "exchange_today":
        entities.append(MNBPExchangeSensorToday())
    elif sensor_type == "gold_today":
        entities.append(MNBPGoldSensorToday())
    else:
        _LOGGER.warning("Unknown sensor type: %s", sensor_type)

    add_entities(entities, update_before_add=True)


class BaseNBPSensor(SensorEntity):
    """Base NBP sensor class."""

    def __init__(self, name: str, interval: int) -> None:
        self._attr_name = name
        self._attr_scan_interval = timedelta(seconds=interval)
        self._last_update: str | None = None

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "last_update": self._last_update,
        }

    def update(self) -> None:
        self._last_update = datetime.now().isoformat()
        _LOGGER.debug("Sensor '%s' updated at %s", self.name, self._last_update)


class MNBPExchangeSensorToday(BaseNBPSensor):
    """
    Sensor kursów walut NBP (dzisiejszy).

    Żródło: https://api.nbp.pl/api/exchangerates/tables/C/today/
    """

    def __init__(self) -> None:
        self._attr_unique_id = "nbp_exchange_today"
        self._rates = []
        super().__init__("NBP Exchange Rates Today", EXCHANGE_TODAY_INTERVAL)

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "last_update": self._last_update,
            "rates": self._rates,
        }

    def update(self) -> None:
        url = "https://api.nbp.pl/api/exchangerates/tables/C/today/"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            payload = response.json()
            self._rates = payload[0].get("rates", [])
            usd = next((r for r in self._rates if r["code"] == "USD"), None)
            self._attr_native_value = usd["bid"] if usd else None            
            super().update()
        except Exception as e:
            _LOGGER.error("Failed to fetch NBP data for today gold price !")
            self._attr_native_value = "Error"
            self.self._attr_native_value = None


class MNBPGoldSensorToday(BaseNBPSensor):
    """
    Sensor ceny złota NBP (dzisiejsza).

    Źródło: https://api.nbp.pl/api/cenyzlota/today
    """

    def __init__(self) -> None:
        self._attr_unique_id = "nbp_gold_today"
        super().__init__("NBP Gold Price Today", GOLD_TODAY_INTERVAL)

    def update(self) -> None:
        url = "https://api.nbp.pl/api/cenyzlota/today"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            payload = response.json()
            self._attr_native_value = payload[0]["cena"]
            super().update()
        except Exception as e:
            _LOGGER.error("Failed to fetch NBP data for today gold price !")
            self._attr_native_value = "Error"
            self.self._attr_native_value = None