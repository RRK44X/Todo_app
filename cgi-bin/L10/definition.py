#r01
#22K1011 工藤理香

import requests
import json

def Date_Time():
    appId="c5700314605b29b57bd673de602b685a"
    response=requests.get("https://worldtimeapi.org/api/timezone/Asia/Tokyo",
                        params={"appId":appId,
                                })
    response.encoding="utf-8"
    result=json.loads(response.text)
    date=result["datetime"].split("T")[0]
    time=result["datetime"].split("T")[1].split(".")[0]
    day=result["day_of_week"]
    day_list=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    day=day_list[day]
    time=list(map(int, time.split(":")))

    for i in range(len(time[:3])):
        if time[:3][i]//10==0:
            time[:3][i]="0"+str(time[:3][i])
    date_time=f"""
    <br>
    <p class="Date">{str(date)}  {str(day)}</p>
    <p class="Time">{time[:3][0]}:{time[:3][1]}:{time[:3][2]}</p>
    """
    return date, date_time

def Weather():
    response=requests.get("https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json")
    result=json.loads(response.text)
    weather_code={1:"晴れ", 2:"曇り", 3:"雨", 4:"雪"}
    weather=weather_code[int(result[0]["timeSeries"][0]["areas"][0]["weatherCodes"][0])//100]
    pops=result[0]["timeSeries"][1]["areas"][0]["pops"]
    pop=sum(list(map(int,pops[:4])))/4
    temps=list(map(int, result[0]["timeSeries"][2]["areas"][0]["temps"]))
    temp=sum(temps)/2
    
    if weather=="晴れ":
        src="/images/tenki_hare.png"
    elif weather=="曇り":
        src="/images/tenki_kumori.png"
    elif weather=="雨":
        src="/images/tenki_ame.png"
    else:
        src="/images/tenki_yuki.png"
    weather=f"""
    <img src={src} class="Picture">
    <p class="PopTemp">{pop}%　　{temp}℃</p>
    """
    if pop>80:
        weather+="<p>傘を持って出かけましょう</p>"
    elif pop>40:
        weather+="<p>折りたたみ傘を持ちましょう</p>"
    else:
        weather+="<br>"
    return weather