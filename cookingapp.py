import streamlit as st
import pandas as pd

st.set_page_config(page_title="스마트 요리 앱", layout="wide")

st.title("🍳 내 손안의 스마트 요리 백과")
st.write("요리를 검색하고, 냉장고 상황에 맞춰 완벽한 레시피를 계산해 보세요!")

@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1_EurVIAhRkQ_7oV_tOgGlfQ2Bt73LORiIZHdiYb9_C0/edit"
    excel_url = sheet_url.split("/edit")[0] + "/export?format=xlsx"
    
    # 데이터 불러오기
    df_ing = pd.read_excel(excel_url, sheet_name=0)
    df_recipe = pd.read_excel(excel_url, sheet_name="recipe") # 시트 이름 주의!
    
    # 컬럼명 공백 제거 (매우 중요)
    df_ing.columns = df_ing.columns.str.strip()
    df_recipe.columns = df_recipe.columns.str.strip()
    
    # 재료 시트 방어벽
    if "대체재" not in df_ing.columns: df_ing["대체재"] = "-"
    if "생략여부" not in df_ing.columns: df_ing["생략여부"] = "-"
        
    return df_ing, df_recipe

# 데이터 로드
df_ing, df_recipe = load_data()

# 5. 검색창
selected_list = st.multiselect(
    "🔍 어떤 요리를 찾으시나요?", 
    df_ing["요리명"].dropna().unique(),
    max_selections=1
)

if selected_list:
    selected_dish = selected_list[0]
    st.subheader(f"🥘 [{selected_dish}] 요리 준비")
    
    dish_df = df_ing[df_ing["요리명"] == selected_dish].copy()
    
    # 6. 인분 수 조절
    portions = st.slider("몇 인분을 만드시겠어요?", 1.0, 20.0, 1.0, 0.5)
    dish_df["최종 필요량"] = dish_df["1인분_기준량"] * portions
    
    # 7. 재료 출력
    st.markdown(f"#### 🛒 {portions}인분 재료 및 대체 팁")
    st.dataframe(dish_df[["재료명", "최종 필요량", "단위", "대체재", "생략여부"]], use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 8. 레시피 출력 (필터링 로직 수정)
    st.markdown("#### 👨‍🍳 조리 순서")
    recipe_row = df_recipe[df_recipe["요리명"] == selected_dish]
    
    if not recipe_row.empty:
        st.info(recipe_row["조리순서"].iloc[0])
    else:
        st.warning("이 요리의 레시피는 아직 등록되지 않았습니다.")
else:
    st.info("👆 위 검색창에서 요리 이름을 입력해 주세요!")