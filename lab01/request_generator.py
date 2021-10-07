import requests
import time
import csv

def main():
    with open("e5_timings_1.csv", "a", newline="") as file:
      writer = csv.writer(file, delimiter=";")
      limits = [100, 200, 400, 800, 1600, 3200]
      for limit in limits:
        for iteration in range(15):
          start_time = time.time_ns() / 1_000_000 # Time in ms
          resp = requests.get(f"https://europe-west6-scad-zhaw.cloudfunctions.net/lab01/recommend?limit={limit}")
          end_time = time.time_ns() / 1_000_000

          if resp.ok:
            print(f"iteration: {iteration}, time: {end_time-start_time}")
            writer.writerow([iteration, end_time-start_time])

if __name__ == "__main__":
  main()
