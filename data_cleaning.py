
# coding: utf-8

# In[ ]:


### Preparation ###
### import os
### os.chdir('C:\\Users\\master\\Desktop\\realestate')
### os.getcwd()
import pandas as pd


# In[ ]:


### Data cleaning ###
### Transaction ###
for yr in ['2016']: # by year
    for month in ['12','11','10','09','08','07','06','05','04','03','02','01']: # by month
        for sido in ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']: # 시도별로
### Read data ###
            excel_name=yr+'년_'+month+'월_전국_실거래가_아파트(매매).xls'
            realestate=pd.read_excel(excel_name, sheetname=sido,header=7)
            for i, row in realestate.iterrows():
                realestate.loc[i,'시군구']=realestate.loc[i,'시군구'].lstrip()
### Create variable of interest ###
            realestate['sido']="" # empty column
            realestate['sigungu']="" # empty column
            realestate['dong']="" # empty column
            realestate['year']=yr # year
            realestate['month']=month # month
            realestate['year']=realestate['year'].astype(int)
            realestate['month']=realestate['month'].astype(int)
            realestate['법정동명']=realestate['시군구']
### Stripping admin to sido, sigungu, and dong ###
            realestate['시군구']=realestate['시군구'].str.split().astype(list) # 행정구역을 띄어쓰기(" ")를 기준으로 list로 바꿔준다
            if sido=='세종특별자치시':
                for i, row in realestate.iterrows():
                    realestate.loc[i,'sido']=realestate.loc[i,'시군구'][0] # 시도에 list[0]를 넣어준다
                    realestate.loc[i,'sigungu']='세종시' # 시군구에 element를 넣어준다
                    realestate.loc[i,'dong']=realestate.loc[i,'시군구'][1] # 읍면동에 list[1]를 넣어준다
            else:
                for i, row in realestate.iterrows():
                    if realestate.loc[i,'시군구'][0][-1]=='시' or realestate.loc[i,'시군구'][0][-1]=='도': # list[0]가 시도일 경우 (always)
                        realestate.loc[i,'sido']=realestate.loc[i,'시군구'][0] # 시도에 list[0]를 넣어준다
                    if realestate.loc[i,'시군구'][1][-1]=='시' or realestate.loc[i,'시군구'][1][-1]=='군' or realestate.loc[i,'시군구'][1][-1]=='구': #list[1]가 시군구일 경우
                        realestate.loc[i,'sigungu']=realestate.loc[i,'시군구'][1] # 시군구에 list[1]를 넣어준다
                    if realestate.loc[i,'시군구'][2][-1]=='구': # list[2]가 '구'라면
                        realestate.loc[i,'dong']=realestate.loc[i,'시군구'][3] #list[3]을 읍면동에 넣어준다.
                    else: #list[2]가 '구'가 아닐 경우
                        realestate.loc[i,'dong']=realestate.loc[i,'시군구'][2] #읍면동에 list[2]를 넣어준다
### Create Contract date Fixed Effects ###            
            realestate['contract_fe']=realestate['계약일'] # 계약일로부터 FE를 만들기 위함
            realestate['contract_fe']=realestate['contract_fe'].replace('1~10','0') # 초순
            realestate['contract_fe']=realestate['contract_fe'].replace('11~20','1') # 중순
            realestate['contract_fe']=realestate['contract_fe'].replace('21~28','2') # 하순_1 (2월)
            realestate['contract_fe']=realestate['contract_fe'].replace('21~29','2') # 하순_2 (2월_윤년)
            realestate['contract_fe']=realestate['contract_fe'].replace('21~30','2') # 하순_3
            realestate['contract_fe']=realestate['contract_fe'].replace('21~31','2') # 하순_4
            realestate['contract_fe']=realestate['contract_fe'].astype(int) # FE가 문자열로 되어있으므로 바꿔준다
### 'destring' krw_10k ###
            realestate['거래금액(만원)']=realestate['거래금액(만원)'].str.replace(",","") # 쉼표를 뗀다
            realestate['거래금액(만원)']=realestate['거래금액(만원)'].astype(int) # 숫자로 바꿔준다
### Saving in a memory by sido ###
            if sido=='서울특별시':
                서울=realestate
            elif sido=='부산광역시':
                부산=realestate
            elif sido=='대구광역시':
                대구=realestate
            elif sido=='인천광역시':
                인천=realestate
            elif sido=='광주광역시':
                광주=realestate
            elif sido=='대전광역시':
                대전=realestate
            elif sido=='울산광역시':
                울산=realestate
            elif sido=='세종특별자치시':
                세종=realestate
            elif sido=='경기도':
                경기=realestate
            elif sido=='강원도':
                강원=realestate
            elif sido=='충청북도':
                충북=realestate
            elif sido=='충청남도':
                충남=realestate
            elif sido=='전라북도':
                전북=realestate
            elif sido=='전라남도':
                전남=realestate
            elif sido=='경상북도':
                경북=realestate
            elif sido=='경상남도':
                경남=realestate
            elif sido=='제주특별자치도':
                제주=realestate
### Create an empty dataframe and append everything ###
        null_df = pd.DataFrame()
        if realestate.loc[0,'year']>=2012:
            monthly = null_df.append([서울, 부산, 대구, 인천, 광주, 대전, 울산, 세종, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주])
        else:
            monthly = null_df.append([서울, 부산, 대구, 인천, 광주, 대전, 울산, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주])
### Saving in a memory by month ###
        if month=='12':
            december=monthly
        elif month=='11':
            november=monthly
        elif month=='10':
            october=monthly
        elif month=='09':
            september=monthly
        elif month=='08':
            august=monthly
        elif month=='07':
            july=monthly
        elif month=='06':
            june=monthly
        elif month=='05':
            may=monthly
        elif month=='04':
            april=monthly
        elif month=='03':
            march=monthly
        elif month=='02':
            february=monthly
        elif month=='01':
            january=monthly
### Create an empty dataframe and append by month ###
    null_df1 = pd.DataFrame()
    yearly = null_df1.append([january, february, march, april, may, june, july, august, september, october, november, december])
### Admincode ###
txt_name='법정동코드.txt'
admincode=pd.read_csv(open(txt_name,newline='\n'),sep='\t', encoding='utf-8')
admincode=admincode[admincode.폐지여부 == '존재']
### Merge ###
merged=pd.merge(yearly, admincode,on='법정동명',left_index=True)
merged=merged.drop('폐지여부',1)
### Process the dataframe ###
merged.rename(columns={'법정동명':'admin','전용면적(㎡)':'area_sqmeter','거래금액(만원)':'krw_10k','번지':'address_code','단지명':'town','계약일':'contract','층':'floor','건축년도':'constructed','도로명':'road_address','법정동코드':'admin_code'},inplace=True)
merged['admin_code']=merged['admin_code'].astype(str)
merged['sido_code']=merged['admin_code'].str.slice(stop=2)
merged['sigungu_code']=merged['admin_code'].str.slice(stop=5)
merged['dong_code']=merged['admin_code'].str.slice(stop=8)
merged=merged[['year','month','admin','admin_code','sido','sido_code','sigungu','sigungu_code','dong','dong_code','town','krw_10k','area_sqmeter','floor','constructed','contract_fe','contract','road_address','address_code']]
### Export to excel ###
excelfile='real_estate_'+yr+'.csv' # 파일이름 지정
merged.to_csv(excelfile,index=False,encoding='utf-8')
