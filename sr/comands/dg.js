const pool = require("../utils/db");

module.exports = {
  name: "dg",
  description: "Elimina un grupo",
  async execute(message, args) {
    const numero = parseInt(args[0]);
    if (!numero) return message.reply("❌ Uso: `!dg [número]`");

    try {
      const result = await pool.query("DELETE FROM grupos WHERE numero_grupo = $1 RETURNING *", [numero]);
      if (result.rowCount === 0) return message.reply(`❌ El grupo **#${numero}** no existe.`);

      message.channel.send(`🗑️ Grupo **#${numero}** eliminado con éxito.`);
    } catch (err) {
      console.error(err);
      message.reply("❌ Error al eliminar el grupo.");
    }
  },
};
