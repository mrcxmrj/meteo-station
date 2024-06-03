async function refreshTable(tableType) {
  try {
    const response = await fetch(`/table/${tableType}`, {
      headers: {
        "x-no-refresh": true,
      },
    });
    const html = await response.text();
    document.getElementById(`${tableType}-table`).innerHTML = html;
  } catch (error) {
    console.error(error);
  }
}

async function refreshTables(tables) {
  const refreshPromises = tables.map((table) => refreshTable(table));
  await Promise.all(refreshPromises);
}

setInterval(() => refreshTables(["temperature", "humidity", "pressure"]), 1000);

async function testJson() {
  try {
    const response = await fetch("/data/temperature", {});
    const json = await response.text();
    console.log(json);
  } catch (error) {
    console.error(error);
  }
}
setTimeout(testJson, 3000);
// TODO:
// - add refreshing for current readings (not whole table)
// - stop refreshing when page != tables
// const periodicTableRefresh = setInterval(() => refreshTables(["temperature", "humidity", "pressure"]), 1000);
// if #table-container not in DOM then clearInterval(periodicTableRefresh)
