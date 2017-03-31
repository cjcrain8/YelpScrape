 #!/user/bin/python

"""

##################################################
##												##
## 	YELP SCRAPE									##
##												##
##	Chelsea Crain								##
##	04/02/2016									##
##												##
## 	This program scrapes Yelp.com and			##
##	saves restaurant home page and menus		##
##	if they exist 								##
##												##
##################################################


"""

from __future__ import print_function, division
from lxml import html
import csv
import urllib2
import requests
import time, os, re, math, random
import sys
import unicodedata
from random import shuffle 
import random

ascii_dict = {'%3A': ':', '%2F': '/', '%3D': '=', '%3F': '?', '%25':'%',
				'%2D':'-', '%5F': '_', '%2E': '.', '%2C':','}
	
headers={'user-agent' : "Mo"}


def multiple_replace(dict, text):
    """http://stackoverflow.com/questions/15175142/
    how-can-i-do-multiple-substitutions-using-regex-in-python
    """
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

def parse_redirect(url):
    out = re.sub(r'.*url=', '', url)
    out = multiple_replace(ascii_dict, out)
    return out


def remove_duplicates(num):
	""" Reads in the number of different restuarants in the county.
		Restaurant "names" are time-stamps.  
		Some restaurants have multiple files, so this funciton
			removes duplicate names and returns a list of unique 
			restaurant names.

	"""
	seen = set()
	seen_add = seen.add
	return [el for el in num if not (el in seen or seen_add(el))]
	
