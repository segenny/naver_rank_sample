import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os

st.set_page_config(
    page_title="네이버 순위 추적",
    page_icon="🔢 ",
)

def _max_width_():
    max_width_str = f"max-width: 2400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

def getNRank(keyword, my_mall, max_page=5, find_all='y'):

    ################################################################
    max_page = 5    # 한 페이지에 40 상품
    find_all = 'y'    # y 하면 max_page 내 모든 순위 찾음, n 하면 1위만 찾음
    ################################################################

    header_text = """
    :authority: search.shopping.naver.com
    :method: GET
    :path: /api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query=%EC%BA%A0%ED%95%91&origQuery=%EC%BA%A0%ED%95%91&iq=&eq=&xq=
    :scheme: https
    accept: application/json, text/plain, */*
    accept-encoding: gzip, deflate, br
    accept-language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
    cookie: NNB=MKSM4LCBMKAWE; NID_AUT=e0R81dA4Sh7Eo65/9rQR8igAPl8JuyeDdUk+3kYdMjcnRqK4tCoo5gxw4RSysbEE; NID_JKL=yqMXwyK13DRlsVbP83VO6eAf9INcex7NBg6Iy0dceoU=; ASID=dc4cab8600000180ca6b065f00000055; _ga=GA1.2.831873633.1653898929; autocomplete=use; AD_SHP_BID=30; nx_ssl=2; BMR=s=1666748073994&r=https%3A%2F%2Fn.news.naver.com%2Fmnews%2Farticle%2F348%2F0000066820&r2=https%3A%2F%2Fnews.naver.com%2Fmain%2Flist.naver%3Fmode%3DLPOD%26mid%3Dsec%26oid%3D348; page_uid=h1AJIwp0J1ZssThhT2Rsssssshh-127596; NID_SES=AAABgifEYCFjkFLqOkLuf6U7feibgIulykeqsHtCem+CdUhhqPm5COa8o7mv+Q03I6JsEIeYPC/03szIFinp4OQgSWqyZvHl8Hv+bGU1YL1Jojh9XQMMHoppAvzzLLrKB/eyI1A6oQ0p8zGaRWaDZsJTLN9kOgfmYm3ZgCNl6NHwY7scrFN7+MT56O32J2qaMx2cZ5qsMz9bB2LvGm7SRNX6qsHJDspRKMfDu9jPJBENwKzIf4R+eqBq09BOx4GtHSYQgJooR+YwNlgNOgFvX9dXgn9Hetti8keAWjxjMX2xC7rtH6GRZZiSP9IK8a4KmZZFUcF94uz8X7EsWdc4Xcs/ocSvygf2D8FNTj5/r83a/gcmBvtBfn5q8jVqlLAsmNQRmQWlXw7wPM4RorodSfiGtm55BgcTB8A8Z/3Ok+YfcNwNKtlVWPajAJN9qWqc3a/ZTSOBIrmrpbugFdIEvJuLhmlxsXk8wCjBF2o1kdHMH4KkZbIjPCNSMX3FAEB+lsApPwWyGHRcuIsE25BVzcgUiQQ=; spage_uid=h1AJIwp0J1ZssThhT2Rsssssshh-127596; sus_val=IdvV29CgB15ZhZuJtvA+XI5D
    logic: PART
    referer: https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery=%EC%BA%A0%ED%95%91&pagingIndex=2&pagingSize=40&productSet=total&query=%EC%BA%A0%ED%95%91&sort=rel&timestamp=&viewType=list
    sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "macOS"
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-origin
    user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
    """
    def get_headers_as_dict(headers: str) -> dict:
        dic = {}
        for line in headers.split("\n"):
            if line.startswith(("GET", "POST")):
                continue
            point_index = line.find(":")
            dic[line[:point_index].strip()] = line[point_index+1:].strip()
        del dic['']
        return dic

    data = get_headers_as_dict(header_text)

    api_url = f'https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query={keyword}&origQuery={keyword}&iq=&eq=&xq='
    result_json = requests.get(api_url, headers=data).json()

    if find_all == 'y':
        page = 1
        while page <= max_page:
                try:
                    st.write(page, '페이지 40개에서 찾는 중..')
                    api_url = f'https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex={page}&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query={keyword}&origQuery={keyword}&iq=&eq=&xq='
                    result_json = requests.get(api_url, headers=data).json()
                    for i in range(40):
                        try:
                            if my_mall in str(result_json['shoppingResult']['products'][i]['lowMallList']):
                                st.write(my_mall, str(result_json['shoppingResult']['products'][i]['rank']) + '위', result_json['shoppingResult']['products'][i]['productTitle'])
                                상태 = '찾음'
                                break
                            else:
                                pass
                        except:
                            break
                    page += 1
                except:
                    st.write(page, '페이지 없음')
                    break
        st.write('완료')
    else:
        page = 1
        상태 = '찾는중'
        while page <= max_page:
            if 상태 == '찾는중':
                try:
                    st.write(page, '페이지 40개에서 찾는 중..')
                    api_url = f'https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex={page}&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query={keyword}&origQuery={keyword}&iq=&eq=&xq='
                    result_json = requests.get(api_url, headers=data).json()
                    for i in range(40):
                        try:
                            if my_mall in str(result_json['shoppingResult']['products'][i]['lowMallList']):
                                st.write(my_mall, str(result_json['shoppingResult']['products'][i]['rank']) + '위', result_json['shoppingResult']['products'][i]['productTitle'])
                                상태 = '찾음'
                                break
                            else:
                                pass
                        except:
                            break
                    page += 1
                except:
                    st.write(page, '페이지 없음')
                    break
            else:
                break
        st.write('완료')

_max_width_()

st.title("🔢 네이버 순위 추적")

검색키워드 = st.text_input('검색키워드를 입력 해 주세요', placeholder='예) 캠핑')
if 검색키워드:
    st.write('검색 키워드 :', 검색키워드)


회사명 = st.text_input('회사명을 입력 해 주세요', placeholder='예) 회사명')
if 회사명:
    st.write('회사 : ', 회사명)

#st.markdown("")
#with st.form(key="my_form"):
#    submit_button = st.form_submit_button(label="✨ Get me the data!")

if 검색키워드 and 회사명: 
    st.markdown("## 결과") 
    getNRank(검색키워드, 회사명)
