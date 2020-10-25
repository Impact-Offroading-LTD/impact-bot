import time
import discord
import psutil
import os
import requests
import json
import asyncio

from datetime import datetime
from discord.ext import commands
from utils import default
import json,urllib.request

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.command(pass_context=True)
    async def verify(self, ctx):
            user = ctx.message.author
            result = json.loads(urllib.request.urlopen("http://impactatv.com/checkid/" + str(ctx.author.id)).read())
            this_role = discord.utils.get(user.guild.roles, name="Members")
            banned = True
            if(result["found"]):
                embed = discord.Embed(title="Your account is already verified!",description="Thank you for verifying your account!",color=0x47f084)
                await user.add_roles(this_role)
                await ctx.send(embed=embed)
            else: 
                embed = discord.Embed(title="Your account is not verified!",description="To make Impact Offroading more secure, we request that you verify your account. Once done please type your verification code here. **You have 5 minutes to do this**\n\n*Type Your Verification Code Below*",color=0xf04747)
                embed.set_author(name="[Click Here to Verify]", url="https://impactatv.com/verify/" + str(ctx.author.id))
                await ctx.send(embed=embed)

                try:
                    code = await self.bot.wait_for('message', timeout=300.0)
                except asyncio.TimeoutError:
                    embed = discord.Embed(title=":x: "   + str(ctx.author.name) +  ", You took too long to send your verification code.",color=0xf04747)
                    return await ctx.send(embed=embed)

                if int(code.content):
                    if(banned):
                        embed = discord.Embed(title=":no_entry: "   + str(ctx.author.name) +  ", Your account has been blacklisted from the Impact Network.",color=0xf04747)
                        return await ctx.send(embed=embed) 
                    else: 
                        embed = discord.Embed(title=""  + str(ctx.author.name) + ", Your account was verified.",color=0x47f084)
                        await user.add_roles(this_role)
                        await ctx.send(embed=embed)


    @commands.command(aliases=['api'])
    async def connection(self, ctx):
        """ About the bot """
        try:
            data = urllib.request.urlopen("http://impactatv.com/apiping").read()
        except:
            data = '{}';
            print("error");
        output = json.loads(data)
        embedColour = discord.Embed.Empty
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        try: 
            embed=discord.Embed(title="Lynx Impact API Status & Information", color=0x00ffb8)
            embed.set_author(name="LynxAPI Information", icon_url="https://media.discordapp.net/attachments/764915659002871858/769763505318395914/impact-discord.png")
            embed.add_field(name="Lynx API Version", value="LynxAPI " + str(output["version"]), inline=True)
            embed.add_field(name="Impact Version", value="Release v" + str(output["impactversion"]), inline=True)
            embed.add_field(name="Impact Auth2 Version", value="7.6", inline=True)
            embed.add_field(name="Connection Status", value=":white_check_mark: Operational ", inline=True)
            embed.add_field(name="API Status", value=str(output["pingstatus"]), inline=False)
        except:
            embed=discord.Embed(title="Lynx Impact API Status & Information", color=0xf04747)
            embed.set_author(name="LynxAPI Information", icon_url="https://media.discordapp.net/attachments/764915659002871858/769763505318395914/impact-discord.png")
            embed.add_field(name="Lynx API Version", value="N/A", inline=True)
            embed.add_field(name="Impact Version", value="N/A", inline=True)
            embed.add_field(name="Impact Auth2 Version", value="N/A", inline=True)
            embed.add_field(name="Connection Status", value=":x: Outage ", inline=True)
            embed.add_field(name="API Status", value="5003", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ev'])
    async def events(self, ctx):
        embed=discord.Embed(title="Your upcoming events",description="You currently have no active events on your impact account.", color=0x4776f0)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
