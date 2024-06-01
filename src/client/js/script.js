// alert("I work");
async function getResponse() {
  const response = await fetch("/table", {
    headers: {
      "x-no-refresh": true,
    },
  });
  console.log(await response.text());
}

getResponse();
