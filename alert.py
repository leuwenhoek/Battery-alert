from plyer import notification
import psutil
import time

class Battery_notify:
    def __init__(self):
        self.full_notified = False
        self.low_notified = False
        pass

    def get_battery_info(self):
        battery = psutil.sensors_battery()
        percent = battery.percent
        is_plugged = battery.power_plugged

        parsed_data = {
            "Percentage" : percent,
            "Is_plugged" : is_plugged
        }

        return parsed_data

    def process(self):

        """
            if battery_percentage <= 40% and not charging then:
                alert user to start charging
            
            if battery_percentage >=80% and charging then:
                alert user to stop charging
        """

        data = self.get_battery_info()

        if data['Percentage'] <= 40 and data['Is_plugged'] == False:
            if not self.low_notified:
                self.low_notified = True
                self.full_notified = False
            return [f'''{data['Percentage']}% battery is left.
Charge the device your device for better battery Health.''',"Charge your device"]

        elif data['Percentage'] >= 80 and data['Is_plugged'] == True:
            if not self.full_notified:
                self.full_notified = True
                self.low_notified = False
            return [f'''{data['Percentage']}% battery is left.
Remove the charger your device for better battery Health.''',"Remove your device from charge"]
        
        if data['Percentage'] > 40:
            self.low_notified = False
        if data['Percentage'] < 80:
            self.full_notified = False

    def Alert(self,message_):
        if message_:
            verdic = message_[1]
            notification.notify(
                title = verdic,
                message = message_[0],
                timeout = 5
            )

    def run_bg(self):
        while True:
            self.Alert(self.process())
            time.sleep(10)


def main():
    battery = Battery_notify()
    battery.run_bg()
    return 0

if __name__ == "__main__":
    main()