# This file contains all functions related to server and its members information.

import nextcord
import random

from utils.responses import compliments
from nextcord.ext import commands
from utils.functions import embed, dict2fields, pages
from utils.assets import get_help_embeds

class Information(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(aliases=["pfp"], ddescription="See a member's profile picture.")
    async def user_pfp(self, ctx, member: nextcord.Member = None):
        if not member:
            member = getattr(ctx, 'user', getattr(ctx, 'author', None))
        await ctx.send(
            embed=embed(
                image=member.avatar,
                color=self.bot.color(ctx.guild),
                author=f"Profile Picture: {member}", # author = member
                footer={
                    'text': random.choice(compliments),
                    'icon_url': self.bot.user.avatar
                }
            )
        )

    
    @nextcord.slash_command(name="pfp", description="See a member's profile picture.")
    async def pfp(self, inter, member: nextcord.Member = None):
        await self.user_pfp(inter, member=member)


    @nextcord.user_command(name="pfp")
    async def pfp_app(self, inter, member: nextcord.Member):
        await self.user_pfp(inter, member)


    @commands.command(aliases=["serverinfo", "si"], description="Get information about a server.")
    async def server_information(self, ctx):
        name = str(ctx.guild.name)
        ID = str(ctx.guild.id)
        description = str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        num_mem = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon)
        role_count = len(ctx.guild.roles)
        
        await ctx.send(
            embed=embed(
                title=f"📚 {name} 📚",
                color=self.bot.color(ctx.guild),
                thumbnail=icon,
                author=ctx.guild.owner,
                description=description,
                fields=dict2fields({
                    'Owner': owner,
                    'Member Count': num_mem,
                    'Role Count': role_count,
                    'Server ID': ID,
                    'Thwipper color': nextcord.Color(self.bot.color(ctx.guild)).to_rgb()
                }, inline=True),
                footer={
                    'text': "Created on {}".format(ctx.guild.created_at.__format__('%A, %B %d, %Y @ %H:%M:%S')),
                    'icon_url': ctx.author.avatar
                },
                image=ctx.guild.banner
            )
        )


    @commands.command(aliases=["ping"], description="Bot Ping")
    async def get_ping(self, ctx):

        ping = round(self.bot.latency * 1000)
        c1 = "🟢"
        c2 = "🟡"
        c3 = "🔴"
        color = self.bot.color(ctx.guild)
        
        if ping >= 350:
            e = embed(description=f"{c3} {ping} ms", color=color)
            await ctx.send(embed=e)
        
        elif ping <= 320:
            e = embed(description=f"{c1} {ping} ms", color=color)
            await ctx.send(embed=e)
        
        elif ping > 320 and ping < 350:
            e = embed(description=f"{c2} {ping} ms", color=color)
            await ctx.send(embed=e)


    @commands.command(aliases=["help"], description="Thwipper's Help Menu")
    async def display_help_menu(self, ctx):
        await pages(ctx, get_help_embeds(self.bot.color(ctx.guild), ctx)) 

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.message.Message):
        if f"<@{self.bot.user.id}>" in message.content and not message.author.bot:
            e, view = embed(
                title="Your friendly neightbourhood Spider-Bot",
                description="Hi {}!\nI am `Thwipper`. My name comes from the onomatopoeia of Spider-Man's Webshooters. Pretty slick, eh? I have lots of cool features that you may find interesting. Check them out with `_help` command. As always, more exciting features are always in the works. Stay tuned and have fun with them.\n_Excelsior!_".format(message.author.name),
                color=self.bot.color(message.guild),
                thumbnail=self.bot.user.avatar,
                author=message.author,
                button=[
                    {
                        'label': 'Github Repository',
                        'emoji': '<:github:1004764713642627103>',
                        'url': 'https://www.github.com/spidey711/Thwipper-bot'
                    },
                    {
                        'label': 'Author',
                        'emoji': '<:spiderman:982567257584594954>',
                        'url': 'https://www.github.com/spidey711'
                    }
                ]
            )   
            await message.reply(
                embed=e,
                view=view
            )


def setup(bot, *args):
    bot.add_cog(Information(bot, *args))