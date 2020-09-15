import requests
from bs4 import BeautifulSoup
import pandas as pd
d={}  #main dictionary
itemnumber=0
#Our dataframe which store the data we scraped
df=pd.DataFrame(columns=["movietitle","Imdbrate","locationname","fullLocations","Stars","StarsDetailed","Reviews","criticReviews","numbervotename","moviedate","Genrees","watchingtime","episodenumber","seasonsnumber","Wins","Nomination","harmful","certificate","keywordscontents","companynames","directorname","directornamesDetailed","writersname","writersnameDetailed","producersname","producersnameDetailed","distributors","distributorDetailed","Story Line","Last Season"])
def parantezatici(harmful):
  harmfulc=""
  for i in range(len(harmful)):
    if harmful[i] != '(':
      harmfulc+=harmful[i]
    else:
      break
  return harmfulc
#it will take the series data from 5000 page and one page contains 50 tvseries you can change the page number based on series number you want
for page in range (0,5000):
  # it will be the first page that your scrap start you can change according to what data you want
  if page == 0:
    url="https://www.imdb.com/search/title/?title_type=tv_series&release_date=2000-01-01,2020-12-31&countries=us&start=9001&ref_=adv_nxt" #bunu değiştirdim ilk sayfaya geri koy amk 
  else:
    #next provide you access the other pages
    next=allfilmscontent.find("a",attrs={"class":"lister-page-next next-page"})
    url="https://www.imdb.com"+next["href"]
  #taking the html data and parsing with BeatifulSoup
  r=requests.get(url)
  allfilmscontent=BeautifulSoup(r.content,"lxml")
  films=allfilmscontent.find_all("div",attrs={"class":"lister-item mode-advanced"})
  #all the films in the page will be visited with this loop
  for i in range(0,len(films)):
    
    hrf=films[i].find("div",attrs={"class":"lister-item-content"}).h3.a
    link=hrf["href"]
  #requesting with the headers param for showing the client presence
    headers_param = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    imdburl="https://www.imdb.com" + link
    print(imdburl)
    # imdb series data stored in 8 different pages for per series and it will automatically collect all of them
    detailpage=requests.get(imdburl,headers=headers_param)
    DetailContent=BeautifulSoup(detailpage.content,"lxml")
    
    imdburlParentalGuide=imdburl+"parentalguide"
    detailPageParentalGuide=requests.get(imdburlParentalGuide,headers=headers_param)    
    DetailContentParentalGuide=BeautifulSoup(detailPageParentalGuide.content,"lxml")

    imdburlAwards=imdburl+"awards"
    detailPageAwards=requests.get(imdburlAwards,headers=headers_param)
    DetailContentAwards=BeautifulSoup(detailPageAwards.content,"lxml")

    # imdburlEpisodes=imdburl+"episodes"
    # detailPageEpisodes=requests.get(imdburlEpisodes,headers=headers_param)
    # DetailContentEpisodes=BeautifulSoup(detailPageEpisodes.content,"lxml")

    imdburlLocations=imdburl+"locations"
    detailPageLocations=requests.get(imdburlLocations,headers=headers_param)
    DetailContentLocations=BeautifulSoup(detailPageLocations.content,"lxml")

    imdburlFullcredits=imdburl+"fullcredits"
    detailPageFullCredits=requests.get(imdburlFullcredits,headers=headers_param)
    DetailContentFullcredits=BeautifulSoup(detailPageFullCredits.content,"lxml")

    imdburlKeywords=imdburl+"keywords"
    detailPageKeywords=requests.get(imdburlKeywords,headers=headers_param)
    DetailContentKeywords=BeautifulSoup(detailPageKeywords.content,"lxml")

    imdburlCompanycredits=imdburl+"companycredits"
    detailPageCompanycredits=requests.get(imdburlCompanycredits,headers=headers_param)
    DetailContentCompanycredits=BeautifulSoup(detailPageCompanycredits.content,"lxml")


    try:
      Imdbrate=""
      ratefind=DetailContent.find("div",attrs={"class":"title_block"}).div.select("div:nth-of-type(3) > strong > span")[0] #select birden fazla da döndürebildiği için [0] olarak belirttik.Array Döner
      #div:nth demek ise biz diyoruz ki tüm divleri al bunlardan karşına çıkan 3.al
      #finddan sonra contents dersen   
      if ratefind["itemprop"]=="ratingValue":
        Imdbrate=ratefind.text
      else:
        Imdbrate="NAN"
    except Exception: 
      Imdbrate="NAN"
    print("{} is IMDBrate".format(Imdbrate))
    
    try:
      reviews=DetailContent.find("div",attrs={"class":"titleReviewBarItem titleReviewbarItemBorder"}).find_all("a")#.select("div:nth-of-type(3)")[0].find_all("a")
      print(reviews)
      Reviews=""
      criticReviews=""
      for i in range(0,len(reviews)):
        if "user" in reviews[i].text:
          Reviews = reviews[i].text
        if "critic" in reviews[i].text:
          criticReviews = reviews[i].text
    except Exception:
      Reviews ="NA"
      criticReviews="NA"

    print("{} are our reviews".format(Reviews))
    print("{} are our criticReviews".format(criticReviews))

    # try:
    #   popular=""
    #   popularity=DetailContent.find("div",attrs={"class":"titleReviewBarSubItem"}).select("div:nth-of-type(2)")[0]#.select("div:nth-of-type(3)")[0].find_all("a")
    #   popular=popularity.find("span",attrs={"class":"subText"}).next.strip().replace('\n','').replace('(','').replace(' ','')
    #   popular=float(popular)
    # except Exception:
    #   popular="NA"

    # print("{} are our popularity rate".format(popular))

    try:
      numbervote=""
      numbervote=DetailContent.find("div",attrs={"class":"title_block"}).div.select("a > span")[0]
      if numbervote["itemprop"] =="ratingCount":
        numbervotename=int(numbervote.text.replace(",",""))
      else:
        numbervotename="NA"
    except Exception:
      numbervotename="NA"

    print("{} is our numbervote".format(numbervotename))

    try:
      genreesarray=[]
      genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(3)")[0].h4 #.find_all("a")
      Genrees=""

      if genrees.text=="Genres:":
        genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(3)")[0].find_all("a")
        for i in range(0,len(genrees)):
          genreesarray.append(genrees[i].text.replace(" ","",1))
    except Exception:
      Genrees="NA"
    if Genrees =="":
      Genrees="NA"

    if Genrees=="NA":
      try:
        genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(1)")[0].h4 #.find_all("a")
        if genrees.text=="Genres:":
          Genrees=""
          genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(1)")[0].find_all("a")
          for i in range(0,len(genrees)):
            genreesarray.append(genrees[i].text.replace(" ","",1))
      except Exception:
        Genrees="NA"
      if Genrees =="":
        Genrees="NA"
    
    
    if Genrees=="NA":
      try:
        genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(4)")[0].h4 #.find_all("a")
        if genrees.text=="Genres:":
          Genrees=""
          genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(4)")[0].find_all("a")
          for i in range(0,len(genrees)):
            genreesarray.append(genrees[i].text.replace(" ","",1))
      except Exception:
        Genrees="NA"
      if Genrees =="":
        Genrees="NA"

    
    if Genrees=="NA":
      try:
        genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(2)")[0].h4 #.find_all("a")
        if genrees.text=="Genres:":
          Genrees=""
          genrees=DetailContent.find("div",attrs={"id":"titleStoryLine"}).select("div:nth-of-type(2)")[0].find_all("a")
          for i in range(0,len(genrees)):
            genreesarray.append(genrees[i].text.replace(" ","",1))
      except Exception:
        Genrees="NA"
      if Genrees =="":
        Genrees="NA"
  
    print("{} are our genrees".format(genreesarray))



    #string 
    try:
      movietitle=""

      title=DetailContentParentalGuide.find("h3",attrs={"itemprop":"name"})
      title=title.a.text
      movietitle=title.strip()
    except Exception:
      movietitle="NA"
    print("{} is title name".format(movietitle))
    
    try:
      wins=""
      nomination=""
      awards=""
      awards=DetailContentAwards.find("div",attrs={"class":"desc"}).text
      awardslist=awards.split()
      wins=awardslist[2]
      nomination=awardslist[5]
    except Exception:
      awards="NAN"
      wins="NAN"
      nomination="NAN"

    
    print("{} are our wins number,{} are our nomination".format(wins,nomination))



    # try:
    #   astseason=""

    #   lastyear=DetailContentEpisodes.find("select",attrs={"id":"byYear"}).find_all("option")
    #   astseason=lastyear[len(lastyear)-1]["value"]
    #   if astseason == "-1":
    #     astseason=lastyear[len(lastyear)-2]["value"]
    # except Exception:
    #   astseason="NA"
    # print("{} is our last season".format(astseason))
    
    try:
      lastseason=""
      lastyear=DetailContent.find("div",attrs={"class":"seasons-and-year-nav"}).select("div:nth-of-type(4)")[0].find_all("a")
      lastseason=lastyear[0].text
    except Exception:
      lastseason="NA"
    
    print("{} is our last season".format(lastseason))



    try:
      episodenumber=""
      episode=DetailContent.find_all("span",attrs={"class":"bp_sub_heading"})
      #print(episode)
      if len(episode)==1:
        episodenumber=episode[0].text
      else:
        episodenumber=episode[1].text
    except Exception:
      episodenumber="NA"

    print("{} are our episode number".format(episodenumber))
    
    
    

       
    try:
      locationnumber=0
      locationstext=[]
      fulllocationstext=[]
      locations=DetailContentLocations.find_all("div",attrs={"class":"soda sodavote odd"})
      for i in range(0,len(locations)):
        newplace=locations[i].a.text
        locationslen=len(newplace.split(','))
        if locationslen>2 or locationslen==2:
          locationstext.append(newplace.split(',')[-2].replace(" ","",1))
        fulllocationstext.append(newplace.replace('\n',""))
  

      locations2=DetailContentLocations.find_all("div",attrs={"soda sodavote even"})
      for i in range(0,len(locations2)):
        newplace=locations[i].a.text
        locationslen=len(newplace.split(','))
        if locationslen>2 or locationslen==2:
          locationstext.append(newplace.split(',')[-2].replace(" ","",1))
        fulllocationstext.append(newplace.replace('\n',""))
      
    except Exception:
      locationstext=[]
      fulllocationstext=[]

    print("{} is our location text,{} is our full location text".format(locationstext,fulllocationstext))

  
  
  
    try:
        StarsNames=[]
        StarsDetailed=[]
        content=DetailContentFullcredits.find("table",attrs={"class":"cast_list"}).find_all("tr")
        for i in content:
          tds=i.find_all("td")
          if len(tds)>2:
            actorname=tds[1].a.text.replace("\n","").replace(" ","",1)
            StarsNames.append(actorname)  
            actornameDetailed=tds[3].find_all("a")
            if len(actornameDetailed)==2:
              actornameDetailed2=actorname+ " - "+ actornameDetailed[0].text +" - " + actornameDetailed[1].text
            elif len(actornameDetailed) ==1:
              actornameDetailed2=actorname+ " - "+ actornameDetailed[0].text 
            StarsDetailed.append(actornameDetailed2.replace('\n','').strip())
    except Exception:
        StarsNames=[]
  
    print("{} are stars name".format(StarsNames))






    try:
        #newurl=imdburl+"parentalguide"
        harmfulcontents=[]
        Certificate=[]
        x=DetailContentParentalGuide.find_all("li",attrs={"class":"ipl-inline-list__item"})

        for i in x:
          content=i.a.text
          if ":" not in content and "Certification" not in content  :
            harmfulcontents.append(parantezatici(content.replace(" ","")))
          if ":" in content:
            Certificate.append(content)
        #harmful=harmfulcontents.strip()
    except Exception:
        Certificate=[]
        harmfulcontents=[]
    print("{} is our certificate and {} is our harmful content ".format(Certificate,harmfulcontents))

    try:
        #newurl=imdburl+"parentalguide"
        x=DetailContentKeywords.find_all("td",attrs={"class":"soda sodavote"})
        keywordscontents=[]
        for i in x:
          content=i["data-item-keyword"]
          keywordscontents.append(content.strip())          
        if keywordscontents =="":
          keywordscontents="NA"
    except Exception:
        keywordscontents=[]
    print("{} are keywords ".format(keywordscontents))
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11

    try:
      

      allinfosabouth4=DetailContentCompanycredits.find("div",attrs={"id":"company_credits_content"}).find_all("h4")
      allinfoul=DetailContentCompanycredits.find("div",attrs={"id":"company_credits_content"}).find_all("ul")
      productionCompanies=[]

      for i in range(len(allinfosabouth4)):
          if "Production Companies" in allinfosabouth4[i].text:
            break
      #print(i)
      #print(len(allinfosabouth4)-1)
      if i != len(allinfosabouth4)-1:
        producers=allinfoul[i].find_all("li")
        for i in producers:
          productionCompanies.append(i.a.text.replace("\n",""))
      
      elif i==len(allinfosabouth4)-1:
        if "Production Companies" in allinfosabouth4[i].text:
            directers1=allinfoul[i].find_all("li")
            for i in directers1:
              productionCompanies.append(i.a.text.replace("\n",""))

        else:
          productionCompanies=[]
    except:
      productionCompanies=[]
    print("{} are productionCompanies ".format(productionCompanies))

    
    try:
      allinfosabouth4=DetailContentCompanycredits.find("div",attrs={"id":"company_credits_content"}).find_all("h4")
      allinfoul=DetailContentCompanycredits.find("div",attrs={"id":"company_credits_content"}).find_all("ul")
      distributors=[]
      distributorDetailed=[]
      for k in range(len(allinfosabouth4)):
        if "Distributors" in allinfosabouth4[k].text:
          break
      if k != len(allinfosabouth4)-1 :
        directers=allinfoul[k].find_all("li")
        for i in directers:
          distributors.append(i.a.text.replace("\n",""))
          distributorDetailed.append(i.text.strip())
      elif k==len(allinfosabouth4)-1:
        if "Distributors" in allinfosabouth4[k].text:
            directers=allinfoul[k].find_all("li")
            for i in directers:
              distributors.append(i.a.text.replace("\n",""))
              distributorDetailed.append(i.text.strip())
        else:
          distributors=[]
          distributorDetailed=[]
      totalmedia=0
      if distributors != []:
        totalmedia=len(distributors)

    except Exception:
      distributors=[]
      distributorDetailed=[]

    if distributors==[]:
      totalmedia=0
    print("distributors are {},total distributions {} ".format(distributors,totalmedia))
    print("DistributorsDetailed {}".format(distributorDetailed))


