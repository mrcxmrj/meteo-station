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
