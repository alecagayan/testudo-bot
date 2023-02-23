import discord
from discord.ext import commands
import requests
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt


class Planetterp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pingplanet(self, ctx):
        await ctx.send('PongPlanet!')

    @commands.command()
    async def course(self, ctx, *, course: str):

        #api request to https://planetterp.com/api/v1/course?name=course
        courseresponse = requests.get(f'https://planetterp.com/api/v1/course?name={course}')
        courseresponse = courseresponse.json()
        coursename = courseresponse['name']    

                        #get all grades https://planetterp.com/api/v1/grades?course=math140
        gradesresponse = requests.get(f'https://planetterp.com/api/v1/grades?course={course}')
        gradesresponse = gradesresponse.json()


        #create dictionary for grades and counts
        grades = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "F": 0,
            "W": 0,
            "Other": 0
        }
        #go through each item and tally up A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-, F, W, and Other
        #each item is formatted as {"course":"MATH140","professor":null,"semester":"201201","section":"0101","A+":0,"A":2,"A-":0,"B+":0,"B":0,"B-":0,"C+":0,"C":0,"C-":0,"D+":0,"D":2,"D-":0,"F":1,"W":3,"Other":0}
        for item in gradesresponse:
            #go through each grade and add it to the dictionary
            for grade in grades:
                #if the grade contains a + or -, remove the + or -
                if grade in item:
                    if '+' in grade:
                        grade = grade.replace('+', '')
                    elif '-' in grade:
                        grade = grade.replace('-', '')
                    #add the count to the dictionary
                    grades[grade] += item[grade]

        gradesum = sum(grades.values())
        #convert dictionary to percentages
        for grade in grades:
            grades[grade] = grades[grade] / gradesum * 100



        print("Grades: " + str(grades))

        df = pd.DataFrame.from_dict(grades, orient='index', columns=['Percentage of students'])
        print(df)
        fig = px.bar(df, x=df.index, y="Percentage of students", title=f'Grades for {coursename}')
        fig.write_image("grades.png")
        
        courseresponse['description'] = courseresponse['description'].replace('<i>', '').replace('</i>', '').replace('<b>', '**').replace('</b>', '**')

        #trim description to 1000 characters
        if len(courseresponse['description']) > 332:
            courseresponse['description'] = courseresponse['description'][:332] + "..."
        
        file = discord.File("grades.png", filename="grades.png")
        embed=discord.Embed(title=courseresponse['name'] + " - " + courseresponse['title'], url="https://planetterp.com/course/" + courseresponse['name'], description=courseresponse['description'])
        embed.set_thumbnail(url="https://planetterp.com/static/images/logo.png")
        embed.add_field(name="Average GPA", value="2.215", inline=True)
        embed.add_field(name="Credits", value="4", inline=True)
        #embed add grades.png local file
        embed.set_image(url="attachment://grades.png")
        msg = await ctx.send(file=file, embed=embed)
        

def setup(bot):
    bot.add_cog(Planetterp(bot))
