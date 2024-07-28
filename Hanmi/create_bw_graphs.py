import pandas as pd
import matplotlib.pyplot as plt
import os

hanmi_folder = r"C:\Users\Andrew\Downloads\hanmi_automation"
os.mkdir(r"C:\Users\Andrew\Downloads\hanmi_graphs")

for csv_file in os.listdir(hanmi_folder):
    print(csv_file)
    if os.stat(rf"{hanmi_folder}\{csv_file}").st_size < 1000:
        continue  # Skip if no useful contents in CSV file

    if csv_file[0].lower() == "b":
        bw = pd.read_csv(
            rf"{hanmi_folder}\{csv_file}",
            header=3,
            usecols=[2, 3, 7],
        )

        # Formatting data frame
        bw.reset_index(drop=True, inplace=True)
        bw["Date/Time"] = pd.to_datetime(bw["Date/Time"])
        # cpu_load["Date/Time.2"] = cpu_load["Date/Time.2"].dt.strftime('%m/%d/%Y')
        bw = bw.resample("D", on="Date/Time").mean()
        bw["Value"] /= 1000000  # Convert to Mbps
        bw["Value.1"] /= 1000000  # Convert to Mbps

        ax = bw.plot.bar(figsize=(6, 6), zorder=2)
        # ax.set_ylim([0, 100])  # Uncomment when generating empty bandwidth graphs

        # ax.set_title(csv_file[:-4], fontsize=14, color="#444444")
        ax.legend(["Avg-Tx", "Avg-Rx"])

        xticks = [tick.get_text() for tick in ax.get_xticklabels()]
        xticks = pd.to_datetime(xticks).strftime('%m/%d/%Y')
        ax.set_xlabel("")
        ax.set_xticklabels(xticks, fontsize=8, color="#444444")

        yticks = [tick.get_text() + " Mbps" for tick in ax.get_yticklabels()]
        ax.set_yticklabels(yticks, fontsize=8, color="#444444")

        ax.tick_params(left=False, color="#AAAAAA")

        ax.grid(axis="y", zorder=-10)
        ax.spines["bottom"].set_color("#AAAAAA")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.savefig(rf'C:\Users\Andrew\Downloads\hanmi_graphs\{csv_file[:-4]}', bbox_inches="tight")
        plt.close()
