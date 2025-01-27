from src.external_fridge_monitor import ExternalFridgeMonitor
from src.internal_fridge_monitor import InternalFridgeMonitor
import threading


def monitoring_fridge_extern():
    fm = ExternalFridgeMonitor()
    fm.monitoring_loop()


def main():
    monitoring_fridge_extern()   


if __name__ == "__main__":
    main()