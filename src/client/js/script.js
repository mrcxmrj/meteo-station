// alert("I work");
async function getResponse() {
  const response = await fetch("/", {
    headers: {
      "x-refresh": true,
    },
  });
}

getResponse();
