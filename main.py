import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
import time
# Cargar variables de entorno
load_dotenv()

intents = discord.Intents.default()
# No necesitamos message_content para comandos slash
bot = commands.Bot(command_prefix="!", intents=intents)

# Lista privada de usuarios que usan el bot
usuarios_registrados = set()

# Función para registrar usuario
def registrar_usuario(user_id: int):
    usuarios_registrados.add(user_id)

# Diccionario temporal para guardar datos del usuario
bot.temp_data = {}


# ------------------------- MODAL 1 -------------------------
class DPSModal1(discord.ui.Modal, title="Datos del Arma"):
    arma = discord.ui.TextInput(label="Nombre del arma", required=True)
    dano_cuerpo = discord.ui.TextInput(label="Daño al cuerpo", required=True)
    dano_cabeza = discord.ui.TextInput(label="Daño a la cabeza", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        # Validar y guardar datos iniciales
        try:
            dano_cuerpo = float(self.dano_cuerpo.value)
            dano_cabeza = float(self.dano_cabeza.value)
            
            if dano_cuerpo <= 0 or dano_cabeza <= 0:
                await interaction.response.send_message(
                    "❌ Los valores de daño deben ser mayores que 0.",
                    ephemeral=True)
                return
                
            interaction.client.temp_data[interaction.user.id] = {
                "arma": self.arma.value,
                "cuerpo": dano_cuerpo,
                "cabeza": dano_cabeza
            }
        except ValueError:
            await interaction.response.send_message(
                "❌ Por favor, ingresa valores numéricos válidos para el daño.",
                ephemeral=True)
            return

        # Mostrar botón efímero al usuario
        view = NextStepView()
        await interaction.response.send_message(
            "✅ Datos iniciales guardados.\nHaz clic en **Siguiente** para continuar.",
            view=view,
            ephemeral=True)


# ------------------------- BOTÓN PARA PASAR AL MODAL 2 -------------------------
class NextStepView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="➡️ Siguiente", style=discord.ButtonStyle.primary)
    async def next_step(self, interaction: discord.Interaction,
                        button: discord.ui.Button):
        await interaction.response.send_modal(DPSModal2())