#######################################################33




    try:

      allinfosh4=DetailContentFullcredits.find("div",attrs={"id":"fullcredits_content"}).find_all("h4")
      allinfostable=DetailContentFullcredits.find("div",attrs={"id":"fullcredits_content"}).find_all("table")
      
      producersname=[]
      producersnameDetailed=[]
      for i in range(len(allinfosh4)):
          if "Series Produced by" in allinfosh4[i].text:
            break
      if i != len(allinfosh4)-1:
        producers=allinfostable[i].find_all("tr")
        for i in producers:
          producername=i.a.text.replace("\n","")
          producersname.append(producername)
          allthetds=i.find_all("td")
          producernameDetailed=producername+" : "+allthetds[2].text.strip()
          producersnameDetailed.append(producernameDetailed)
        
      elif i== len(allinfosh4)-1:
        if "Series Produced by" in allinfosh4[i].text:
          producers=allinfostable[i].find_all("tr")
          for i in producers:
            producername=i.a.text.replace("\n","")
            producersname.append(producername)
            allthetds=i.find_all("td")
            producernameDetailed=producername+" : "+allthetds[2].text.strip()
            producersnameDetailed.append(producernameDetailed)
        else:
          producersname=[]
    except Exception:
      producersname=[]
    print("{} are producersname ".format(producersname))
    print("{} producerdetail name is ".format(producersnameDetailed))      
    try:  
      
      allinfosh4=DetailContentFullcredits.find("div",attrs={"id":"fullcredits_content"}).find_all("h4")
      allinfostable=DetailContentFullcredits.find("div",attrs={"id":"fullcredits_content"}).find_all("table")
      directornames=[]
      directornamesDetailed=[]
      for k in range(len(allinfosh4)):
        if "Series Directed by" in allinfosh4[k].text:
          break

      if k != len(allinfosh4)-1:
        directers=allinfostable[k].find_all("tr")
        for i in directers:
          directorname=i.a.text.replace("\n","")
          directornames.append(directorname)
          allthetds=i.find_all("td")
          directornameDetailed=directorname + " : " + allthetds[2].text.strip()
          directornamesDetailed.append(directornameDetailed)
      elif k==len(allinfosh4)-1:
        #print(k)
        if "Series Directed by" in allinfosh4[k].text:
          directers=allinfostable[k].find_all("tr")
          for i in directornames:
            directorname=i.a.text.replace("\n","")
            directornames.append(directorname)
            allthetds=i.find_all("td")
            directornameDetailed=directorname + " : " + allthetds[2].text.strip()
            directornamesDetailed.append(directornameDetailed)
        else:
          directornames=[]
            
    except Exception:
      directornames=[]
    print("director name is {}".format(producersname,directornames))
    print("{} directordetail name is ".format(directornamesDetailed))