def listmaker(area, csvname, maintree, agentlist, neigh_out, path):

	# ipurl ='http://my-ip.herokuapp.com/'
	# mainpage3 = requests.get(ipurl)
	# maintree3 = html.fromstring(mainpage3.content)
	# ip = maintree3.xpath('.//*[@id="viewsource"]//text()')
	# print(ip)

	## with open... list_out = 
	#list_out = codecs.open(csvname,"a",encoding='utf-8')
	
	file_name = os.path.join(path,'first_time.txt')
	
	if os.path.isfile(file_name):
		first_time = False
		os.remove(file_name)
		
	elif not os.path.isfile(file_name):
		first_time = True
		file = open(file_name, 'w')
		file.close()
	
	
	url = "http://www.yelp.com/search?cflt=restaurants&l=p:" + area
	print(area)
	print(url)
	try:
		agentname = random.choice(agentlist)
		temppage = requests.get(url, headers={'User-agent': agentname})
		temptree = html.fromstring(temppage.content)
		no_bot = temptree.xpath('.//*[@class="pseudo-input_text"]//text()')
		print(no_bot)
		if no_bot == []:
			print("UH OH! CAN'T ACCESS MAIN PAGE")
			print(time.strftime("%H:%M:%S"))
			#sys.exit(0)
			exit()
	except:
		try:
			time.sleep(10)
			agentname = random.choice(agentlist)
			temppage = requests.get(url, headers={'User-agent': agentname})
			temptree = html.fromstring(temppage.content)
			no_bot = temptree.xpath('.//*[@class="pseudo-input_text"]//text()')
			print(no_bot)
			if no_bot == []:
				print("UH OH! CAN'T ACCESS MAIN PAGE")
				print(time.strftime("%H:%M:%S"))
				#sys.exit(0)
				exit()
		except:
			if first_time == True:
				print("FIRST TIME")
				print("OH SNAP! CAN'T ACCESS FIRST SEARCH PAGE")
				print(time.strftime("%H:%M:%S"))
				#sys.exit(0)
				exit()
			elif first_time == False:
				with open(neigh_out, 'a') as csvfile:
					writer = csv.writer(csvfile, lineterminator ='\n')
					writer.writerow([area, "Finished", "\n"])
				print("bad link")
				exit()
				
	# find total number of results
	try:
		results = [item.strip() for item in 
					temptree.xpath('//*[@class="pagination-results-window"]//text()')]
		num = results[0]
		splitted = num.split()
		num_results = int(splitted[3])
		print("Number results: %s" %num_results)
		no_bot = temptree.xpath('.//*[@class="pseudo-input_text"]//text()')
		print(no_bot)
		if no_bot == []:
			print("UH OH! CAN'T ACCESS MAIN PAGE")
			print(time.strftime("%H:%M:%S"))
			#sys.exit(0)
			exit()
	except:
		nothing = open("nothing.csv",'a')
		nothing.write(area + "\n")
		return "Nothing was Found"
	
	# need a new filter if more than 100 pages 
	
	max = 1000
	if (num_results > max ):
		additional_filter = ["&attrs=RestaurantsPriceRange2.1","&attrs=RestaurantsPriceRange2.2","&attrs=RestaurantsPriceRange2.3","&attrs=RestaurantsPriceRange2.4"]
	else:
		additional_filter = [""] # if no additional filter, only do loop once
	print(additional_filter)
	for filter in additional_filter:
		# reload page 1 with the filters, and get the number of pages.
		print (filter)
		url = "http://www.yelp.com/search?cflt=restaurants" + filter + "&l=p:" + area
		try:
			agentname = random.choice(agentlist)
			mainpage2 = requests.get(url, headers={'User-agent': agentname})
			maintree2 = html.fromstring(mainpage2.content)
		except:
			try:
				time.sleep(10)
				agentname = random.choice(agentlist)
				mainpage2 = requests.get(url, headers={'User-agent': agentname})
				maintree2 = html.fromstring(mainpage2.content)
			except:
				print("UH OH! CAN'T ACCESS SEARCH PAGE")
				print(time.strftime("%H:%M:%S"))
				#sys.exit(0)
				exit()
		# get current page and total pages
		
		try:
			pages= [item.strip() for item in 
					maintree2.xpath('//*[contains(@class,"page-of-pages")]//text()')]
			page = pages[0]
			print(pages)
			splitted = page.split()
			cur_page = int(splitted[1])
			total_page = int(splitted[3])
			print("Current page: %s" %cur_page)
			print("Total page: %s" %total_page)
		except:
			nothing = open("nothing.csv",'a')
			nothing.write(area + "/n")
			return "Nothing was Found"
		## check if we already scraped this and start on the page that we need to.
		## db = map(None,  .......
		
		#try:
		with open(csvname, 'r') as csvfile:
			mycsv = csv.reader(csvfile)
			donepages = []
			for row in mycsv:
				hood = row[1]
				if hood == area:
					pages = int(row[3])
					#print(pages)
					donepages.append(pages)
					#print(donepages)
		p = len(donepages)
			
		# except:
			# p = 0
		print(p)
		if (total_page-1)*10 < p:
			return "We're done with this neighborhood yo"
		else:
			cur_page = int(math.floor(p/10)+1)
		print(cur_page)
		
		while(cur_page <= total_page):
			if random.sample(range(100),1)[0] == 1:
				print("Pausing")
				### incremendt this back up eventually
				time.sleep(.4)
			url = "http://www.yelp.com/search?cflt=restaurants&start=" + str((cur_page-1)*10) + filter + "&l=p:" + area
			try:
				searchpage = requests.get(url, headers)
				searchtree = html.fromstring(searchpage.content)
			except:
				try:
					searchpage = requests.get(url, headers)
					searchtree = html.fromstring(searchpage.content)
				except:
					print("UH OH! CAN'T ACCESS SEARCH PAGE # %s" %cur_page)
					print(time.strftime("%H:%M:%S"))
					#sys.exit(0)
					exit()
			print(url)
			print(cur_page)
			print(total_page)
			#we want to get a list of restaurants.
			for item in searchtree.xpath('//*[@class="search-result natural-search-result"]'):
				try: search_num = [el.strip() for el in item.xpath('.//@data-key')]
				except: search_num = ""
				print(search_num)
				try: 
					name = [el.strip() for el in item.xpath('.//*[@data-analytics-label="biz-name"]//text()')]
					if name == []:
						name = ['NA']
				except: name = ['NA']
				
				#print(name)
				try: 
					id = [el.strip() for el in item.xpath('.//@href')]
					id = id[0]
				except: id = ""
				#print(id)	
				try: 
					rating = [el.strip() for el in item.xpath('.//@title')]
					if rating ==[]:
						rating = ['NA']
				except: rating = ['NA']
				#print(rating)
				try: 
					reviews = [el.strip() for el in item.xpath('.//*[@class="review-count rating-qualifier"]//text()')]
					if reviews ==[]:
						reviews = ['NA']
				except: reviews = ['NA']
				#print(reviews)
				try: 
					dress =  [el.strip() for el in item.xpath('.//address//text()')]
					address = dress[0] + dress[1]
				except: address = ""
				#print(address)
				try: 
					phone = [el.strip() for el in item.xpath('.//*[@class="biz-phone"]//text()')]
					if phone == []:
						phone = ['NA']
				except: phone = ['NA']
				#print(phone)
				time.sleep(.2)
				with open(csvname, 'a') as csvfile:
					# print(search_num[0])
					# print(name[0])
					
					# print(id)
					# print(rating[0])
					try:
						writer = csv.writer(csvfile, lineterminator ='\n')
						writer.writerow([str(int(round(time.time()*1000))), area,
							filter , search_num[0], unicode(name[0]).encode("utf-8"), id, rating[0],
							reviews[0], address, phone[0], '\n'] )
					except:
						print("unicode?")
				# list_out.write(str(int(round(time.time()*1000))) + "," + 
					# area.replace('\n',"") + "," + filter + "," + search_num + 
					# "," + name + "," + id + "," + rating + "," + reviews + "," + 
					# address + "," + phone + "\n")
					
			if cur_page <= total_page:
				cur_page += 1
			print(cur_page)
					
	return "Neighborhood Parsed!"

				