# ------------------------- MODAL 2 -------------------------
class DPSModal2(discord.ui.Modal, title="Datos adicionales"):
    velocidad = discord.ui.TextInput(label="Daño por segundo", required=True)
    mutado = discord.ui.TextInput(label="Daño vs Mutados (%)", required=True)
    cargador = discord.ui.TextInput(label="Cargador", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        # Recuperar datos previos
        data = interaction.client.temp_data.get(interaction.user.id)
        if not data:
            await interaction.response.send_message(
                "❌ No encontré datos previos. Usa el comando de nuevo.",
                ephemeral=True)
            return

        # Guardar datos nuevos con validación
        try:
            velocidad = float(self.velocidad.value)
            mutado = int(self.mutado.value)
            cargador = int(self.cargador.value)
            
            if velocidad <= 0:
                await interaction.response.send_message(
                    "❌ El daño por segundo debe ser mayor que 0.",
                    ephemeral=True)
                return
            
            if cargador <= 0:
                await interaction.response.send_message(
                    "❌ El cargador debe ser mayor que 0.",
                    ephemeral=True)
                return
                
        except ValueError:
            await interaction.response.send_message(
                "❌ Por favor, ingresa valores numéricos válidos.",
                ephemeral=True)
            return

        arma = data["arma"]
        dano_cuerpo = data["cuerpo"]
        dano_cabeza = data["cabeza"]

        # Fórmulas
        mutadoT = (mutado + 100) / 100
        dps_cuerpo = dano_cuerpo * velocidad * mutadoT
        dps_cabeza = dano_cabeza * velocidad * mutadoT
        dano_por_cargador_cabeza = (cargador / velocidad) * dps_cabeza
        dano_por_cargador_cuerpo = (cargador / velocidad) * dps_cuerpo

        # Crear embed final
        embed = discord.Embed(title=f"📊 Estadísticas de {arma}",
                              color=discord.Color.green())
        embed.add_field(
            name="",
            value="/////////////////////////////////////////////////////////",
            inline=False)
        embed.add_field(
            name="🧪 Daño Por Segundo ",
            value="──────────────────────────────────────────────────────────",
            inline=False)
        embed.add_field(name="🩸 DPS Cuerpo",
                        value=f"{dps_cuerpo:.2f}",
                        inline=True)
        embed.add_field(name="🎯 DPS Cabeza",
                        value=f"{dps_cabeza:.2f}",
                        inline=True)
        embed.add_field(
            name="🔋 DAÑO POR CARGADOR",
            value="──────────────────────────────────────────────────────────",
            inline=False)
        embed.add_field(name="🔃 Daño por Cargador Cabeza",
                        value=f"{dano_por_cargador_cabeza:.2f}",
                        inline=False)
        embed.add_field(name="💣 Daño por Cargador Cuerpo",
                        value=f"{dano_por_cargador_cuerpo:.2f}",
                        inline=False)

        # Borrar datos temporales
        interaction.client.temp_data.pop(interaction.user.id, None)

        # Enviar embed para todos
        await interaction.response.send_message(embed=embed)


# ------------------------- COMANDO SLASH -------------------------
@bot.tree.command(name="dps-arma", description="DPS de tu arma")
async def arma(interaction: discord.Interaction):
    registrar_usuario(interaction.user.id)  # <-- registra usuario
    await interaction.response.send_modal(DPSModal1())


# ------------------------- EVENTO READY -------------------------
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"✅ Bot conectado como {bot.user}")
    print(f"🔁 Comandos slash sincronizados: {len(synced)}")
    print(f"{bot.user} está conectado y listo 🚀")
    
@bot.tree.command(name="usuarios", description="Ver usuarios registrados (SOLO ADMIN)")
async def ver_usuarios(interaction: discord.Interaction):
    TU_ID = 394266030542684170  # <-- pon aquí tu ID de Discord

    if interaction.user.id == TU_ID:
        if usuarios_registrados:
            lista = "\n".join([f"<@{uid}>" for uid in usuarios_registrados])
            await interaction.user.send(f"📋 Usuarios que usaron el bot:\n{lista}")
            await interaction.response.send_message("✅ Te envié la lista por DM", ephemeral=True)
        else:
            await interaction.response.send_message("📋 Nadie ha usado aún tus comandos.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ No tienes permiso para este comando.", ephemeral=True)