########################################################################
    try:
        writersNames=[]
        writersNamesDetailed=[]
        i=0
        for i in range(len(allinfosh4)):
            if "Series Writing Credits" in allinfosh4[i].text:
              break
        if i != len(allinfosh4)-1:
          producers=allinfostable[i].find_all("tr")
          for i in producers:
            writerName=i.a.text.strip()
            writersNames.append(writerName)
            allthetds=i.find_all("td")
            writersnameDetailed=writerName + " : " + allthetds[2].text.strip()
            writersNamesDetailed.append(writersnameDetailed)

        elif i== len(allinfosh4)-1:
          if "Series Writing Credits" in allinfosh4[i].text:
            producers=allinfostable[i].find_all("tr")
            for i in producers:
              writerName=i.a.text.strip()
              writersNames.append(writerName)
              allthetds=i.find_all("td")
              writersnameDetailed=writerName + " : " + allthetds[2].text.strip()
              writersNamesDetailed.append(writersnameDetailed)      
              writersNames=[]
            
    except Exception:
        writersNames=[]
    print("{} are our writers ".format(writersNames))
    print("{} are our writersDetailed".format(writersNamesDetailed))

#############################################################3


    try:
      watchingtime=""
      watchingtime=DetailContent.find("time").text.strip()
    except Exception:
      watchingtime="NA"

    print("{} are our watching time".format(watchingtime))




    try:
      seasonsnumber=""
      seasons=DetailContent.find("div",attrs={"class":"seasons-and-year-nav"}).select("div:nth-of-type(3)")[0].find_all("a")
      seasonsnumber=seasons[0].text
    except Exception:
      seasonsnumber="NA"

    print("{} are our seansons number".format(seasonsnumber))



    try:

      moviedate=DetailContentParentalGuide.find("span",attrs={"class":"nobr"}).text
      moviedate=moviedate.strip()
      moviedate=moviedate.replace("\r\n","")
    except Exception:
      moviedate="NA"
    print("{} is moviedate".format(moviedate))
    

    try:
      storyline=""
      storylinefinding=DetailContent.find("div",attrs={"class":"inline canwrap"}).p.span.text
      storyline=storylinefinding
    except Exception:
      storyline="NA"
    
    print("{} is storyline.".format(storyline))

    d[itemnumber] = {}
    d[itemnumber]['movietitle']=movietitle
    d[itemnumber]['Imdbrate'] = Imdbrate
    d[itemnumber]['locationname'] = locationstext
    d[itemnumber]['fullLocations']=fulllocationstext
    d[itemnumber]['Stars'] = StarsNames
    d[itemnumber]['StarsDetailed']=StarsDetailed
    d[itemnumber]['Reviews'] = Reviews #buraya da critic reviews geliyor onu düzelt !
    d[itemnumber]['criticReviews'] = criticReviews
    d[itemnumber]['numbervotename'] = numbervotename
    d[itemnumber]['moviedate'] = moviedate
    d[itemnumber]['Genrees'] = genreesarray
    d[itemnumber]['watchingtime'] = watchingtime
    d[itemnumber]['episodenumber'] = episodenumber
    d[itemnumber]['seasonsnumber'] = seasonsnumber
    d[itemnumber]['Wins'] = wins
    d[itemnumber]['Nomination']=nomination
    d[itemnumber]['harmful']=harmfulcontents
    print(Certificate)
    d[itemnumber]['certificate']=Certificate
    d[itemnumber]['keywordscontents']=keywordscontents
    d[itemnumber]['companynames']=productionCompanies

    d[itemnumber]['directorname']=directornames
    d[itemnumber]['directornamesDetailed']=directornamesDetailed
    
    d[itemnumber]['writersname']=writersNames
    d[itemnumber]['writersnameDetailed']=writersNamesDetailed


    d[itemnumber]['producersname']=producersname
    d[itemnumber]['producersnameDetailed']=producersnameDetailed

    d[itemnumber]['distributors']=distributors
    d[itemnumber]['distributorDetailed']=distributorDetailed
    #writerı ekle !! 
    d[itemnumber]['Story Line']=storyline
    d[itemnumber]['Last Season']=lastseason
    df=df.append(d[itemnumber],ignore_index=True)
    itemnumber +=1
    print("Item completed {} page is {}".format(itemnumber,page))
    print("*"*200)

from google.colab import files
df.to_excel('1956ImdbUS180-210.xlsx',encoding='utf-8-sig')
files.download('1956ImdbUS180-210.xlsx')