def menu_grabber(done_rest, area, csvname, haveyelp, yelpgot, haveexternal, gotexternal, agentlist, path):

	
	yelpmenu = False
	external = False
	
	# read in done_list
	try: 
		donelist = []
		with open("done.csv", 'r') as csvfile:
			mycsv = csv.reader(csvfile)
			for row in mycsv:
				name = str(row[0])
				donelist.append(name)
				
	except: donelist = []
	
	full_done_rest=open(os.path.join(path,"done_rest.csv"), "a")
	
	#print(donelist)
	done_file = open("done.csv","a")
	# get list of time names
	time_names = []
	unique_list = []
	print(csvname)
	with open(csvname, 'r') as csvfile:
		mycsv = csv.reader(csvfile)
		for row in mycsv:
			hood = row[1]
			#print(hood)
			if hood == area:
				name = str(row[0])
				time_names.append(name)
				id = str(row[5])
				unique_list.append(id)
			
		# print(time_name)
		#print(len(unique_list))
		
	# get info from each restaurant
	print(len(unique_list))
	i = 0
	
	x = [i for i in range(len(unique_list))]
	shuffle(x)
	print(x)
	
	for i in x:
		
		yelpmenu = False
		external = False
		print (i) 
		time_name = time_names[i]
		print(time_name)
		url_id = unique_list[i]

		if (not time_name in donelist) and (not url_id in done_rest):		
			if random.sample(range(100),1)[0] == 1:
				print("Pausing")
				time.sleep(7)
			url = "http://www.yelp.com" + url_id
			time.sleep(.3)
			print(url)
			try:
				agentname = random.choice(agentlist)
				print(agentname)
				mainpage = requests.get(url, headers={'User-agent': agentname})
				maintree = html.fromstring(mainpage.content)
				no_bot = maintree.xpath('.//*[@class="pseudo-input_text"]//text()')
				#print(no_bot)
				if no_bot == []:
					print("UH OH! CAN'T ACCESS MAIN PAGE")
					print(time.strftime("%H:%M:%S"))
					#sys.exit(0)
					exit()

			except:
				try:
					time.sleep(10)
					agentname = random.choice(agentlist)
					print(agentname)
					mainpage = requests.get(url, headers={'User-agent': agentname})
					maintree = html.fromstring(mainpage.content)
					no_bot = maintree.xpath('.//*[@class="pseudo-input_text"]//text()')
					#print(no_bot)
					if no_bot == []:
						print("UH OH! CAN'T ACCESS MAIN PAGE")
						print(time.strftime("%H:%M:%S"))
						#sys.exit(0)
						exit()
				except:
					try:
						time.sleep(10)
						agentname = random.choice(agentlist)
						print(agentname)
						mainpage = requests.get(url, headers={'User-agent': agentname})
						maintree = html.fromstring(mainpage.content)
						no_bot = maintree.xpath('.//*[@class="pseudo-input_text"]//text()')
						#print(no_bot)
						if no_bot == []:
							print("UH OH! CAN'T ACCESS MAIN PAGE")
							print(time.strftime("%H:%M:%S"))
							#sys.exit(0)
							exit()
					except:
						print("UH OH! CAN'T ACCESS RESTAURANT MAIN PAGE")
						print(time.strftime("%H:%M:%S"))
						#sys.exit(0)
						exit()
			# os.chdir()
			with open(time_name + "_mainpage.html", 'wb') as fid:
				fid.write(mainpage.content)
			print("File Written")
			
			# get menus
			try: # first get yelp formatted menus
				time.sleep(3.5)
				#menufileY = requests.get(url, headers)
				#menutree = html.fromstring(mainpage.content)
				elem = maintree.xpath('.//*[contains(@class,"menu-explore")]/@href' )
				print(str(elem[0]))
				page = "http://www.yelp.com" + str(elem[0])
				print(page)
				yelpmenu = True
				haveyelp += 1 
			except:
				try: # then get external  menus
					time.sleep(2)
					#menufileE = requests.get(url, headers)
					#menutreeE = html.fromstring(menufileE.content)

					external = maintree.xpath('.//*[contains(@class,"external-menu")]')
					elem = maintree.xpath('.//*[contains(@class,"menu-link-block")]//@href')
					print(str(elem[0]))
					page = str(elem[0])
					external = True
					haveexternal += 1
				except:
					page = "nolink"
					print("No menu found")
			
			# print menu files
			end = ""
			if "pdf" in page:
				menu = time_name + ".pdf"
				page = page.split('&website_link_type')[0]
				newpage = parse_redirect(page)
				print(newpage)
				try:
					time.sleep(4.5)
					agentname = random.choice(agentlist)
					response = requests.get(newpage, headers={'User-agent': agentname})
					#page_content = content.read()
					with open(menu, 'wb') as output:
						output.write(response.content)
