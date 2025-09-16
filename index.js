const { Client, GatewayIntentBits, Collection } = require("discord.js");
const fs = require("fs");
const path = require("path");
require("dotenv").config();
client.login(process.env.TOKEN);
const keepAlive = require("./keep_alive");

// Inicializar cliente de Discord
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.commands = new Collection();

// Cargar comandos dinámicamente
const commandFiles = fs.readdirSync(path.join(__dirname, "src/commands")).filter(file => file.endsWith(".js"));

for (const file of commandFiles) {
  const command = require(`./src/commands/${file}`);
  client.commands.set(command.name, command);
}

// Listener de mensajes
client.on("messageCreate", async (message) => {
  if (!message.content.startsWith("!") || message.author.bot) return;

  const args = message.content.slice(1).split(/ +/);
  const commandName = args.shift().toLowerCase();

  if (client.commands.has(commandName)) {
    try {
      await client.commands.get(commandName).execute(message, args, client);
    } catch (error) {
      console.error(error);
      message.reply("❌ Error ejecutando el comando.");
    }
  }
});

client.once("ready", () => {
  console.log(`✅ Bot conectado como ${client.user.tag}`);
});

// Mantener web activa
keepAlive();

// Iniciar el bot
client.login(process.env.TOKEN);
