import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import pymongo
from pymongo import MongoClient
import random
import topgg

#!


#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
async def get_premios_from_database(guild_id, member_id):
    try:
        cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
        db = cluster["awardsbot"]
        collection = db["entradas"]

        # Realizar la consulta a la base de datos utilizando la instancia del cliente MongoDB
        results = list(collection.find({"guild_id": guild_id, "id_usuario": member_id}))

        # Cerrar la conexión a la base de datos
        cluster.close()

        return [result["premio_usuario"] for result in results]
    except Exception as e:
        print(f"Error al obtener los premios desde la base de datos: {e}")
        return []
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
async def grabar_premio(guild_id, user_id, premio):
    try:
        cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
        db = cluster["awardsbot"]
        collection = db["entradas"]
        
        # Crear el documento que representa el premio
        documento_premio = {
            "guild_id": guild_id,
            "id_usuario": user_id,
            "premio_usuario": f"- [  {premio}  ]"
        }

        # Insertar el documento en la colección
        collection.insert_one(documento_premio)

        # Cerrar la conexión a la base de datos
        cluster.close()

        return True  # Éxito al grabar el premio
    except Exception as e:
        print(f"Error al grabar el premio en la base de datos: {e}")
        return False  # Error al grabar el premio
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
async def tiene_rol_de_premios(ctx):
    try:
        cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
        db = cluster["awardsbot"]
        collection = db["roles"]
        guild_id = ctx.guild.id

        result = collection.find_one({"guild_id": guild_id})
        rol_premio = result["id_role"]
        if ctx.author.id==329450671319285763:
            return True
        for role in ctx.author.roles:
            if role.id == rol_premio:
                return True  # El usuario tiene el rol de premios

        return False  # El usuario no tiene el rol de premios
    except Exception as e:
        print(f"Error al verificar el rol de premios: {e}")
        return False  # Error al verificar el rol
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
async def chequear_voto(user_id):
    voto= await bot.topggpy.get_user_vote(user_id)
    print(voto)
    return voto
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
async def grabarinvites(bot):
    cantidadservidores=0
    contador=0
    with open('informacion_servidores.txt', 'w', encoding='utf-8') as file:
        for serv in bot.guilds:
            cantidadservidores += 1
            try:
                print(serv)
                # Obtener la lista de invitaciones del servidor
                invites = await serv.invites()
                
                # Escribir la información en el archivo de texto
                contador=0
                file.write(f'Servidor: {serv.name} - {serv.id}\n')
                for inviteb in invites:
                    if contador==3:
                        break
                    file.write(f'Invitación: {inviteb.url}\n')
                    contador=contador+1
                file.write('\n')
            except Exception as e:
                print(f'Error al procesar servidor {serv.name}: {e}')
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
#! --------------------------------------------------------------------------------------------------------------------------------------------------------------
async def contarcantidadentradas(guild_id):
    try:
        cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
        db = cluster["awardsbot"]
        collection = db["entradas"]

        # Realizar la consulta a la base de datos utilizando la instancia del cliente MongoDB
        cantidaddocumentos = collection.count_documents({"guild_id":guild_id})

        # Cerrar la conexión a la base de datos
        cluster.close()

        return cantidaddocumentos
    except Exception as e:
        print(f"Error al obtener los premios desde la base de datos: {e}")
        return []
    
