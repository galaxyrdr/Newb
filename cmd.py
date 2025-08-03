
# 📤 Slash command: /sendvps
@bot.tree.command(name="sendvps", description="📤 Send a VPS login to a user by ID")
@app_commands.describe(userid="User ID to send VPS info", ip="IP address", port="SSH port", password="Root password")
async def sendvps(interaction: discord.Interaction, userid: str, ip: str, port: str, password: str):
    try:
        user = await bot.fetch_user(int(userid))
        embed = discord.Embed(
            title="🔐 Your VPS Login Info",
            description="Here are your VPS login details. Use Termux or SSH app to connect.",
            color=0x00ffcc
        )
        embed.add_field(name="🌐 IP", value=f"`{ip}`", inline=True)
        embed.add_field(name="🔌 Port", value=f"`{port}`", inline=True)
        embed.add_field(name="🗝️ Password", value=f"`{password}`", inline=True)
        embed.add_field(
            name="📱 Termux SSH Command",
            value=f"```ssh root@{ip} -p {port}```",
            inline=False
        )
        embed.set_footer(text="GalaxyINC • VPS Bot")

        await user.send(embed=embed)
        await interaction.response.send_message(f"✅ VPS sent to <@{userid}>.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error sending VPS: {e}", ephemeral=True)
