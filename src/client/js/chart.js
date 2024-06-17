const colors = { blue: "#3674d9", red: "#eb4034", green: "#32a852" };
const valueFormatter = (value) => `${Math.round(value * 100) / 100}${unit}`;
const getCurrentCategory = () => {
  const url = new URL(window.location.href);
  const routes = url.pathname.split("/");
  return routes[routes.length - 1];
};
let refreshIntervalId;

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
    const newSeries = chart.addLineSeries({ color: colorArray[i] });
    newSeries.setData(data);
    return newSeries;
  });
}

async function getNewData(series) {
  try {
    const response = await fetch(`/data/${getCurrentCategory()}`);
    const json = await response.json();
    const processedData = processData(json);
    processedData?.forEach((data, i) => {
      series[i].update(...data);
    });
  } catch (error) {
    console.error(error);
  }
}

function evalConfig(html) {
  const configScript = html.match(/<script[^>]*>([\s\S]*?)<\/script>/gi)[1];
  const scriptLines = configScript.split("\n");
  const trimmedScriptLines = scriptLines.map((line) => line.trim());
  const scriptContentLines = trimmedScriptLines.slice(
    1,
    trimmedScriptLines.length - 1,
  );
  const config = scriptContentLines.join("");
  eval?.(config);
}

function initiateChart() {
  const chartContainer = document.getElementById("chart");
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

  refreshIntervalId = setInterval(() => getNewData(series), 3000);
}

function attachListenersToChartOptions() {
  const chartOptions = document.querySelectorAll(".chart-option");
  chartOptions.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      refreshChartContainer(e.target.getAttribute("data-id"));
    });
  });
}

async function refreshChartContainer(chartType) {
  const url = `/charts/${chartType}`;
  try {
    const response = await fetch(url, {
      headers: {
        "x-no-refresh": true,
      },
    });
    const html = await response.text();
    document.getElementById("chart-container").innerHTML = html;
    clearInterval(refreshIntervalId);
    evalConfig(html);
    attachListenersToChartOptions();
    initiateChart();
    window.history.pushState({}, "", url);
  } catch (error) {
    console.error(error);
  }
}

attachListenersToChartOptions();
initiateChart();