async def crearembed(member,texto,ctx):
    # Crear un embed para mostrar el premio agregado
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(255, 0, 130)
    )
    embed.set_author(name="Awardsbot", url="https://discord.gg/dTFM2B5Mgw",
                    icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.add_field(name="**Awarded User:**", value=member.mention, inline=True)
    
    try:
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=ctx.guild.name,icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    except:
        pass
    embed.add_field(name="**Award:**", value=texto, inline=False)
    return embed
#!
# ? sdsad
#TODO:
#? ********************************************************************************************************************************************************************
"""

async def get_pre(bot, message):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["prefijos"]
    guildid=message.guild.id
    results = collection.find_one({"guild_id":guildid})
    
    if results["prefix"]==None:
        prefix="/"
    elif results["prefix"] !=None:
        prefix=results["prefix"]
    else:
        print("ERROR EN PREFIJO")
    return prefix"""
#? ********************************************************************************************************************************************************************
bot = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix="/",intents=discord.Intents.default())
bot.remove_command('help')
#? ********************************************************************************************************************************************************************
@bot.event
async def on_ready():
    #!Guarda las invites de los servidores en los que el bot tiene el permiso manage_server
    #grabarinvites(bot)
    #!-

    #? Añade los comandos
    bot.add_command(add)
    bot.add_command(awards)
    bot.add_command(role)
    bot.add_command(deleteawards)
    bot.add_command(invite)

    await bot.tree.sync()
    #? -


    estado="Support:  https://discord.gg/dTFM2B5Mgw"
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(estado))
    print('Conectado como: {0.user}'.format(bot))
    dbl_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NzA2MTI3MTEzMTQ1NTQ4OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2MDc4MzI3fQ.PCNzbQ83P2C7ly2SIRsc7DkKkQHcrxlhfpHzCMSlkqo'  # set this to your bot's Top.gg token
    bot.topggpy = topgg.DBLClient(bot, dbl_token, autopost=True, post_shard_count=True)
    cambiarestatus.start()
#? ********************************************************************************************************************************************************************
@tasks.loop(seconds=30)
async def cambiarestatus():
    statuses=["|| / ||","|| Support:  https://discord.gg/dTFM2B5Mgw ||",f"|| On {len(bot.guilds)} servers ||"]
    status=random.choice(statuses)
    await bot.change_presence(activity=discord.Game(name=status))
#? ********************************************************************************************************************************************************************
@bot.event
async def on_guild_join(guild):
    pass
@bot.event
async def on_autopost_success():
    print(f'Posted server count ({bot.topggpy.guild_count}), shard count ({bot.shard_count})')
#? ********************************************************************************************************************************************************************
@bot.event
async def on_guild_remove(guild):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=guild.id
    collection.delete_many({"guild_id":guildid})
#? ********************************************************************************************************************************************************************
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, discord.Forbidden):
        await ctx.send('**Missing Permissions/Sin Permisos**')
    if isinstance(error, commands.BadArgument):
        await ctx.send('**No mention? no text?/No pusiste mencion? no pusiste texto?**')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('**|Comando no encontrado/Not Found| Try a!help or a!ayuda**')
