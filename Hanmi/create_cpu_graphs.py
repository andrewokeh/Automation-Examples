import pandas as pd
import matplotlib.pyplot as plt
import os

hanmi_folder = r"C:\Users\Andrew\Downloads\hanmi_automation"
os.mkdir(r"C:\Users\Andrew\Downloads\hanmi_graphs")


def create_cpu_graph(csv_file, data_type):
    type_var = ""
    type_columns = []
    var_num = 0

    if data_type == "avg":
        type_var = "Average"
        type_columns = [10, 11]
        var_num = 2
    elif data_type == "max":
        type_var = "Peak"
        type_columns = [6, 7]
        var_num = 1

    if csv_file[0] == "C":
        cpu_load = pd.read_csv(
            rf"{hanmi_folder}\{csv_file}",
            header=3,  # May need to be 3 or 4 depending on if there is an empty row of commas or not
            usecols=type_columns,
        )

        # Formatting data frame
        cpu_load.reset_index(drop=True, inplace=True)
        cpu_load[f"Date/Time.{var_num}"] = pd.to_datetime(cpu_load[f"Date/Time.{var_num}"])
        # cpu_load["Date/Time.2"] = cpu_load["Date/Time.2"].dt.strftime('%m/%d/%Y')
        cpu_load = cpu_load.resample("D", on=f"Date/Time.{var_num}").mean()

        ax = cpu_load.plot.bar(figsize=(6, 3), color="#4472C4", zorder=2)
        # ax.set_ylim([0, 100])  # Uncomment when making empty CPU graphs

        # ax.set_title(csv_file[:-4], fontsize=14, color="#444444")
        ax.get_legend().remove()

        xticks = [tick.get_text() for tick in ax.get_xticklabels()]
        xticks = pd.to_datetime(xticks).strftime('%m/%d/%Y')
        ax.set_xlabel("")
        ax.set_xticklabels(xticks, fontsize=8, color="#444444")

        ax.set_ylabel(f"{type_var} CPU Load", fontsize=12, color="#444444")
        yticks = [tick.get_text() + "%" for tick in ax.get_yticklabels()]
        ax.set_yticklabels(yticks, fontsize=8, color="#444444")

        ax.tick_params(left=False, color="#AAAAAA")

        ax.grid(axis="y", zorder=-10)
        ax.spines["bottom"].set_color("#AAAAAA")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.savefig(rf'C:\Users\Andrew\Downloads\hanmi_graphs\{csv_file[:-4]}-{type_var}', bbox_inches="tight")
        plt.close()


for file in os.listdir(hanmi_folder):
    print(file)
    if os.stat(rf"{hanmi_folder}\{file}").st_size < 1000:
        continue  # Skip if no useful contents in CSV file
    create_cpu_graph(file, "avg")
    create_cpu_graph(file, "max")