#					file.write(response.read())
#					file.close()
					if external == True:
						gotexternal += 1 
				except:
					print("wtf")
				print("Pdf menu fetched")
			elif page != "nolink":
				try:
					if external==True:
						if "redir" in page:
							page = parse_redirect(page)
						print(page)
						gotexternal += 1
						output = open(time_name + ".log", "w")
						time.sleep(2.5)
						menu = time_name + end
						agentname = random.choice(agentlist)
						file = requests.get(page, headers={'User-agent': agentname})
						#page_content = content.read()
						with open(menu, 'wb') as fid:
							fid.write(file.content)
						output.close()
						print("Html external menu file fetched")
					if yelpmenu == True:
						if not page.startswith("http://www.yelp.com"):
							page = "http://www.yelp.com" + page
						output = open(time_name + ".log", "w")
						time.sleep(.8)
						menu = time_name + end
						agentname = random.choice(agentlist)
						file = requests.get(page, headers={'User-agent': agentname})
						#page_content = content.read()
						with open(menu, 'wb') as fid:
							fid.write(file.content)
						output.close()
						print("Yelp menu file fetched")
						yelpgot += 1
				except:
					nothing = open("nothing.csv",'a')
					nothing.write(area + "\n")
					print("No site anymore")
			done_rest.append(url_id)		 
			donelist.append(time_name)
			done_file.write(time_name + "," + page + "\n")
			full_done_rest.write(url_id + "\n")
		else:
			print("Restaruant already scraped")
		i += 1 
		

	return done_rest, haveexternal, gotexternal, haveyelp, yelpgot
			
