const pool = require("../utils/db");

module.exports = {
  name: "join",
  description: "Únete a un grupo existente",
  async execute(message, args) {
    const numero = parseInt(args[0]);
    if (!numero) return message.reply("❌ Uso: `!join [número]`");

    try {
      // Verificar si existe
      const grupo = await pool.query("SELECT * FROM grupos WHERE numero_grupo = $1", [numero]);
      if (grupo.rowCount === 0) return message.reply(`❌ El grupo **#${numero}** no existe.`);

      // Verificar si ya está lleno
      const miembros = await pool.query("SELECT * FROM grupo_miembros WHERE numero_grupo = $1", [numero]);
      if (miembros.rowCount >= 8) return message.reply(`❌ El grupo **#${numero}** ya está lleno (8/8).`);

      // Verificar si ya está en el grupo
      const yaMiembro = miembros.rows.find(m => m.user_id === message.author.id);
      if (yaMiembro) return message.reply(`❌ Ya eres miembro del grupo **#${numero}**.`);

      // Insertar
      await pool.query(
        "INSERT INTO grupo_miembros (numero_grupo, user_id, username) VALUES ($1, $2, $3)",
        [numero, message.author.id, message.author.tag]
      );

      message.channel.send(`✅ ${message.author.tag} se unió al grupo **#${numero}**.`);
    } catch (err) {
      console.error(err);
      message.reply("❌ Error al unirse al grupo.");
    }
  },
};
