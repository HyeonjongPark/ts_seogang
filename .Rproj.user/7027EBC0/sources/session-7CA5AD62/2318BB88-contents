
library(data.table)
library(tidyr)
df0 = read.csv("./data/보건복지부_시군구별 치매현황_20231231.csv", fileEncoding = "euc-kr")
df0 %>% head
fwrite(df0, "./data/prep/df0.csv", bom =TRUE)




colnames(df0)
## views_history
fn_views_history_make1 = function(df , cname) {
  sp_df = spread(df[,c("연도", "시도", "시군구", "성별", "연령별", cname)], key = "연도", value = cname)
  un_df = unite(sp_df, col = cname, colnames(sp_df)[5:ncol(sp_df)], sep = ",")
  un_df$cname = paste0("[", un_df$cname, "]")
  colnames(un_df)[5] = cname  
  
  return(un_df)
}
df0 %>% head
vh_qty = fn_views_history_make1(df0, "노인인구수")
vh_nwt = fn_views_history_make1(df0, "치매환자수")
vh_det = fn_views_history_make1(df0, "치매환자유병률")
vh_iet = fn_views_history_make1(df0, "최경도.환자")
vh_tet = fn_views_history_make1(df0, "경도.환자")
vh_deu = fn_views_history_make1(df0, "중등도.환자")
vh_ieu = fn_views_history_make1(df0, "중증.환자")
vh_teu = fn_views_history_make1(df0, "경도인지장애.환자수")
vh_ecu = fn_views_history_make1(df0, "경도인지장애.환자유병률")


vh_l <- list(vh_qty, vh_nwt, vh_det, vh_iet, vh_tet, vh_deu, vh_ieu, vh_teu, vh_ecu)
df0_summary = purrr::reduce(.x = vh_l, merge, all = T)
df0_summary %>% head

data.table::fwrite(df0_summary, "./data/prep/df0_summary.csv", bom = TRUE)




## 

#변수에 포함된 지역별 녹지비율, 음주율, 흡연율 정도를 분석하면 저희가 의도한 방향성

# df1_smoke = readxl::read_xlsx("./data/데이터정리.xlsx", sheet = "건강_흡연율")
# 
# df1_drink = readxl::read_xlsx("./data/데이터정리.xlsx", sheet = "건강_음주율")
# 
# df1_green = readxl::read_xlsx("./data/데이터정리.xlsx", sheet = "환경_녹지율")
# df1_green = df1_green[-1,]
library(dplyr)
df1 = readxl::read_xlsx("./data/데이터정리.xlsx", sheet = "raw")
df1 %>% head

df1_summary = df1 %>% as.data.frame()

data.table::fwrite(df1_summary, "./data/prep/df1_summary.csv", bom = TRUE)


