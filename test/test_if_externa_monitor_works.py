from src.external_fridge_monitor import ExternalFridgeMonitor

def start():
    print('starting test')
    monitor = ExternalFridgeMonitor()
    monitor.setupSerial()
    monitor.monitoring_loop()


if __name__ == "__main__":
    start()
