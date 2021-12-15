import modi
import time
import asyncio
import os


bundle = modi.MODI()


class CoinClassifier:
    def __init__(self):
        # Module Init - CHANGE ORDERS IF NEEDED / IT CHANGES MOSTLY EVERYTIME.
        self.ir1, self.ir2, self.ir3, self.ir4 = bundle.irs
        self.motor2, self.motor1 = bundle.motors
        self.d5, self.d1, self.d2, self.d3, self.d4  = bundle.displays

        # Balance Init - total: Won, rest: number of coins
        self.total = 0
        self.tens = 0
        self.fifties = 0
        self.hundreds = 0
        self.fivehundreds = 0

        # Motor location Init
        self.motor1.second_degree = 75
        self.motor1.first_degree = 75
        self.motor2.second_degree = 75
        self.motor2.first_degree = 75
        time.sleep(0.4)
        self.motor1.second_degree = 60
        self.motor1.first_degree = 60
        self.motor2.second_degree = 60
        self.motor2.first_degree = 60
        time.sleep(0.5)
        self.motor1.second_degree = 75
        self.motor1.first_degree = 75
        self.motor2.second_degree = 75
        self.motor2.first_degree = 75

        # Display Init
        self.d1.text = f"10's: {self.tens}"
        self.d2.text = f"50's: {self.fifties}"
        self.d3.text = f"100's: {self.hundreds}"
        self.d4.text = f"500's: {self.fivehundreds}"
        self.d5.text = f"-Total-\n {self.total}"


    async def check_for_input(self, period: int) -> list:
        sensitivity = 40
        result = []
        while True:
            print(f"{self.ir4.proximity}   {self.ir3.proximity}   {self.ir2.proximity}    {self.ir1.proximity}")
            if self.ir1.proximity > sensitivity:
                print("IR1 (10) Coin Detected")
                result.append(self.ir1)

            if self.ir2.proximity > sensitivity:
                print("IR2 (50) Coin Detected")
                result.append(self.ir2)

            if self.ir3.proximity > sensitivity:
                print("IR3 (100) Coin Detected")
                result.append(self.ir3)

            if self.ir4.proximity > sensitivity:
                print("IR4 (500) Coin Detected")
                result.append(self.ir4)

            await asyncio.sleep(period)
            if result:
                return result


    def update_balance(self, detected: list) -> None:
        if self.ir1 in detected:
            self.tens += 1
            self.total += 10
            self.motor2.first_degree = 75
            time.sleep(0.4)
            self.motor2.first_degree = 60
            time.sleep(0.5)
            self.motor2.first_degree = 75

        if self.ir2 in detected:
            self.fifties += 1
            self.total += 50
            self.motor2.second_degree = 75
            time.sleep(0.4)
            self.motor2.second_degree = 60
            time.sleep(0.5)
            self.motor2.second_degree = 75

        if self.ir3 in detected:
            self.hundreds += 1
            self.total += 100
            self.motor1.first_degree = 75
            time.sleep(0.4)
            self.motor1.first_degree = 60
            time.sleep(0.5)
            self.motor1.first_degree = 75

        if self.ir4 in detected:
            self.fivehundreds += 1
            self.total += 500
            self.motor1.second_degree = 75
            time.sleep(0.4)
            self.motor1.second_degree = 60
            time.sleep(0.5)
            self.motor1.second_degree = 75


    def show_balance(self) -> None:
        self.d1.text = f"10's: {self.tens}"
        self.d2.text = f"50's: {self.fifties}"
        self.d3.text = f"100's: {self.hundreds}"
        self.d4.text = f"500's: {self.fivehundreds}"
        self.d5.text = f"-Total-\n {self.total}"


    def get_total_balance(self) -> int:
        return self.total

async def main():
    bank = CoinClassifier()

    while True:
        print("Checking for coins!...")
        detected = await bank.check_for_input(period=1)
        bank.update_balance(detected)
        bank.show_balance()
        print(f"Total balance: {bank.get_total_balance()}")


if __name__ == "__main__":
    if len(bundle.irs) != 4:
        print(f"IR sensor is missing! (Recognized: {len(bundle.irs)})")
        exit(1)

    if len(bundle.motors) != 2:
        print(f"Motor is missing! (Recognized: {len(bundle.motors)})")
        exit(1)

    if len(bundle.displays) != 5:
        print(f"Display is missing! (Recognized: {len(bundle.displays)})")
        exit(1)

    asyncio.run(main())

