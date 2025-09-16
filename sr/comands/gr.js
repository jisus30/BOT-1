const pool = require("../utils/db");

module.exports = {
  name: "gr",
  description: "Crea un grupo con un número",
  async execute(message, args) {
    const numero = parseInt(args[0]);
    if (!numero) return message.reply("❌ Uso: `!gr [número]`");

    try {
      await pool.query("INSERT INTO grupos (numero_grupo) VALUES ($1)", [numero]);
      message.channel.send(`✅ Grupo **#${numero}** creado con éxito.\nUsa \`!join ${numero}\` para unirte.`);
    } catch (err) {
      message.channel.send("❌ Ese grupo ya existe o hubo un error.");
      console.error(err);
    }
  },
};
