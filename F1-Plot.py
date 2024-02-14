from bs4 import BeautifulSoup
from PIL import Image
from matplotlib import pyplot as plt
import requests


# specific link key words and track distances in a dict
track_data = {
  "t_link": ["1124/bahrain", "1125/saudi-arabia", "1108/australia", "1109/italy", 
             "1110/miami", "1111/spain", "1112/monaco", "1126/azerbaijan",
             "1113/canada", "1114/great-britain", "1115/austria", "1116/france",
             "1117/hungary", "1118/belgium", "1119/netherlands", "1120/italy",
             "1133/singapore", "1134/japan", "1135/united-states", "1136/mexico", 
             "1137/brazil", "1138/abu-dhabi"],
  "t_distance_km": [5.412, 3.450, 5.278, 4.908, 5.412, 4.675, 3.337, 6.003,
                    4.361, 5.891, 4.318, 5.842, 4.381, 7.004, 4.259, 5.793,
                    5.063, 5.807, 5.513, 4.304, 4.309, 5.280]
}
x = 0
# exception made for sprint races, link to data changes
if (track_data["t_link"][x] == '1109/italy') or (track_data["t_link"][x] == '1115/austria') or (track_data["t_link"][x] == '1137/brazil'):
    link = "https://www.formula1.com/en/results.html/2022/races/"+track_data["t_link"][x]+"/sprint-grid.html"
else: 
    link = "https://www.formula1.com/en/results.html/2022/races/"+track_data["t_link"][x]+"/starting-grid.html"

# Making the soup
html_text = requests.get(link).text
soup = BeautifulSoup(html_text, 'lxml')
table = soup.find_all('tr')

# data scrapping function, pulling data from each link called
drivers_name = []
drivers_car = []
drivers_time = []
for rows in table[1:]:
    driver_name = rows.find("span", class_ = "last-name hide-for-mobile" )
    driver_car = rows.find("td", class_ = "semi-bold uppercase hide-for-mobile")
    driver_time = rows.find_all("td", class_ = "dark bold")
    drivers_name.append(driver_name.text)
    drivers_car.append(driver_car.text)
    drivers_time.append(driver_time[1].text)       

# conversion of time stamp to seconds 0.001
drivers_time_s = []
for time in drivers_time:
    if ':' in time:
        split = time.split(":")
        time_s = (int(split[0]) * 60) + float(split[1])
        drivers_time_s.append(time_s)
    else:
        drivers_time_s.append(time)

# take the time of lap and divide by total track distance, or length, to get 
# ratios. Use ratios in relation to 1st place time to get all data.
total_dis = [0]
total_time = [0]
distance_m = track_data["t_distance_km"][x] * 1000
ratio_1st = drivers_time_s[0]/distance_m 
for time in drivers_time_s[1:3]:
    ratio_23 = time/distance_m
    master_ratio = ratio_23/ratio_1st
    dif_ratio = master_ratio - 1
    dif_distance = dif_ratio * distance_m #difference in distance from 1st
    total_dis.append(dif_distance)
    dif_time = dif_ratio * time #difference in time from 1st
    total_time.append(dif_time)
dif_dis = [total_dis[1], total_dis[2]-total_dis[1]]
dif_t = [total_time[1], total_time[2]-total_time[1]]
car_length_m = 5.5
rank = [1, 2, 3]
cars = [Image.open('Red Bull.png'), Image.open('Mercedes.png'),
       Image.open('Mclaren.png'), Image.open('Ferrari.png'),
       Image.open('Alpine.png'), Image.open('Haas.png')]
car_t3 = [Image.open('Ferrari.png'), Image.open('Red Bull.png'), Image.open('Ferrari.png')]  
plt.scatter(total_dis, rank)
plt.show()

'''error with markers, gunna be a hard one figuring it out'''

''' data is pulled, gotta plot to show the difference'''