def main(scrape_name):
	""" Drive function """
	# print("waiting to start...")
	# time.sleep(60)

	start_time = time.time()
	
	
	path = "E:\Yelp\Yelp_Scrapes\Scrape_" + scrape_name

	os.chdir(path)
	
	agentlist = []
	with open("user_agents.csv", 'r') as csvfile:
		mycsv = csv.reader(csvfile)
		for row in mycsv:
			name = str(row[0])
			agentlist.append(name)
	
	
	maindir = os.path.dirname(os.path.abspath(__file__))
	print(maindir)
	CSVDIR = os.path.join(maindir, 'csvdir')
	print(CSVDIR)
	os.chdir(maindir)
	
	neigh_out = os.path.join(maindir, "{}.csv".format("done_neighborhood"))
	# make done file if does not exist
	if not os.path.isfile("done_neighborhood.csv"):
		# print("none")		
		with open("done_neighborhood.csv", 'w') as csvfile:
			print("Done neighborhood csv created")
	else:
		print("Done csv already created")
	with open("done_neighborhood.csv", 'r') as csvfile:
		mycsv = csv.reader(csvfile)
		done = []
		for row in mycsv:
			rows = str(row[0])
			done.append(rows)
			#done = [row["done"] for row in DictReader(csvfile)]
		youre_done_for = done
		print(youre_done_for)
		
		
	done_rest = []
	# neigh_list = os.listdir(CSVDIR)
	if not os.path.isfile("done_rest.csv"):
		# print("none")		
		with open("done_rest.csv", 'w') as csvfile:
			print("Done csv created")
	else:
		print("Done csv already created")
	with open("done_rest.csv", "r") as csvfile:
		mycsv = csv.reader(csvfile)
		for row in mycsv:
			id = str(row[0])
			done_rest.append(id)
		
	# for item in neigh_list:
		# tempstate = os.path.join(CSVDIR, item)
		# state_list = os.listdir(tempstate)
		# for el in state_list:
			# with open(os.path.join(tempstate, el)) as csvfile:
				# csvreader=csv.reader(csvfile)
				# for row in csvreader:
					# done_rest.append(row[5])
	print(len(done_rest))
	time.sleep(12)
	area_list = []
	with open(os.path.join(maindir, 'neighborhood_order_min.csv')) as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			area_list.append(row[0])
	yelpgot = 0
	haveyelp = 0
	haveexternal = 0
	gotexternal = 0
	#print(area_list)
	for area in area_list:
		if not area in youre_done_for:
			os.chdir(maindir) # changes current working directory
			state = area.split(":")[0]
			for x in range(1,len(area.split(":"))):
				if area.split(":")[-x] != "":
					name = area.split(":")[-x]
					break
			try: os.mkdir(CSVDIR)
			except: print("CSV directory already there!")
			statedir = os.path.join(CSVDIR, state)
			try: os.mkdir(statedir)
			except: print("State directory already there!")
			#print(statedir)
			if "/" in name:
				name=name.replace("/", ".")
			csvname = os.path.join(statedir, "{}.csv".format(name))
			#print(csvname)
			if not os.path.isfile(csvname):
				os.chdir(statedir)
				with open(name +'.csv', 'w') as csvfile:
					print("Csvname created")
			else: print("Neighborhood directory already there!")
			name_dir = os.path.join(maindir, name)
			try:os.mkdir(name_dir)
			except: print("Neighborhood folder already there")
			os.chdir(name_dir)
			if "." in name:
				name=name.replace(".","/")
			url = "http://www.yelp.com/search?cflt=restaurants&l=p:" + area
			print(url)
			try:
				time.sleep(1.1)
				agentname = random.choice(agentlist)
				print(agentname)
				mainpage = requests.get(url, headers={'User-agent': agentname})
				maintree = html.fromstring(mainpage.content)
				no_bot = maintree.xpath('.//*[@class="pseudo-input_text"]//text()')
				#print(no_bot)
				if no_bot == []:
					print("UH OH! CAN'T ACCESS MAIN PAGE")
					print(time.strftime("%H:%M:%S"))
					#sys.exit(0)
					exit()
			except:
				try:
					time.sleep(10)
					agentname = random.choice(agentlist)
					print(agentname)
					mainpage = requests.get(url, headers={'User-agent': agentname})
					maintree = html.fromstring(mainpage.content)
					no_bot = maintree.xpath('.//*[@class="pseudo-input_text"]//text()')
					#print(no_bot)
					if no_bot == []:
						print("UH OH! CAN'T ACCESS MAIN PAGE")
						print(time.strftime("%H:%M:%S"))
						#sys.exit(0)
						exit()
				except:
					print("UH OH! CAN'T ACCESS MAIN PAGE")
					print(time.strftime("%H:%M:%S"))
					#sys.exit(0)
					exit()
				
			# find and make list of all cities (da_hood)
			cities = [item.strip() for item in maintree.xpath('//*'
				'[@class="place radio-check"]'
				'//input[@name="place"]/@value')]
			# cities = [item.strip() for item in maintree.xpath('//*[@class="main"]'
				# '//label[@class="place radio-check"]'
				# '//input[@name="place"]/@value')]
			cities = [var for var in cities if var]	
			cities = remove_duplicates(cities)
			print (cities)
			
			
			#need to check and see if area has already been parsed
			j= None
			i=0
			# print("FIRST ITEM IN CITIES: %s" %cities[0])
			# print("LENGTH OF CITIES: %s" %len(cities))
			for town in cities:
				#town = "Albany"
				# if " " in town:
					# town = town.replace(" ", "_")
				# if "," in town:
					# state = town.split(",_",1)[1]
					# print(state)
					# town = town.split(",",1)[0]
					# state_neigh = state + ":" + town + "::"	
				# elif area.split(":")[3] != "":
					# state = area.split(":")[0] + ":" + area.split(":")[1]
					# state_neigh = state + "::" + town
			
				# else:
					# state_neigh = state + ":" + town + "::"	
				state_neigh = town
				print("i = %s" %i)
				#print("Town: %s" %town)
				print(state_neigh)
				if state_neigh in youre_done_for:
					print("Already done!")
					i+=1
					if i == (len(cities)-1):
						# print("IN THE LOOP")
						with open(neigh_out, 'a') as csvfile:
								writer = csv.writer(csvfile, lineterminator ='\n')
								writer.writerow([cities[0], "Finished", "\n"])
						youre_done_for.append(cities[0])
						print("ADDED FIRST NEIGHBORHOOD TO DONE: %s" %cities[0])
					continue
				time.sleep(1.5)
				j = listmaker(state_neigh, csvname, maintree, agentlist, neigh_out, path)
				print(j)
				
				#j= "Hi"
				print("Parsing the Menus.............")
				if j != "Nothing was Found" and j:
					done_rest, haveexternal, gotexternal, haveyelp, yelpgot = menu_grabber(done_rest, state_neigh,csvname, haveyelp, yelpgot, haveexternal, gotexternal, agentlist, area)
				
				
				
				if (i > 0) and (i < len(cities)):
					with open(neigh_out, 'a') as csvfile:
							writer = csv.writer(csvfile, lineterminator ='\n')
							writer.writerow([state_neigh, "Finished", "\n"])
					youre_done_for.append(state_neigh)
					
				if i == (len(cities)-1):
					print("IN THE LOOP")
					with open(neigh_out, 'a') as csvfile:
							writer = csv.writer(csvfile, lineterminator ='\n')
							writer.writerow([cities[0], "Finished", "\n"])
					youre_done_for.append(cities[0])
					print("ADDED FIRST NEIGHBORHOOD TO DONE: %s" %cities[0])
				i+=1
	print("Woot woot!!")
	total_time = time.time()-start_time
	if total_time < 60:
		print ("Run time: %s seconds " %total_time)
	if total_time >= 60 and total_time < 3600:
		total_time = total_time / 60
		print ("Run time: %s minutes " %total_time)
	if total_time >= 3600:
		total_time = (total_time/60)/60
		print ("Run time: %s hours " %total_time)
	
	os.chdir(maindir)
	
if __name__ == '__main__':
    main(sys.argv[1])
