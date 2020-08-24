# imports
import pandas as pd
from selenium import webdriver
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
import os

def runChromeDriver(driverAddress):
	driver = webdriver.Chrome(executable_path=r""+driverAddress)
	driver.get('https://www.facebook.com/')
	return driver

def login(username,password,driver):
	userN = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input')
	passW = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/input')
	sub = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
	try:
		userN.clear()
		userN.send_keys(username)
		passW.clear()
		passW.send_keys(password)
		sub.click()
	except:
		pass
	time.sleep(3)
	return driver
def reload(driver,maxScrollDown):
    driver.refresh()
    time.sleep(1.5)
    for i in range(maxScrollDown):
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        time.sleep(1)
    time.sleep(2)
    allPosts = driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/'+
											'div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div/div/div/div')
    return allPosts
class FacebookComments:
	def __init__(self,chromeDriverAddress,username,password):
		self.chromeAddress = chromeDriverAddress
		self.username = username
		self.password = password
	
	def mainProcess(self,driver,saveFileName,maxScrol,allCom,ind):
		allPosts = []
		while int(ind/2.5)+1 <= maxScrol:
			ind +=1
			if ind % 5 == 0:
				try:
					with open(saveFileName+'.txt', 'r',encoding='utf-8') as f:
						row1 = ""
						for row in f:
							w1 = row[:-1]
							if w1 != '_!*_':
								row1 += w1
							else:
								if not (row1 in allCom):
									allCom.append(row1)
								row1 = ""
					f.close()
					ind = int(allCom[len(allCom)-1]) + 5
					allCom = allCom[:-1]
					os.remove(saveFileName+'.txt')
				except:
					pass
				with open(saveFileName+'.txt', 'w' , encoding="utf-8") as f:
					for w in allCom:
						f.write((w)+"\n_!*_\n")
					f.write(str(ind)+"\n_!*_\n")
				f.close()
				print(len(allCom))
				allPosts = reload(driver,ind)
			try:
				try:
					showMore = allPosts[ind].find_element_by_class_name(
						'oajrlxb2.bp9cbjyn.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846'+
						'.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv'+
						'.nhd2j8a9.pq6dq46d.mg4g778l.btwxx1t3.g5gj957u.p7hjln8o.kvgmc6g5.cxmmr5t8.oy'+
						'grvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.p8fzw8mz.qt6c0cv9.a8nywdso.l9j0dhe7'+
						'.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.p8dawk7l.buofh1pr')
					actions = ActionChains(driver)
					actions.move_to_element(allPosts[ind]).perform()
					showMore.click()
					time.sleep(2)
				except  Exception as inst:
					pass
				try:
					iCheck = 0
					showMore = allPosts[ind].find_element_by_xpath(
						'div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[4]/div[1]/div[2]')
					actions = ActionChains(driver)
					actions.move_to_element(allPosts[ind]).perform()
					showMore.click()
					time.sleep(2)
					try:
						while(1):
							if iCheck > 55:
								break
							iCheck+=1
							showMore = allPosts[ind].find_element_by_xpath(
								'div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[4]/div[1]/div[2]')
							actions = ActionChains(driver)
							actions.move_to_element(allPosts[ind]).perform()
							showMore.click()
							time.sleep(1)
					except  Exception as inst:
						pass
				except Exception as inst:
					pass
				commentTags = allPosts[ind].find_elements_by_xpath('div/div/div/div/div/div/div/'
																+'div/div/div[2]/div/div[4]/div/div/div[2]/ul/li')
				for el in commentTags:
					try:
						seeMore = el.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.'+
														'e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc'+
														'684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.'+
														'hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.'+
														'i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.oo9gr5id.gpro0wi8.lrazzd5p')
						for eli in seeMore:
							if eli.get_attribute('outerHTML').split(' ')[0][1:] == 'div' and eli.get_attribute('role') == 'button' :
								actions = ActionChains(driver)
								actions.move_to_element(eli).perform()
								eli.click()
								time.sleep(1)
					except  Exception as inst:
						pass
					try :
						comment = el.find_element_by_class_name('oi732d6d.ik7dh3pa.d2edcug0.qv66sw1b.'+
													'c1et5uql.a8c37x1j.muag1w35.enqfppq2.jq4qci'+
														'2q.a3bd9o3v.knj5qynh.oo9gr5id')
						actions = ActionChains(driver)
						actions.move_to_element(comment).perform()
						comment = comment.text
						if len(str(comment)) > 1:
							if not (comment in allCom):
								allCom.append(comment)
					except Exception as inst:
						pass
			except Exception as inst:
				pass
			time.sleep(1)
	def getPageCommets(self,url,saveFileName = 'temp',maxScrol=50):
		driver = runChromeDriver(self.chromeAddress)
		driver = login(self.username,self.password,driver)
		driver.get(url)
		allCommets = []
		ind = -1
		self.mainProcess(driver,saveFileName,maxScrol,allCommets,ind)



if __name__ == "__main__":
	# your Info
	chromeDriverAddress = '' # for example : 'C:\\chromedriver.exe'
	username = '' # your facebook username or email or phone number
	password = '' # your password
	pageUrl = '' # for example : 'https://www.facebook.com/Rudaw.net'


	maxScrol = 150 # max scroll is because of that you need to scroll down to load more comments.
    
	saveFileName = '' # filename that you want to save the comments in it.


	fbc = FacebookComments(chromeDriverAddress,username,password)
	fbc.getPageCommets(pageUrl,saveFileName=saveFileName,maxScrol=maxScrol)
