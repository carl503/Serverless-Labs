import requests
import time
import csv

def main():
    with open("e5_timings.csv", "a", newline="") as file:
      writer = csv.writer(file, delimiter=";")
      sleep_intervals = [10, 20, 40, 80, 160, 320, 500] # in s
      for interval in sleep_intervals:
        for iteration in range(15):
          start_time = time.time_ns() / 1_000_000 # Time in ms
          resp = requests.get("https://europe-west6-scad-zhaw.cloudfunctions.net/lab01/recommend")
          end_time = time.time_ns() / 1_000_000

          if resp.ok:
            print(f"iteration: {iteration}, time: {end_time-start_time}")
            writer.writerow([iteration, end_time-start_time])

if __name__ == "__main__":
  main()
