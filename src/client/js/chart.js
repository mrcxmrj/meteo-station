const chartContainer = document.getElementById("chart");
const unit = "hPa";
const valueFormatter = (value) => `${Math.round(value * 100) / 100}${unit}`;

const chart = LightweightCharts.createChart(chartContainer, {
  height: 500,
  autoSize: true,
  layout: {
    textColor: "white",
    background: { type: "solid", color: "transparent" },
  },
  localization: { priceFormatter: valueFormatter },
});

const createMockSeries = (length) =>
  Array.from({ length: length }, (_, i) => ({
    time: `2019-04-${(i + 1) % 30}`,
    value: Math.random(),
  }));

const temperatureSeries = chart.addLineSeries({ color: "#eb4034" });
temperatureSeries.setData(createMockSeries(20));

const humiditySeries = chart.addLineSeries();
humiditySeries.setData(createMockSeries(20));

setInterval(
  () =>
    temperatureSeries.update({
      time: new Date().toDateString(),
      value: Math.random() * 100,
    }),
  5000,
);
