async function refreshTable(tableId) {
  try {
    const response = await fetch("/tables", {
      headers: {
        "x-no-refresh": true,
      },
    });
    const html = await response.text();
    document.getElementById(tableId).innerHTML = html;
  } catch (error) {
    console.error(error);
  }
}

setInterval(() => refreshTable("temperature-table"), 1000);
