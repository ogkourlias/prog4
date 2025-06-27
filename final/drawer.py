import os
import matplotlib.pyplot as plt
import multiprocessing as mp


class Drawer:
    def __init__(self, df, img_dir="img"):
        self.df = df
        self.img_dir = img_dir
        os.makedirs(self.img_dir, exist_ok=True)

    def worker(self, sensor, df, img_dir, completed_list):
        try:
            broken_rows = df[df["machine_status"] == "BROKEN"]
            recovery_rows = df[df["machine_status"] == "RECOVERING"]
            anomaly_rows = df[df["LocalOutlierFactor"] == -1]

            plt.figure(figsize=(25, 3))
            plt.plot(df[sensor], color="grey")
            plt.plot(
                recovery_rows[sensor],
                linestyle="none",
                marker="o",
                color="yellow",
                markersize=5,
                label="recovering",
                alpha=0.5,
            )
            plt.plot(
                broken_rows[sensor],
                linestyle="none",
                marker="X",
                color="red",
                markersize=20,
                label="broken",
            )
            plt.plot(
                anomaly_rows[sensor],
                linestyle="none",
                marker="X",
                color="blue",
                markersize=4,
                label="anomaly predicted",
                alpha=0.1,
            )
            plt.title(sensor)
            plt.legend()

            filename = f"{sensor}.png"
            path = os.path.join(img_dir, filename)
            plt.savefig(path)
            plt.close()

            completed_list.append(sensor)
        except Exception as e:
            print(f"Error plotting {sensor}: {e}")

    def run(self):
        manager = mp.Manager()
        completed_plots = manager.list()
        processes = []

        for col in self.df.columns:
            if "sensor" in col:
                p = mp.Process(
                    target=self.worker,
                    args=(col, self.df, self.img_dir, completed_plots),
                )
                p.start()
                processes.append(p)

        for p in processes:
            p.join()

        print(f"Completed plots for sensors: {list(completed_plots)}")
