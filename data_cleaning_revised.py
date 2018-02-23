#%% Preparation ###
import os
#os.chdir('D:\\Documents\\GitHub\\real-estate\\')
os.chdir('C:\\Users\\master\\Desktop\\realestate')
### os.getcwd()
import pandas as pd

final_df = pd.DataFrame()


#%% Data cleaning ###
### Transaction ###
for yr in range(2016,2017): # by year

    for mt in range(1,13): # by month
        if mt < 10:
           month = '0' + str(mt)
        else:
           month = str(mt)

        for sido in ['서울특별시']:#, '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']: # 시도별로

            ### Read data ###
            excel_name = '.\\data\\'+str(yr)+'년_'+month+'월_전국_실거래가_아파트(매매).xls'
            dfi = pd.read_excel(excel_name, sheetname=sido, header=7) # df of input
            dfo = pd.DataFrame(index=dfi.index) # df for output in same index as input

            # for i, row in realestate.iterrows():
            #    realestate.loc[i,'시군구']=realestate.loc[i,'시군구'].lstrip()
            tmp_add = dfi.loc[:,'시군구'].str.lstrip() #'시군구'는 string이 띄어쓰기로 구분되어 있는데, 왼쪽에 불필요한 white space도 있으므로 이를 떼어준다.


#% Create variable of interest ###
            dfo['year'] = yr # year
            dfo['month'] = mt # month
            dfo['sido'] = sido
            dfo['sigungu'] = "" # empty column
            dfo['dong'] = "" # empty column
            add_list = tmp_add.str.split().astype(list)  # address list: 행정구역을 띄어쓰기(" ")를 기준으로 list로 바꿔준다


#% Stripping admin to sido, sigungu, and dong ###
            if sido == '세종특별자치시': # 세종시의 경우에는 시도: 세종특별자치시, 시군구: 세종시, 읍면동: X동으로 들어갈 예정.
                dfo.loc[:,'sigungu'] = '세종시' # sigungu에는 '세종시'라고 일괄입력해준다.
                dfo.loc[:,'dong'] = add_list[:].str[1] #세종특별자치시에 읍면동은 2번째 element에 적혀있으므로 dong에는 list[1]를 넣어준다
            else:
                tmp_bl1 = add_list[:].str[1].str[-1]=='시' #list 내 2번째 elt의 마지막 글자가 '시'인 경우 True(=1)
                tmp_bl2 = add_list[:].str[1].str[-1]=='군' #list 내 2번째 elt의 마지막 글자가 '군'인 경우 True(=1)
                tmp_bl3 = add_list[:].str[1].str[-1]=='구' #list 내 2번째 elt의 마지막 글자가 '구'인 경우 True(=1)
                dfo.loc[tmp_bl1|tmp_bl2|tmp_bl3,'sigungu'] = add_list[:].str[1] # 시군구에 list[1]를 넣어준다
                tmp_bl = add_list[:].str[2].str[-1] == '구' # list 내 3번째 elt의 마지막 글자가 '구'라면 (ex. 경기도 성남시 분당구 수내동)
                dfo.loc[tmp_bl,'dong'] = add_list[:].str[3] # list 내 4번째 elt를 읍면동에 넣어준다
                dfo.loc[~tmp_bl,'dong'] = add_list[:].str[2] # list 내 3번째 글자의 마지막 글자가 '구'가 아니라면 (ex. 경기도 부천시 원미동) list 내 3번째 elt를 읍면동에 넣어준다

#% Create Contract date Fixed Effects ###            
#            realestate['contract_fe']=realestate['계약일'] # 계약일로부터 FE를 만들기 위함
#            realestate['contract_fe']=realestate['contract_fe'].replace('1~10','0') # 초순
#            realestate['contract_fe']=realestate['contract_fe'].replace('11~20','1') # 중순
#            realestate['contract_fe']=realestate['contract_fe'].replace('21~28','2') # 하순_1 (2월)
#            realestate['contract_fe']=realestate['contract_fe'].replace('21~29','2') # 하순_2 (2월_윤년)
#            realestate['contract_fe']=realestate['contract_fe'].replace('21~30','2') # 하순_3
#            realestate['contract_fe']=realestate['contract_fe'].replace('21~31','2') # 하순_4
#            realestate['contract_fe']=realestate['contract_fe'].astype(int) # FE가 문자열로 되어있으므로 바꿔준다

#% 'destring' 거래금액(만원) ###
            tmp_price = dfi['거래금액(만원)'].str.replace(",","") # 쉼표를 뗀다
            dfo['admin'] = tmp_add
            dfo['price'] = tmp_price.astype(int) # 숫자로 바꿔준다

#$ add variables ###
            dfo['area'] = dfi['전용면적(㎡)']
            dfo['floor'] = dfi['층']
            dfo['const_yr'] = dfi['건축년도']
            dfo['town'] = dfi['단지명']
            dfo['address_code'] = dfi['번지']
            dfo['road'] = dfi['도로명'] # 계약일 제외됨
#$ append them ###
            final_df = pd.concat([final_df,dfo], ignore_index=True)
            
#%% Admincode ###
txt_name = 'admin_code_ansi.txt'
admincode = pd.read_csv(open(txt_name,newline='\n'),sep='\t', encoding='utf-8')
admincode = admincode[admincode.폐지여부 == '존재']
admincode.rename(columns={'법정동명':'admin','법정동코드':'admin_code'},inplace=True)

#%% Merge ###
merged=pd.merge(final_df, admincode, on='admin', left_index=True)
merged=merged.drop('폐지여부', 1)

#%% Process the dataframe ###
merged['admin_code']=merged['admin_code'].astype(str)
merged['sido_code']=merged['admin_code'].str.slice(stop=2)
merged['sigungu_code']=merged['admin_code'].str.slice(stop=5)
merged['dong_code']=merged['admin_code'].str.slice(stop=8)

# merged=merged[['year','month','admin','admin_code','sido','sido_code','sigungu','sigungu_code','dong','dong_code','town','krw_10k','area_sqmeter','floor','constructed','contract_fe','contract','road_address','address_code']]

#%% Export to excel ###
excelfile='real_estate_'+str(yr)+'.csv' # 파일이름 지정
merged.to_csv(excelfile,index=False,encoding='utf-8')