# ----- Modal Purple Zone -----
class PurpleZoneModal(discord.ui.Modal, title="Purple Zone"):

    numero = discord.ui.TextInput(label="Número (Escriba Reconpensa de la PZ)",
                                  placeholder="Ejemplo: 15.256",
                                  style=discord.TextStyle.short,
                                  required=True,
                                  max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            valor = float(self.numero.value)
            valor_formateado = f"{valor:.3f} K"

            # Enviamos un mensaje con dropdown para elegir la opción
            view = PurpleZoneView(valor_formateado)
            await interaction.response.send_message(
                content=
                f"✅ Número recibido: **{valor_formateado}**\nAhora elige una opción:",
                view=view,
                ephemeral=True)

        except ValueError:
            await interaction.response.send_message(
                "❌ Debes ingresar un número válido con decimales.",
                ephemeral=True)


# ----- Dropdown fuera del modal -----
class PurpleZoneSelect(discord.ui.Select):

    def __init__(self, numero):
        options = [
            discord.SelectOption(label="PZ Arañas"),
            discord.SelectOption(label="PZ Aco Scy - Reapers"),
            discord.SelectOption(label="PZ Aco Tent - Tendrils"),
            discord.SelectOption(label="PZ Aco Spit - Hystericks"),
            discord.SelectOption(label="PZ 15 Bosses"),
            discord.SelectOption(label="PZ 700 Zombies"),
        ]
        super().__init__(placeholder="Elige una opción",
                         options=options,
                         min_values=1,
                         max_values=1)
        self.numero = numero

    async def callback(self, interaction: discord.Interaction):
        opcion = self.values[0]

        # Crear el embed
        embed = discord.Embed(title="📊 Purple Zone",
                              color=discord.Color.purple())
        embed.add_field(name="⚔️ Nombre de PZ", value=opcion, inline=False)
        embed.add_field(name="🔢 Recompensa", value=self.numero, inline=False)

        # ----- Asignar imagen distinta según la opción -----
        imagenes = {
            "PZ Arañas":
            "https://cdn.discordapp.com/attachments/1205222551832363091/1364428286754689104/image.png?ex=6809a25d&is=680850dd&hm=bec016a8fef163ed807a3024c897e1dfab1b13e472e76833a9826e02b076c61d&",
            "PZ Aco Scy - Reapers":
            "https://media.discordapp.net/attachments/1205222551832363091/1234193424538927124/image.png?ex=6635c672&is=663474f2&hm=5d509a56f9a4be216c944d119680f0dc2dfcdcc49ed8a417ba5c3efa1ac7fd75&=&format=webp&quality=lossless",
            "PZ Aco Tent - Tendrils":
            "https://media.discordapp.net/attachments/1205222551832363091/1234641390814756974/image.png?ex=66361626&is=6634c4a6&hm=83c99ea5f67f9336cc1f041f9caf218a4933c3cbe1b619fd99f4d0ef39087130&=&format=webp&quality=lossless",
            "PZ Aco Spit - Hystericks":
            "https://media.discordapp.net/attachments/1205222551832363091/1233307594047623218/image.png?ex=6635d934&is=663487b4&hm=2782cd711e6cabe86f1c91c24c2a8fbebc9c86f3de04aa05dc6f66e61242e00d&=&format=webp&quality=lossless",
            "PZ 15 Bosses":
            "https://media.discordapp.net/attachments/1205222551832363091/1233325713059352606/image.png?ex=662caf94&is=662b5e14&hm=10aa53b0f0d6b3150cd7c19fab2f915ffaf47692aa1047aef0d14daa72f9331c&=&format=webp&quality=lossless",
            "PZ 700 Zombies":
            "https://media.discordapp.net/attachments/1205222551832363091/1235678706563809351/image.png?ex=66353ef9&is=6633ed79&hm=e09e011e0f3c505cdaab9d327e16faf928c54e569de073302e89078daebddfd8&=&format=webp&quality=lossless"
        }

        if opcion in imagenes:
            embed.set_image(url=imagenes[opcion])

        mensaje_mencion = "@here"  # ID del rol
        await interaction.response.send_message(content=mensaje_mencion,
                                                embed=embed)


# ----- View que contiene el dropdown -----
class PurpleZoneView(discord.ui.View):

    def __init__(self, numero):
        super().__init__()
        self.add_item(PurpleZoneSelect(numero))


# ----- Slash Command -----
@bot.tree.command(name="pz", description="Abre el formulario Purple Zone")
async def pz_form(interaction: discord.Interaction):
    registrar_usuario(interaction.user.id)  # <-- registra usuario
    await interaction.response.send_modal(PurpleZoneModal())


# ------------------------- RUN BOT -------------------------




if __name__ == "__main__":
    # Mantener el bot vivo
    keep_alive()

    token = os.getenv("TOKEN")
    if not token:
        print("❌ Error: TOKEN no encontrado en las variables de entorno")
        print(
            "💡 Por favor, añade tu token de Discord en un archivo .env o como variable de entorno"
        )
        exit(1)
 #   if __name__ == "__main__":
  #      keep_alive()  # ✅ SOLO AQUÍ SE LLAMA
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Error: Token de Discord inválido")
    except Exception as e:
        print(f"❌ Error al ejecutar el bot: {e}")