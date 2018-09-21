#THIS IS THE BASE CODE FOR FINDING CORRELATION BETWEEN WEIGHT/CAREER IN NBA

#import sqlite
import sqlite3

#Open connection to database
db = sqlite3.connect('sql_file.db')

#Create a Cursor object to read database and execute SQL; 
cursor = db.cursor()

#Reset the table 
try:
	cursor.execute('DROP TABLE players_stats_sql')
	db.commit()
finally:
	pass

#Create SQL table 
cursor.execute('''
	CREATE TABLE players_stats_sql(
	id_sql INT PRIMARY KEY,
	years_start_sql INT,
	years_end_sql INT,
	weight_sql INT,
	height_sql INT)
''')
db.commit()

#Open database file, creates new output file, reads database file
file = open("player_data.csv", "r")
new_csv = open("nba_players_career_length.csv", "w")
lines = file.readlines()

#create empty lists, grouped by weight range, to insert career duration into 
under_175 = []
between_176_210 = []
between_211_240 = []
between_241_270 = []
above_271 = []

#create empty lists, grouped by height range, to insert career duration into 
under_six_one = []
six_two_and_four = []
six_five_and_seven = []
six_eight_and_eleven = []
seven_plus = []

#For-Loop parse on database file and inserts parsed data in SQL table
for player in lines[1:]:
	example_split = player.strip().split(",")
	year_start = int(example_split[1])
	year_end = int(example_split[2])

	duration = year_end - year_start

	try:
		weight = int(example_split[5])
	except:
		pass

	height = example_split[4]
	
	#begin height unit conversion
	parsed_height = height.split("-")
	try:
		ft_height = int(parsed_height[0])
	except:
		pass
	try:
		in_height = int(parsed_height[1])
	except:
		pass
	ft_conversion = ft_height * 12
	total_inch_height = ft_conversion + in_height
	#end height unit conversion

	#begin weight calculation
	if weight <= 175 and year_end != 2018:
		under_175.append(duration)
	elif 176 <= weight <= 210 and year_end != 2018:
		between_176_210.append(duration)
	elif 201 <= weight <= 225 and year_end != 2018:
		between_211_240.append(duration)
	elif 226 <= weight <= 250 and year_end != 2018:
		between_241_270.append(duration)
	elif weight >= 251 and year_end != 2018:
		above_271.append(duration)
	#end weight calculation

	#begin height calculation
	if total_inch_height < 73 and year_end != 2018:
		under_six_one.append(duration)
	elif 73 <= total_inch_height <= 76 and year_end != 2018:
		six_two_and_four.append(duration)
	elif 77 <= total_inch_height <= 79 and year_end != 2018:
		six_five_and_seven.append(duration)
	elif 80 <= total_inch_height <= 83 and year_end != 2018:
		six_eight_and_eleven.append(duration)
	elif total_inch_height >= 84 and year_end != 2018:
		seven_plus.append(duration)
	#end weight calculation

	player_info = [year_start, year_end, weight, total_inch_height]

	#insert parsed data into SQL table
	cursor.execute('''
		INSERT INTO players_stats_sql(years_start_sql, years_end_sql, weight_sql, height_sql) 
		VALUES (?,?,?,?)''', player_info)
	db.commit()

#prints weight result in python
print("Avg career length of players under 175lb:")
print(sum(under_175)/len(under_175))

print("Avg career length of players between 176lb and 210lb:")
print(sum(between_176_210)/len(between_176_210))

print("Avg career length of players between 211lb and 240lb:")
print(sum(between_211_240)/len(between_211_240))

print("Avg career length of players between 241lb and 270lb:")
print(sum(between_241_270)/len(between_241_270))

print("Avg caeer length of players over 271lb:")
print(sum(above_271)/len(above_271))


#prints heigh result in python
print("Avg career length of players under 6'1:")
print(sum(under_six_one)/len(under_six_one))

print("Avg career length of players between 6'2 n 6'4")
print(sum(six_two_and_four)/len(six_two_and_four))

print("Avg career length of players between 6'5 n 6'7:")
print(sum(six_five_and_seven)/len(six_five_and_seven))

print("Avg career length of players between 6'8 and 6'11:")
print(sum(six_eight_and_eleven)/len(six_eight_and_eleven))

print("Avg career length of players over 7':")
print(sum(seven_plus)/len(seven_plus))

#remove active players 
cursor.execute('''
	DELETE FROM players_stats_sql WHERE years_end_sql = 2018
	''')
db.commit()

#add header to new_csv file
new_csv.write("Career length in NBA, Weight, Height\n")

#pull data from SQL and insert into new_csv file
for new_row in cursor.execute('''
	SELECT 
	years_end_sql - years_start_sql AS duration,
	weight_sql,
	height_sql
	FROM players_stats_sql 
	'''):

#turn list into a string
	sql_string = str(new_row)

#removes () from string
	new_csv.write(sql_string[1:(len(sql_string)-1)])
	new_csv.write("\n")

print ("script is complete")