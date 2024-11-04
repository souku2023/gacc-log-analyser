from app.models.log import Log
import time
t= time.time()
l = Log(r"c:\Users\sahas\Downloads\136_cc_log_m_29180_2024_10_06_00_53_06\141_cc_log_m_29143_2024_10_26_02_56_26")
print(time.time() - t)
print(l.mission_info_df.to_csv(), file=open('t.csv', 'w'))