module.exports = {
  name: "dps",
  description: "Calcula el DPS de un arma",
  async execute(message, args) {
    if (args.length < 5) {
      return message.reply("❌ Uso: `!dps [arma] [daño cuerpo] [daño cabeza] [velocidad] [cargador] [mutado%]`");
    }

    const [arma, danoCuerpo, danoCabeza, velocidad, cargador, mutado] = args;
    const cuerpo = parseFloat(danoCuerpo);
    const cabeza = parseFloat(danoCabeza);
    const atk = parseFloat(velocidad);
    const mag = parseInt(cargador);
    const bonus = (parseInt(mutado) + 100) / 100;

    if (isNaN(cuerpo) || isNaN(cabeza) || isNaN(atk) || isNaN(mag)) {
      return message.reply("❌ Todos los valores de daño, velocidad y cargador deben ser números.");
    }

    const dpsCuerpo = cuerpo * atk * bonus;
    const dpsCabeza = cabeza * atk * bonus;
    const danoMagCuerpo = (mag / atk) * dpsCuerpo;
    const danoMagCabeza = (mag / atk) * dpsCabeza;

    message.channel.send(
      `📊 **${arma}**\n\n🩸 DPS Cuerpo: **${dpsCuerpo.toFixed(2)}**\n🎯 DPS Cabeza: **${dpsCabeza.toFixed(2)}**\n\n🔋 Daño x Cargador Cuerpo: **${danoMagCuerpo.toFixed(2)}**\n💣 Daño x Cargador Cabeza: **${danoMagCabeza.toFixed(2)}**`
    );
  },
};
