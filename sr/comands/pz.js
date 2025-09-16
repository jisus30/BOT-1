module.exports = {
  name: "pz",
  description: "Muestra información de la Purple Zone",
  async execute(message, args) {
    if (args.length < 2) {
      return message.reply("❌ Uso: `!pz [nombre] [recompensa]`");
    }

    const nombre = args[0];
    const recompensa = args[1];

    message.channel.send(
      `🟣 **Purple Zone**\n⚔️ Nombre: **${nombre}**\n💎 Recompensa: **${recompensa}**`
    );
  },
};
