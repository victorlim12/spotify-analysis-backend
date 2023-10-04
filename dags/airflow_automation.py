
import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(2023,1,29),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}

def run_etl():
    from models.user import Account 
    from models.token import Token  
    from models.profile import Profile
    from etl.Load_psql import Load_PSQL
    from utils.utils import refresh_access_token

    from app import db
    try:
        # Query the database to get a list of usernames
        usernames = db.session.query(Account.username).all()

        # Loop through the usernames and perform ETL for each one
        for username in usernames:
            token = db.session.query(Token).filter_by(username=username).first()
            profile = db.session.query(Profile).filter_by(username=username).first()

            if token and profile:
                access_token = refresh_access_token(token)
                response = Load_PSQL(access_token, profile.spotifyid)

                if response.json["code"] == 200:
                    print(f'ETL completed for username: {username}')
                else:
                    print(f'ETL failed for username: {username}, error: {response.json["message"]}')

        return {'message': 'ETL completed for all users', 'code': 200}
    except Exception as e:
        return {'message': f'error found: {e}', 'code': 404}

dag = DAG(
    'spotify_final_dag',
    default_args=default_args,
    description='Spotify ETL process 1-min',
    schedule_interval=dt.timedelta(minutes=50),
)

with dag:    
    run_etl_job = PythonOperator(
        task_id='spotify_etl_final',
        python_callable=run_etl,
        dag=dag,
    )

    run_etl_job