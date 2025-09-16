const pool = require("../utils/db");

module.exports = {
  name: "gl",
  description: "Muestra la lista de miembros de un grupo",
  async execute(message, args) {
    const numero = parseInt(args[0]);
    if (!numero) return message.reply("❌ Uso: `!gl [número]`");

    try {
      const miembros = await pool.query(
        "SELECT username FROM grupo_miembros WHERE numero_grupo = $1 ORDER BY joined_at ASC",
        [numero]
      );

      if (miembros.rowCount === 0) return message.reply(`❌ El grupo **#${numero}** está vacío o no existe.`);

      const lista = miembros.rows.map((m, i) => `**${i + 1}.** ${m.username}`).join("\n");

      message.channel.send(`📋 **Grupo #${numero}**\n${lista}\n\nMiembros: **${miembros.rowCount}/8**`);
    } catch (err) {
      console.error(err);
      message.reply("❌ Error mostrando la lista del grupo.");
    }
  },
};
