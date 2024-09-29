function drawThermometer(ctx, temperature_celcius) {
  ctx.fillStyle = "#CCCCCC";
  ctx.strokeStyle = "#999999";
  ctx.lineWidth = 3;
  ctx.arc(100, 300, 40, 0, Math.PI * 2); // Bulb
  ctx.fill();
  ctx.fillRect(80, 0, 40, 300);

  ctx.beginPath();
  ctx.fillStyle = "#FF3D3D";
  ctx.arc(100, 300, 30, 0, Math.PI * 2);
  ctx.fill();

  y = 210 - temperature_celcius;
  h = 310 - y;

  ctx.fillRect(90, y, 20, h);
}

const unpackData = (data, i) => data[0].values[i];

const canvasIds = [
  "internal-thermometer",
  "dht-thermometer",
  "bmp-thermometer",
];
const canvases = canvasIds.map((id) => document.getElementById(id));
const ctxs = canvases.map((canvas) => canvas.getContext("2d"));
const drawThermometers = (data) =>
  ctxs.forEach((ctx, i) => drawThermometer(ctx, unpackData(data, i)));

async function getNewData() {
  try {
    const response = await fetch(`/data/temperature`);
    const json = await response.json();
    return json;
  } catch (error) {
    console.error(error);
  }
}

async function updateThermometer() {
  const newData = await getNewData();
  drawThermometers(newData);
}

drawThermometers(initialData);
setInterval(updateThermometer, 1000);
