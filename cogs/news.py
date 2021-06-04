import os
import discord
from pymongo import MongoClient
from discord.ext import commands

MONGODB = os.environ["MONGODB"]

class News(commands.Cog):
  
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def news(self, ctx, news):
    author = ctx.author.id
    cluster = MongoClient(MONGODB)
    db = cluster['disslash']
    news = db['news']
    count = news.count_documents({})
    try:
      post = {"_id": count + 1, "news": news}
      notes.insert_one(post)

      embed = discord.Embed(title="New News Update")
      embed.add_field(name="`New News`", value = news)
      await ctx.send(embed=embed)
    
    except:
      await ctx.send("Post Failed To Send, Please Fix")
      
      
def setup(client):
    client.add_cog(News(client))
    
  
