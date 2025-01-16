from tabulate import tabulate as tb
import matplotlib.pyplot as plt

driver_data = []
racer_info = {}


def racer_data(file):
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4:
                code, full_name, team = parts[1], parts[2], parts[3]
                racer_info[code] = {"name": full_name, "team": team}


def lap_data_store(lap_file, lap_no):
    with open(lap_file, 'r') as lap:
        next(lap)
        for line in lap:
            driver_code = line[:3]
            speed = float(line[3:].strip())
            if driver_code in racer_info:
                full_name = racer_info[driver_code]["name"]
                team = racer_info[driver_code]["team"]
            else:
                full_name = "unknown"
                team = "unknown"
            driver_data.append({"driver": driver_code,
                                "full name": full_name,
                                "team": team,
                                "car speed": speed,
                                "lap": lap_no})


def race_name(lap_file, lap_no):
    with open(lap_file, 'r') as f:
        location = f.readline().strip()
        print(f"Lap {lap_no} race is in {location}.")


def fastest_racer(lap_no):
    lap_data = [entry for entry in driver_data if entry["lap"] == lap_no]
    fastest = max(lap_data, key=lambda x: x["car speed"])
    print(f"the fastest racer in lap {lap_no}:")
    print(
        f"Driver: {fastest['full name']} ({fastest["driver"]}), team:{fastest["team"]}, speed: {fastest['car speed']:.3f}")


def fast_individual_racer():
    individual_drive_speed = {}

    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])

        if driver not in individual_drive_speed or speed < individual_drive_speed[driver]["speed"]:
            individual_drive_speed[driver] = {
                "full name": entry["full name"],
                "team": entry["team"],
                "speed": speed
            }

    table = [{"driver": info["full name"], "Team": info["team"], "fastest time": info["speed"]}
             for info in individual_drive_speed.values()]

    print("individual fastest time of every racer:")
    print(tb(table, headers="keys", tablefmt="fancy_grid"))


def fast_individual_racer_descending():
    individual_drive_speed_descend = {}

    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])

        if driver not in individual_drive_speed_descend or speed < individual_drive_speed_descend[driver]["speed"]:
            individual_drive_speed_descend[driver] = {
                "full name": entry["full name"],
                "team": entry["team"],
                "speed": speed
            }

    table = [{"driver": info["full name"], "Team": info["team"], "fastest time": info["speed"]}
             for info in individual_drive_speed_descend.values()]

    table.sort(key=lambda x: x["fastest time"], reverse=True)

    print("individual fastest time of every racer(in descending order):")
    print(tb(table, headers="keys", tablefmt="fancy_grid"))


def average_speed_racers():
    total_speed = sum(entry["car speed"] for entry in driver_data)
    total_driver = len(driver_data)
    average_time = total_speed / total_driver if total_driver else print("no data on driver.")
    print(f"the average time of overall racers is: {average_time:.2f}")


def average_speed_individual():
    racer_average = {}

    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])

        if driver not in racer_average:
            racer_average[driver] = {"total time": 0, "count": 0, "full name": entry["full name"],
                                     "team": entry["team"]}
        racer_average[driver]["total time"] += speed
        racer_average[driver]["count"] += 1

    average = [{"driver": data["full name"], "team": data["team"],
                "average time": data["total time"] / data["count"]}
               for data in racer_average.values()]
    average.sort(key=lambda x: x["average time"], reverse=True)

    print("average speed of every racer:")
    print(tb(average, headers="keys", tablefmt="fancy_grid"))


def plot_fastest_racers():
    individual_drive_speed = {}

    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])

        if driver not in individual_drive_speed or speed < individual_drive_speed[driver]["speed"]:
            individual_drive_speed[driver] = {
                "full name": entry["full name"],
                "speed": speed
            }

    drivers = [info["full name"] for info in individual_drive_speed.values()]
    speeds = [info["speed"] for info in individual_drive_speed.values()]

    plt.figure(figsize=(10, 6))
    plt.barh(drivers, speeds, color="skyblue")
    plt.xlabel("fastest speed(seconds)")
    plt.ylabel("racers")
    plt.title("fastest speed of racers")
    plt.show()


def plot_average_speed():
    racer_average = {}

    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])

        if driver not in racer_average:
            racer_average[driver] = {"total time": 0, "count": 0,
                                     "full name": entry["full name"], "team": entry["team"]}
        racer_average[driver]["total time"] += speed
        racer_average[driver]["count"] += 1

    drivers = [data["full name"] for data in racer_average.values()]
    averages = [data["total time"] / data["count"] for data in racer_average.values()]

    plt.figure(figsize=(10, 6))
    plt.barh(drivers, averages, color="lightcoral")
    plt.xlabel("average speed")
    plt.ylabel("racers")
    plt.title("average speed of all racers")
    plt.show()


def option():
    while True:
        print("menu")
        print("1. lap1")
        print("2. lap2")
        print("3. lap3")
        print("4. view graphs")
        print("5. exit")
        choice = input("choose a lap:")

        if choice not in ["1", "2", "3", "4"]:
            print("invalid choice, please try again.")
            continue
        if choice == "5":
            print("exiting the data.")
            break
        elif choice == "4":
            while True:
                print("option for graph")
                print("1. graph for fastest")
                print("2. graph for average")
                print("3. back to main menu")
                grpah_choice = input("enter your option:")

                if grpah_choice == "1":
                    plot_fastest_racers()
                elif grpah_choice == "2":
                    plot_average_speed()
                elif grpah_choice == "3":
                    break
                else:
                    print("invalid choice, please enter again.")
        else:
            lap_no = int(choice)
            race_name(f"project1/lap_times_{lap_no}.txt", lap_no)

            while True:
                print(f"lap{lap_no} option:")
                print("1. fastest Racer:")
                print("2. individual speed list")
                print("3. individual speed list(descending)")
                print("4. average speed")
                print("5. individual average list")
                print("6. back to main menu")
                sub_choice = input("choose the option:")

                if sub_choice == "1":
                    fastest_racer(lap_no)

                elif sub_choice == "2":
                    fast_individual_racer()

                elif sub_choice == "3":
                    fast_individual_racer_descending()

                elif sub_choice == "4":
                    average_speed_racers()

                elif sub_choice == "5":
                    average_speed_individual()

                elif sub_choice == "6":
                    break

                else:
                    print("invalid choice. please enter again.")


racer_data("project1/f1_drivers.txt")
lap_data_store("project1/lap_times_1.txt", 1)
lap_data_store("project1/lap_times_1.txt", 2)
lap_data_store("project1/lap_times_3.txt", 3)
option()