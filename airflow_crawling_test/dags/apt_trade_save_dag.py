from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
import xml.etree.ElementTree as ET
import pendulum
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic' 
plt.rcParams['axes.unicode_minus'] = False

kst = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1, tzinfo=kst),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id='apt_trade_to_csv',
    default_args=default_args,
    description='아파트 실거래가 API를 통해 데이터를 수집하고 CSV로 저장',
    schedule_interval='*/1 * * * *', # 매 1분마다 실행
    catchup=False,
    tags=['real_estate'],
)

load_dotenv()
DECODE_KEY = os.getenv('DECODE_KEY')

def get_and_save_apt_data(**context):
    """
    국토교통부 아파트 실거래 데이터를 호출하여 csv로 저장하는 함수
    """
    def get_apt_data_by_month(lawd_cd, deal_ym, num_rows=100):
        url = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
        params = {
            "serviceKey": DECODE_KEY,
            "LAWD_CD": lawd_cd,
            "DEAL_YMD": deal_ym,
            "numOfRows": str(num_rows),
            "pageNo": "1"
        }

        try:
            res = requests.get(url, params=params, timeout=10)
            res.encoding = 'utf-8'
            root = ET.fromstring(res.text)
            items = root.find('.//items')

            if items is None:
                return []

            return [
                {
                    "계약년도": item.findtext('dealYear'),
                    "계약월": item.findtext('dealMonth'),
                    "계약일": item.findtext('dealDay'),
                    "아파트": item.findtext('aptNm'),
                    "거래금액": item.findtext('dealAmount'),
                    "면적": item.findtext('excluUseAr'),
                    "층": item.findtext('floor')
                }
                for item in items.findall('item')
            ]
        
        except Exception as e:
            print(e)
            return []

    # 현재 날짜의 전월을 기준으로 조회
    now = datetime.now(tz=kst)
    prev_month = now - relativedelta(months=1)
    ym = prev_month.strftime('%Y%m')
    lawd_cd = "11545"

    data = get_apt_data_by_month(lawd_cd, ym)
    if not data:
        print("데이터 없음")
        return "No data"

    df = pd.DataFrame(data)
    df['거래금액(만원)'] = pd.to_numeric(df['거래금액'].str.replace(",", ""), errors='coerce')
    df['계약일자'] = pd.to_datetime(
        df['계약년도'] + '-' + df['계약월'].str.zfill(2) + '-' + df['계약일'].str.zfill(2), errors='coerce'
    )
    df = df[['계약일자', '아파트', '거래금액(만원)', '면적', '층']]

    # 저장 경로 설정
    output_dir = os.path.join(os.environ["AIRFLOW_HOME"], "output")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"apt_trade_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"파일 저장 완료: {filepath}/{filename}")
    return filepath

save_task = PythonOperator(
    task_id='save_apt_trade_to_csv',
    python_callable=get_and_save_apt_data,
    provide_context=True,
    dag=dag,
)
