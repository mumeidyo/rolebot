import discord
from discord.ext import commands
from config import Config
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

# Botのインスタンス作成
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Botが起動したときに実行される"""
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')

@bot.command(name='roles')
async def show_roles(ctx):
    """利用可能なロールとその絵文字を表示する"""
    # Botの権限をチェック
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send("エラー: Botにロールを管理する権限がありません。サーバー設定でロールの管理権限を付与してください。")
        logger.error("Bot lacks manage_roles permission")
        return

    embed = discord.Embed(title="Available Roles", 
                         description="リアクションを追加して役職を取得できます！\n取り消すには再度リアクションをクリックしてください。",
                         color=discord.Color.blue())

    # 絵文字のリスト
    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    # サーバー内の利用可能なロールを取得
    available_roles = [
        role for role in ctx.guild.roles 
        if not role.name in Config.EXCLUDED_ROLES 
    ]

    # ロールと絵文字のマッピングを作成
    role_emoji_map = {}
    for i, role in enumerate(available_roles[:10]):  # 最大10個のロールまで
        role_emoji_map[emojis[i]] = role
        embed.add_field(name=role.name, value=f"{emojis[i]}", inline=True)
        logger.debug(f"Mapped role {role.name} to emoji {emojis[i]}")

    message = await ctx.send(embed=embed)

    # メッセージにリアクションを追加
    for emoji in role_emoji_map.keys():
        await message.add_reaction(emoji)

    # ロールと絵文字のマッピングをメッセージに保存
    bot.role_mappings[message.id] = role_emoji_map

@bot.event
async def on_raw_reaction_add(payload):
    """ユーザーがリアクションを追加したときの処理"""
    if payload.member.bot:
        return

    # メッセージのロールマッピングを取得
    role_mapping = bot.role_mappings.get(payload.message_id)
    if not role_mapping:
        logger.debug(f"No role mapping found for message {payload.message_id}")
        return

    emoji = str(payload.emoji)
    if emoji not in role_mapping:
        logger.debug(f"Emoji {emoji} not found in role mapping")
        return

    role = role_mapping[emoji]
    try:
        guild = bot.get_guild(payload.guild_id)
        if not guild.me.guild_permissions.manage_roles:
            logger.error("Bot lacks manage_roles permission")
            return

        await payload.member.add_roles(role)
        logger.info(f"Added role {role.name} to {payload.member.name}")
    except discord.Forbidden:
        logger.error(f"Failed to add role {role.name} to {payload.member.name}: Missing permissions")
    except Exception as e:
        logger.error(f"Failed to add role {role.name} to {payload.member.name}: {str(e)}")

@bot.event
async def on_raw_reaction_remove(payload):
    """ユーザーがリアクションを削除したときの処理"""
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member is None or member.bot:
        return

    # メッセージのロールマッピングを取得
    role_mapping = bot.role_mappings.get(payload.message_id)
    if not role_mapping:
        logger.debug(f"No role mapping found for message {payload.message_id}")
        return

    emoji = str(payload.emoji)
    if emoji not in role_mapping:
        logger.debug(f"Emoji {emoji} not found in role mapping")
        return

    role = role_mapping[emoji]
    try:
        if not guild.me.guild_permissions.manage_roles:
            logger.error("Bot lacks manage_roles permission")
            return

        if role in member.roles:
            await member.remove_roles(role)
            logger.info(f"Removed role {role.name} from {member.name}")
    except discord.Forbidden:
        logger.error(f"Failed to remove role {role.name} from {member.name}: Missing permissions")
    except Exception as e:
        logger.error(f"Failed to remove role {role.name} from {member.name}: {str(e)}")

def run_bot():
    """Botを実行する"""
    # ロールと絵文字のマッピングを保存する辞書を初期化
    bot.role_mappings = {}
    bot.run(Config.DISCORD_BOT_TOKEN)