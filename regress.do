clear all
set more off
set matsize 5000, perm
set maxvar 32767, perm
global dta "C:\Users\master\Desktop\realestate\"
cd $dta

import delimited C:\Users\master\Desktop\realestate\real_estate_2016.csv, encoding(UTF-8)

****** renaming variables - to be reflected at Python level ******
drop contract
rename (krw_10k area_sqmeter constructed contract_fe)(price area yr_const contract)
label variable price in_10k_KRW
label variable area square_meter
label variable yr_const year_the_building_was_constructed
label variable contract contract_n
label define contract_n 0 초순 1 중순 2 하순
label value contract contract_n
labmask sido_code, val(sido)
labmask sigungu_code, val(sigungu)
labmask dong_code, val(dong)
drop sido sigungu dong
rename (sido_code sigungu_code dong_code) (sido sigungu dong)
******

****** 시도/시군구/읍면동을 뺀 나머지 주소로 저장하고 싶다면 ******
encode admin, gen(full_admin)
gen fulla = admin + " " + town + " " + address_code
egen remain = group(fulla)
gen remainadd = town + " " + address_code
labmask remain, val(remainadd)
drop admin town road_address address_code fulla remainadd
save real_estate_2016_1.dta, replace
******

****** full_address 형식으로 저장하고 싶다면  ******
*encode admin, gen(full_admin)
*gen fulla = admin + " " + town + " " + address_code
*encode fulla, gen(full)
*drop fulla admin town road_address address_code
*label variable full full_address
*save real_estate_2016.dta, replace


****** Regression ******
use real_estate_2016_1.dta, replace

* outreg2을 실행할 때 첫번째 모델은 replace 옵션으로 시작하고, 뒤에 다른 리그레션을 이어 붙일 때는 append 옵션 쓸 것 *
*regress price area floor yr_const i.dong, vce(cluster remain)
*outreg2 using reg1.doc, replace ctitle(cluster_1) keep(price area floor yr_const) addtext(Dong FE, YES, Month FE, NO)
*regress price area floor yr_const i.dong i.month, vce(cluster remain)
*outreg2 using reg1.doc, append ctitle(robust_2) keep(price area floor yr_const) addtext(Dong FE, YES, Month FE, YES)
