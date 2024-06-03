const chartContainer = document.getElementById("chart");
const colors = { blue: "#3674d9", red: "#eb4034", green: "#32a852" };
const valueFormatter = (value) => `${Math.round(value * 100) / 100}${unit}`;

function processData(data) {
  const splitData = data.map((el) =>
    el.values.map((value) => ({
      time: parseInt(el.time),
      value: parseFloat(value),
    })),
  );

  let result = [];
  for (const i in splitData[0]) {
    result.push(splitData.map((records) => records[i]));
  }
  return result;
}

function createSeries(chart, datas) {
  const colorArray = Object.values(colors);
  return datas.map((data, i) => {
    console.log(data);
    const temperatureSeries = chart.addLineSeries({ color: colorArray[i] });
    temperatureSeries.setData(data);
    return temperatureSeries;
  });
}

const chart = LightweightCharts.createChart(chartContainer, {
  height: 500,
  autoSize: true,
  layout: {
    textColor: "white",
    background: { type: "solid", color: "transparent" },
  },
  localization: { priceFormatter: valueFormatter },
});

const processedData = processData(initialData);
const series = createSeries(chart, processedData);

async function getNewData() {
  try {
    const response = await fetch(`/data/${category}`);
    const json = await response.json();
    const processedData = processData(json);
    processedData?.forEach((data, i) => {
      series[i].update(...data);
    });
  } catch (error) {
    console.error(error);
  }
}
setInterval(getNewData, 3000);
