from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OVERVIEW_DIRECTORY = Path("data/processed/overview")
FIGURE_DIRECTORY = Path("reports/figures")


def create_daily_volume_chart():
    daily = pd.read_csv(OVERVIEW_DIRECTORY / "daily_request_volume.csv")
    daily["created_date"] = pd.to_datetime(daily["created_date"])
    daily = daily.sort_values("created_date")

    peak = daily.loc[daily["requests"].idxmax()]
    figure, axis = plt.subplots(figsize=(11, 5.5))
    axis.plot(daily["created_date"], daily["requests"], color="#1f5a94", linewidth=2)
    axis.scatter(peak["created_date"], peak["requests"], color="#c2410c", zorder=3)
    axis.annotate(
        f"Peak: {peak['requests']:,}\n{peak['created_date'].date()}",
        xy=(peak["created_date"], peak["requests"]),
        xytext=(12, -38),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "color": "#c2410c"},
    )
    axis.set_title("NYC 311 Service Requests by Day | Q1 2025")
    axis.set_xlabel("Request creation date")
    axis.set_ylabel("Requests")
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(FIGURE_DIRECTORY / "daily_request_volume_q1_2025.png", dpi=200)
    plt.close(figure)


def create_volume_duration_chart():
    volume = pd.read_csv(OVERVIEW_DIRECTORY / "complaint_type_volume.csv")
    duration = pd.read_csv(OVERVIEW_DIRECTORY / "complaint_type_resolution.csv")
    chart_data = volume.merge(duration, on="complaint_type", how="inner")
    chart_data = chart_data.head(12).sort_values("median_hours")

    figure, axis = plt.subplots(figsize=(11, 6.5))
    axis.scatter(
        chart_data["median_hours"],
        chart_data["requests"],
        s=chart_data["requests"] / 35,
        color="#1f5a94",
        alpha=0.75,
        edgecolors="white",
        linewidths=0.8,
    )
    label_offsets = {
        "Illegal Parking": (6, 4),
        "HEAT/HOT WATER": (6, 4),
        "Noise - Residential": (6, 4),
        "Blocked Driveway": (6, 4),
        "UNSANITARY CONDITION": (6, 4),
        "PLUMBING": (6, 9),
        "PAINT/PLASTER": (6, -14),
        "Street Condition": (6, 4),
    }
    for _, row in chart_data.iterrows():
        if row["complaint_type"] not in label_offsets:
            continue
        axis.annotate(
            row["complaint_type"],
            (row["median_hours"], row["requests"]),
            xytext=label_offsets[row["complaint_type"]],
            textcoords="offset points",
            fontsize=8,
        )

    axis.set_xscale("log")
    axis.set_title("High-Volume 311 Complaint Types: Volume vs. Typical Closure Time")
    axis.set_xlabel("Median closure time (hours, log scale)")
    axis.set_ylabel("Requests created in Q1 2025")
    axis.grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(
        FIGURE_DIRECTORY / "complaint_volume_vs_resolution_q1_2025.png",
        dpi=200,
    )
    plt.close(figure)


def create_borough_volume_chart():
    borough = pd.read_csv(OVERVIEW_DIRECTORY / "borough_request_volume.csv")
    borough = borough.sort_values("requests")
    colors = ["#9ca3af" if name == "Unspecified" else "#1f5a94" for name in borough["borough"]]

    figure, axis = plt.subplots(figsize=(9, 5.5))
    bars = axis.barh(borough["borough"], borough["requests"], color=colors)
    for bar, share in zip(bars, borough["share_pct"]):
        axis.text(
            bar.get_width() + 3_000,
            bar.get_y() + bar.get_height() / 2,
            f"{share:.2f}%",
            va="center",
        )

    axis.set_title("NYC 311 Service Requests by Borough | Q1 2025")
    axis.set_xlabel("Requests created in Q1 2025")
    axis.set_ylabel("Borough")
    axis.grid(axis="x", alpha=0.25)
    axis.set_xlim(0, borough["requests"].max() * 1.18)
    figure.tight_layout()
    figure.savefig(FIGURE_DIRECTORY / "borough_request_volume_q1_2025.png", dpi=200)
    plt.close(figure)


def create_borough_complaint_mix_chart():
    top_complaints = pd.read_csv(
        OVERVIEW_DIRECTORY / "top_complaints_by_borough.csv"
    )
    top_complaints = top_complaints[top_complaints["borough"] != "Unspecified"]
    borough_order = ["BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND"]
    matrix = top_complaints.pivot(
        index="borough",
        columns="complaint_type",
        values="borough_share_pct",
    ).reindex(borough_order).fillna(0)
    matrix = matrix[matrix.max().sort_values(ascending=False).index]

    figure, axis = plt.subplots(figsize=(11, 5.5))
    image = axis.imshow(matrix.values, cmap="Blues", aspect="auto")
    axis.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=25, ha="right")
    axis.set_yticks(range(len(matrix.index)), matrix.index)
    for row_index, borough in enumerate(matrix.index):
        for column_index, complaint_type in enumerate(matrix.columns):
            value = matrix.loc[borough, complaint_type]
            if value:
                axis.text(
                    column_index,
                    row_index,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                    color="white" if value >= 15 else "black",
                )

    colorbar = figure.colorbar(image, ax=axis)
    colorbar.set_label("Share of requests within borough (%)")
    axis.set_title("Top Three Complaint Types Within Each Borough | Q1 2025")
    figure.tight_layout()
    figure.savefig(FIGURE_DIRECTORY / "borough_complaint_mix_q1_2025.png", dpi=200)
    plt.close(figure)


def main():
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    create_daily_volume_chart()
    create_volume_duration_chart()
    create_borough_volume_chart()
    create_borough_complaint_mix_chart()
    print("Saved charts to:", FIGURE_DIRECTORY)


if __name__ == "__main__":
    main()
