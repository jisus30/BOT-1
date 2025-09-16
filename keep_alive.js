const express = require("express");

function keepAlive() {
  const app = express();
  app.get("/", (req, res) => res.send("Bot activo 🚀"));
  app.listen(process.env.PORT || 3000, () => {
    console.log("🌐 Servidor keep-alive activo");
  });
}

module.exports = keepAlive;