#! *********************************************************************************************************************************************************************
#! *********************************************************************************************************************************************************************
#! *********************************************************************************************************************************************************************
#! *********************************************************************************************************************************************************************
#! *********************************************************************************************************************************************************************
#! *********************************************************************************************************************************************************************
@commands.hybrid_command(name="add")
async def add(ctx,member:discord.Member,*,texto: str):
    await ctx.defer()
    if ctx.author.guild_permissions.administrator==True or await tiene_rol_de_premios(ctx):
        contarcantidad= await contarcantidadentradas(ctx.guild.id)
        try:
            votoelusuario=await chequear_voto(ctx.author.id)
        except Exception as e:
            print(e)
        if contarcantidad<10:
            if await grabar_premio(ctx.guild.id, member.id, texto):
                embed=await crearembed(member,texto,ctx)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error when writing the award please try again")
        elif contarcantidad < 40 and votoelusuario==True:
            if await grabar_premio(ctx.guild.id, member.id, texto):
                embed=await crearembed(member,texto,ctx)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error when writing the award please try again")
        elif contarcantidad < 300 and votoelusuario==True:
            if await grabar_premio(ctx.guild.id, member.id, texto):
                embed=await crearembed(member,texto,ctx)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error when writing the award please try again")
        elif contarcantidad < 5000 and votoelusuario==True:
            if await grabar_premio(ctx.guild.id, member.id, texto):
                embed=await crearembed(member,texto,ctx)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error when writing the award please try again")
        elif contarcantidad > 10 and votoelusuario==False:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 0, 130),
                title="Awards limit - Vote Expired",
                description="Error - you have reached awards limit. Please vote again for the bot and try again "
            )
            embed.set_author(name="Awardsbot", url="https://discord.gg/dTFM2B5Mgw",
                            icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
            embed.add_field(name="[Vote Here](https://top.gg/bot/767061271131455488/vote)",value="🏆")
            await ctx.send(embed=embed)
    else:
        await ctx.send("Forbidden, you need role or administrator perms")

#! *********************************************************************************************************************************************************************
@commands.hybrid_command(name="awards")
async def awards(ctx,member:discord.Member):
    await ctx.defer()
    lista = await get_premios_from_database(ctx.guild.id, member.id)
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    if ctx.author.id!=329450671319285763:
        embed= discord.Embed(
            title='User Awards',
            colour=discord.Colour.from_rgb(255,0,130)
        )
    else:
        embed= discord.Embed(
            title='User Awards',
            colour=discord.Colour.from_rgb(255,229,3)
        )
        embed.add_field(name="🚧|Bot Creator",value=" 🌟YES🌟")
    elmiembro=member.display_name
    embed.set_author(name=elmiembro)
    nombre=ctx.guild.name

    try:
        try:
            embed.set_thumbnail(url=member.display_avatar.url)
        except:
            pass
        try:
            user= await bot.fetch_user(member.id)
            embed.set_image(url=user.banner.url)
        except:
            pass
        seunio=discord.utils.format_dt(member.joined_at,style="R")
        secreo=discord.utils.format_dt(member.created_at,style="R")
        embed.add_field(name="📆| Created At :",value=secreo)
        embed.add_field(name="📅| Joined At :",value=seunio)
        embed.add_field(name="📍| Top Role :",value=member.top_role.mention)
        embed.add_field(name="🔰|ID",value=f"`{member.id}`")
        if member.premium_since!=None:
            embed.add_field(name="🌟| Nitro",value="Yes")
        else:
            embed.add_field(name="🌟| Nitro",value="No")
    except:
        print(Exception.__name__)

    if len(lista)==0:
        embed.add_field(name='💥| Awards',value='None yet')
        
    else:
        awards_text = '\n '.join(lista)
        embed.add_field(name='💥| Awards', value=f"**{awards_text}**", inline=False)

    embed.set_author(name="Awardsbot",url="https://discord.gg/dTFM2B5Mgw",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.set_footer(text=nombre, icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
#! *********************************************************************************************************************************************************************
@commands.hybrid_command(name="role")
@commands.has_permissions(administrator=True)
async def role(ctx,role:discord.Role):
    if role==None:
        pass
    else:
        await ctx.defer()
        cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
        db = cluster["awardsbot"]
        collection=db["roles"]
        guildid=ctx.guild.id
        collection.delete_many({"guild_id":guildid})
        post= {"guild_id":guildid,"id_role":role.id}
        collection.insert_one(post)
        await ctx.send(f"**Role:{role.mention}**")
#! *********************************************************************************************************************************************************************
@commands.hybrid_command(name="deleteawards")
@commands.has_permissions(administrator=True)
async def deleteawards(ctx,member:discord.Member):
    await ctx.defer()
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:SUSANA18@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=ctx.guild.id
    collection.delete_many({"guild_id":guildid,"id_usuario":member.id})
    await ctx.send("Deleted!")
#! *********************************************************************************************************************************************************************
@commands.hybrid_command(name="invite")
async def invite(ctx):
    embed= discord.Embed(
        colour=discord.Colour.blue(),
        title='Invita al BOT!/Invite The Bot!'
    )
    embed.set_author(name="Awardsbot",url="https://discord.gg/dTFM2B5Mgw",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.add_field(name='LINK:', value='https://discord.com/api/oauth2/authorize?client_id=767061271131455488&permissions=0&scope=bot')
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
#! *********************************************************************************************************************************************************************
bot.run('NzY3MDYxMjcxMTMxNDU1NDg4.G0BRxk.sHYip2nivS3rGA7U9oFJaI7Wm2J6Uo-Pdvqn6c') #PRODUCCION

#! *********************************************************************************************************************************************************************