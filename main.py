#写一个请求和风天气的request
import requests
import numpy as np
import matplotlib.pyplot as plt
#location = "beijing"


#获取地址
url = 'https://pv.sohu.com/cityjson?ie=utf-8'
#从这里获取ip，因为ipconfig的ipv4属于本地局域网，无法使用
r = requests.get(url)
str = r.text
loc = str[28:40]
#ip
#腾讯接口
url_loc = "https://apis.map.qq.com/ws/location/v1/ip?ip="+loc+"&key=IQ5BZ-OCJ6G-W4YQF-IBEQ2-GVG3H-3IBG6"
r_loc = requests.get(url_loc)
str_loc = r_loc.json()
city = str_loc["result"]["ad_info"]["city"]
province = str_loc["result"]["ad_info"]["province"]
nation = str_loc["result"]["ad_info"]["nation"]
location = nation+province+city
#weather
url0 = 'https://free-api.heweather.net/s6/weather/now?location='+city+'&key=b73ad3f0ea0c4ae884567768b5485097'
strhtml0 = requests.get(url0)
dic0 = strhtml0.json()
cond_txt0 = dic0["HeWeather6"][0]["now"]["cond_txt"]
tmp0 = dic0["HeWeather6"][0]["now"]["tmp"]
fl0 = dic0["HeWeather6"][0]["now"]["fl"]
wind_dir0 = dic0["HeWeather6"][0]["now"]["wind_dir"]
wind_spd0 = dic0["HeWeather6"][0]["now"]["wind_spd"]
hum0 = dic0["HeWeather6"][0]["now"]["hum"]
update_loc0 = dic0["HeWeather6"][0]["update"]["loc"]

#air_quality
url1 = 'https://free-api.heweather.net/s6/weather/lifestyle?location='+city+'&key=b73ad3f0ea0c4ae884567768b5485097'
strhtml1 = requests.get(url1)
dic1 = strhtml1.json()
brf1 = dic1['HeWeather6'][0]["lifestyle"][7]["brf"]
txt1 = dic1['HeWeather6'][0]["lifestyle"][7]["txt"]
update_loc1 = dic1["HeWeather6"][0]["update"]["loc"]

#temperature
#relative_humidity
url2 = 'https://free-api.heweather.net/s6/weather/forecast?location='+city+'&key=b73ad3f0ea0c4ae884567768b5485097'
strhtml2 = requests.get(url2)
dic2 = strhtml2.json()
tmp2 = []
hum2 = []
for i in range(3):
    a = int(dic2["HeWeather6"][0]["daily_forecast"][i]["tmp_max"])
    b = int(dic2["HeWeather6"][0]["daily_forecast"][i]["tmp_min"])
    c = (a+b)/2
    tmp2.append(c)
    hum2.append(int(dic2["HeWeather6"][0]["daily_forecast"][i]["hum"]))


#生成折线图
x = ["today","tomorrow","three days from now"]
plt.plot(x,tmp2,'r--',label = 'tmp')
plt.legend()
plt.savefig("static/images/tmp.png")
plt.close()

plt.plot(x,hum2,'b--',label = 'hum')
plt.legend()
plt.savefig("static/images/hum.png")
plt.close()



from flask import  Flask,render_template  #导入render_template模块
app=Flask(__name__)

@app.route('/')
def index():
    context = {
        'location':location,
        #weather
        'cond_txt0':cond_txt0,
        'tmp0':tmp0,
        'fl0':fl0,
        'wind_dir0':wind_dir0,
        'wind_spd0':wind_spd0,
        'hum0':hum0 ,
        'update_loc0':update_loc0,

        #air_quality
        'brf1':brf1,
        'txt1':txt1,
        'update_loc1':update_loc1,

        #temperature
        #relative_humidity
        'tmp2':tmp2,
        'hum2':hum2,
    }
    return render_template("index.html",context = context)   #调用render_template函数，传入html文件参数



if __name__=="__main__":
    app.run(port=2020,host="127.0.0.1",debug=True)
