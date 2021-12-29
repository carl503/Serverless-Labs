import asyncio
import time
from threading import Thread, Condition
from bleak import BleakScanner

running = True
cond = Condition()

def main():
    global running, cond

    beacons = [
        "AC:23:3F:82:6E:25",
        "AC:23:3F:85:1F:1A"
    ]
    threads = []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for beacon in beacons:
        try:
            thread = BeaconInteraction(beacon, loop)
            threads.append(thread)
            thread.start()
        except Exception as e:
            print("thread could not be started", e)

    while(running):
        terminate = input("Do you want to exit? (y/n):\n")
        if (terminate == "yes" or terminate == "y"):
            with cond:
                running = False
                cond.notify_all()
                
    for thread in threads:
        thread.join()

    loop.close()

class BeaconInteraction(Thread):
    def __init__(self, beacon_id: str, loop, timeout: int = 30):
        Thread.__init__(self)
        self.beacon_id = beacon_id
        self.timeout = timeout
        self.loop = loop

    def run(self):
        print(f"starting beacon listener for beacon id: {self.beacon_id}")
        while(running):
            with cond:
                self.loop.run_until_complete(self.poll_distance())
                cond.wait(self.timeout)         

    async def poll_distance(self):
        device = await BleakScanner.find_device_by_address(self.beacon_id, timeout = self.timeout) 
        if device is not None:
            print(f"{self.beacon_id} distance: {device.rssi}")
        else:
            print(f"could not read value of {self.beacon_id}")
        

if __name__ == "__main__":
    main()
