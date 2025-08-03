
REWARD_CHANNEL_ID = 1390651899853930627  # Channel for reward request

# 🎯 View for selecting reward plan
class RewardPlanView(View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=60)
        self.user = user

        select = Select(
            placeholder="🎯 Select your VPS reward plan",
            options=[
                discord.SelectOption(label="🎁 8 Invites = 16GB RAM", value="inv_8_16"),
                discord.SelectOption(label="🏆 15 Invites = 32GB RAM", value="inv_15_32"),
                discord.SelectOption(label="🚀 1x Boost = 16GB RAM", value="boost_1_16"),
                discord.SelectOption(label="🚀🚀 2x Boost = 32GB RAM", value="boost_2_32"),
            ]
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("❌ Only you can select your plan.", ephemeral=True)
            return

        value = interaction.data["values"][0]
        if value.startswith("inv"):
            _, invites, ram = value.split("_")
            plan_text = f"{invites} Invites = {ram}GB RAM"
        elif value.startswith("boost"):
            _, boost_count, ram = value.split("_")
            plan_text = f"{boost_count}x Boost = {ram}GB RAM"
        else:
            plan_text = "Unknown Plan"

        embed = discord.Embed(
            title="📥 VPS Reward Request",
            description="A new VPS reward request has been submitted!",
            color=0x2400ff
        )
        embed.add_field(name="👤 User", value=f"{self.user.mention} (`{self.user.id}`)", inline=False)
        embed.add_field(name="🏆 Plan", value=plan_text, inline=True)
        embed.add_field(name="🐧 OS", value="Ubuntu 22.04", inline=True)
        embed.set_footer(text="Click a button below to accept or reject.")

        view = AcceptRejectView(self.user, plan_text)
        channel = bot.get_channel(REWARD_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed, view=view)
            await interaction.response.send_message("✅ Your request has been sent for approval.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Reward request channel not found.", ephemeral=True)


# ✅ Accept / Reject Button View
class AcceptRejectView(View):
    def __init__(self, requester: discord.User, plan: str):
        super().__init__(timeout=120)
        self.requester = requester
        self.plan = plan

    @discord.ui.button(label="✅ Accept", style=discord.ButtonStyle.success, emoji="✅")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="✅ VPS Request Accepted",
                description=f"Your VPS request for `{self.plan}` has been accepted!",
                color=0x00ff00
            )
            embed.add_field(name="🕐 Status", value="Your VPS will be deployed soon by admin.", inline=False)
            await self.requester.send(embed=embed)
            await interaction.response.send_message(f"✅ Accepted VPS request for {self.requester.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Could not send DM. The user may have DMs closed.", ephemeral=True)

    @discord.ui.button(label="❌ Reject", style=discord.ButtonStyle.danger, emoji="❌")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="❌ VPS Request Rejected",
                description=f"Your VPS request for `{self.plan}` has been rejected.",
                color=0xff0000
            )
            await self.requester.send(embed=embed)
            await interaction.response.send_message(f"❌ Rejected VPS request for {self.requester.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Could not send DM. The user may have DMs closed.", ephemeral=True)


# 🔧 Slash command: /create
@bot.tree.command(name="create", description="🎁 Request a VPS reward (based on invites or boosts)")
async def create(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎁 VPS Reward Center",
        description="Choose your reward plan below to request a VPS.",
        color=0x2400ff
    )
    await interaction.response.send_message(embed=embed, view=RewardPlanView(interaction.user), ephemeral=True)


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