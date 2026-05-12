import streamlit as st
import json
import os

# 数据文件路径
DATA_FILE = "dishes.json"

# 读取菜品
def load_dishes():
    if not os.path.exists(DATA_FILE):
        init_data = [
            {"id": 1, "name": "宫保鸡丁", "price": 28.0, "remark": "经典川菜"},
            {"id": 2, "name": "番茄炒蛋", "price": 16.0, "remark": "家常下饭菜"},
            {"id": 3, "name": "红烧肉", "price": 36.0, "remark": "肥而不腻"}
        ]
        save_dishes(init_data)
        return init_data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 保存菜品
def save_dishes(dish_list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dish_list, f, ensure_ascii=False, indent=2)

# ---------------------- 侧边栏导航 ----------------------
st.sidebar.title("📋 点餐系统")
page = st.sidebar.radio("功能页面", ["顾客点餐", "菜品管理(增删改)"])

dishes = load_dishes()

# ====================== 页面1：顾客点餐 ======================
if page == "顾客点餐":
    st.title("🍽️ 在线点餐")
    st.divider()

    if not dishes:
        st.info("暂无菜品，请先到菜品管理添加")
    else:
        for item in dishes:
            st.subheader(f"{item['name']}  ￥{item['price']}")
            st.text(f"备注：{item['remark']}")
            st.divider()

# ====================== 页面2：菜品管理 增删改 ======================
elif page == "菜品管理(增删改)":
    st.title("🔧 菜品管理中心")
    st.divider()

    # 1. 新增菜品
    st.subheader("➕ 添加新菜品")
    with st.form("add_form"):
        new_name = st.text_input("菜品名称")
        new_price = st.number_input("菜品价格", min_value=0.0, step=0.5)
        new_remark = st.text_input("菜品备注/简介")
        submit_add = st.form_submit_button("确认添加")

        if submit_add:
            if new_name.strip() == "":
                st.warning("菜品名称不能为空！")
            else:
                # 生成新ID
                max_id = max([d["id"] for d in dishes], default=0)
                new_id = max_id + 1
                dishes.append({
                    "id": new_id,
                    "name": new_name,
                    "price": new_price,
                    "remark": new_remark
                })
                save_dishes(dishes)
                st.success("✅ 菜品添加成功！")
                st.rerun()

    st.divider()

    # 2. 修改 / 删除 菜品
    st.subheader("✏️ 修改 / 🗑️ 删除菜品")
    if not dishes:
        st.info("暂无菜品可管理")
    else:
        for idx, item in enumerate(dishes):
            with st.expander(f"ID:{item['id']} | {item['name']} ￥{item['price']}"):
                edit_name = st.text_input("修改名称", value=item["name"], key=f"name_{item['id']}")
                edit_price = st.number_input("修改价格", value=item["price"], min_value=0.0, step=0.5, key=f"price_{item['id']}")
                edit_remark = st.text_input("修改备注", value=item["remark"], key=f"remark_{item['id']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"保存修改", key=f"save_{item['id']}"):
                        dishes[idx]["name"] = edit_name
                        dishes[idx]["price"] = edit_price
                        dishes[idx]["remark"] = edit_remark
                        save_dishes(dishes)
                        st.success("修改已保存！")
                        st.rerun()
                with col2:
                    if st.button(f"删除菜品", key=f"del_{item['id']}"):
                        dishes.pop(idx)
                        save_dishes(dishes)
                        st.warning("已删除该菜品")
                        st.rerun()
            st.divider()