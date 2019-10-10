from bs4 import BeautifulSoup
import requests
import re
import os


def get_varient(varient):
    varients_url = {}
    for i in range(len(varient)):
        m= re.search(r'<a href="(\S+)"',str(varient[i].a))
        varients_url[varient[i].a.text]= "https://www.carwale.com"+ m.group(1)
    return varients_url

def one_brand(varients_url):
    all_brand={}
    brand_type_version_url = list(varients_url.values())
    brand_names = list(varients_url.keys())
    for i in range(len(brand_names)):
    #for i in range(1):             # ??????????????????????????????????????????????
        all_brand[brand_names[i]] = one_car(brand_type_version_url[i])
    return all_brand

def one_car(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    gen_key_spec = {"key Specifications":gen_data(soup)} #getting key specifications
    specs= soup.findAll("table",{"class":"specs"})
    
    detailed_spec = scrape_spec_features(specs) #detailed specifications
    #return (gen_key_spec.update(detailed_spec))
    res = {**gen_key_spec, **detailed_spec} 
    return res 

def scrape_spec_features(specs):
    final={}
    specifications={}
    for i in range(4):
        specs_tr=specs[i].findAll("tr")
        temp={}
        for j in range(len(specs_tr)):
            specs_td=specs_tr[j].findAll("td")
            temp[specs_td[0].text]=specs_td[1].text
        specifications[specs[i].th.text]=temp
    features={}
    list(range(4,len(specs)))
    for i in range(4,len(specs)):
        temp={}
        specs_tr=specs[i].findAll("tr")
        #print(i,"      ",specs_tr)
        for j in range(1,len(specs_tr)):
            specs_td = specs_tr[j].findAll("td")
            temp[specs_td[0].text]=specs_td[1].text
        
        features[specs_tr[0].text]=temp
        
    final["spec"]=specifications
    final["fea"]=features
    return final



def gen_data(soup):
    temp={}
    specs = soup.findAll("tr",{"class":""})
    for i in range(5):
        temp[specs[i].th.text]= specs[i].td.span.text
    return temp# -*- coding: utf-8 -*-
def mkdir(relative_path):
    try:
        os.mkdir("/home/arch/project/"+relative_path)
    except FileExistsError:
        pass#print("already exits")
    except FileNotFoundError:
        print("check path of directory again")

def open_file(file_name,mode,relative_path="/home/arch/project/"):
    f=open(relative_path+file_name,mode)
    return f


# %%
final={}
#%%
for i in range(37):
#for i in [37]:

    f = open("/home/arch/project/model_name_url_{}.txt".format(i),"r")
    l = f.readlines()
    loop_two={}
            
    #l[0] #1st element in the maruthi s-press find varients_url 1st
    for j in range(len(l)):
    #for j in range(1):
            
        try:
            response = requests.get(l[j][:-1])
            soup = BeautifulSoup(response.content,"html.parser")

            # %%
            general_data=gen_data(soup)#general data of a model 
            only_for_one={"gen":general_data}
            
            # %%
            varient = soup.findAll("div",{"class":"variant__name"})
            varients_url = get_varient(varient)
            #brand_type_version_url = list(varients_url.values())
            # 
            # %%
            only_for_one["detail"]=one_brand(varients_url)
            m = re.search('.com/(\S+)-cars/(\S+)/\n',l[j])
            #print(all_brand)
            loop_two[m.group(2)]=only_for_one
            fp=open("/home/arch/project/temp/final_back_up{}.txt".format(i),"w+")    
            print(loop_two,file =fp)
            print(i,j)
            fp.close()
        except :
            print("failed",i,j)
    m = re.search('.com/(\S+)-cars/(\S+)/\n',l[j])
    final[m.group(1)]=loop_two   
#%%     
end = open("/home/arch/project/final1.txt","w+")
print(final,file = end)    
#%%

