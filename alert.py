from win11toast import toast
import psutil
import time

class BatteryMonitor:
    def __init__(self):
        self.low_notified = False
        self.full_notified = False
        self.last_low_notify = 0
        self.last_full_notify = 0
        self.cooldown = 15 * 60

    def get_battery_info(self):
        battery = psutil.sensors_battery()
        if battery is None:
            return None
        return {
            "percent": battery.percent,
            "plugged": battery.power_plugged
        }

    def process(self):
        data = self.get_battery_info()
        if not data:
            return None

        percent = data['percent']
        is_plugged = data['plugged']
        now = time.time()

        if percent <= 40 and not is_plugged:
            if (not self.low_notified) or (now - self.last_low_notify > self.cooldown):
                self.low_notified = True
                self.last_low_notify = now
                return {
                    "title": "Battery Low (Health Alert)",
                    "msg": f"Battery is at {percent}%. Please plug in your charger."
                }
        else:
            self.low_notified = False
            self.last_low_notify = 0

        if percent >= 80 and is_plugged:
            if (not self.full_notified) or (now - self.last_full_notify > self.cooldown):
                self.full_notified = True
                self.last_full_notify = now
                return {
                    "title": "Battery Charged (Health Alert)",
                    "msg": f"Battery is at {percent}%. Remove the charger."
                }
        else:
            self.full_notified = False
            self.last_full_notify = 0

        return None

    def run(self):
        print("Monitoring Windows Battery (Press Ctrl+C to stop)...")
        while True:
            alert_data = self.process()
            if alert_data:
                toast(alert_data['title'], alert_data['msg'])
            time.sleep(5)

if __name__ == "__main__":
    monitor = BatteryMonitor()
    monitor.run()
