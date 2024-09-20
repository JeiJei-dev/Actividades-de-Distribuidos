(async function main() {
  const connections = [];
  for (let i = 0; i < 1000; i++) {
    connections.push(
      fetch("http://localhost:3000/api/new-connection", {
        method: "POST",
      })
    );
  }
  Promise.all(connections);
})();
