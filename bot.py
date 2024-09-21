import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'ล็อกอินเป็น {bot.user}')

@bot.command()
async def verify(ctx):
    # ส่ง DM ไปยังผู้ใช้
    await ctx.author.send('กรุณาใส่เลขบัตรประชาชนของคุณสำหรับการยืนยัน:')
    
    def check(msg):
        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

    try:
        # รอรับข้อความจาก DM
        msg = await bot.wait_for('message', check=check, timeout=60)  # รอ 60 วินาที

        # ตรวจสอบอายุจากเลขบัตรประชาชน
        id_number = msg.content
        year_of_birth = int(id_number[0:2])  # สมมุติว่าเลข 2 หลักแรกคือปีเกิด
        current_year = 2024  # อัปเดตปีปัจจุบันตามต้องการ
        age = current_year - (1900 + year_of_birth) if year_of_birth < 24 else current_year - (2000 + year_of_birth)

        if age < 15:
            await ctx.author.send('การยืนยันล้มเหลว: คุณต้องมีอายุมากกว่า 15 ปี.')
        else:
            role = discord.utils.get(ctx.guild.roles, name='Verified')  # แทนที่ 'Verified' ด้วยชื่อยศที่คุณต้องการ
            await ctx.author.add_roles(role)
            await ctx.author.send('การยืนยันสำเร็จ! คุณได้รับยศ Verified แล้ว.')

    except asyncio.TimeoutError:
        await ctx.author.send('คุณใช้เวลานานเกินไปในการตอบกลับ! การยืนยันถูกยกเลิก.')

TOKEN = 'MTI4NzA1ODMxODQzNDYzMTY5MA.Gntv6U.TMUAp6rstFRtXvG1Ksdp_wNxPsB2MFLnkHvW20'  # แทนที่ด้วย Token ของบอทของคุณ
bot.run(TOKEN)
