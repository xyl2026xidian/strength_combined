import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

st.set_page_config(page_title="强度理论·组合变形", layout="wide")

# ========== 侧边栏 ==========
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/gears.png", width=80)
    st.title("⚙️ 强度理论")
    st.markdown("**组合变形分析系统**")
    st.markdown("---")

    module = st.radio(
        "选择模块",
        ["📖 理论体系",
         "📊 组合变形计算",
         "💪 强度理论对比",
         "🎯 强度理论选择",
         "🏗️ 工程应用",
         "📐 案例分析",
         "🎨 应力云图",
         "🔄 3D可视化",
         "🧪 虚拟实验"]
    )
    st.markdown("---")
    st.caption("💡 交互式学习 | 实时可视化 | 工程实战")

# ========== 材料数据库 ==========
MATERIALS = {
    "Q235钢": {"E": 210, "nu": 0.30, "sigma_s": 235, "sigma_b": 400, "type": "塑性"},
    "45钢": {"E": 210, "nu": 0.28, "sigma_s": 355, "sigma_b": 600, "type": "塑性"},
    "40Cr钢": {"E": 210, "nu": 0.30, "sigma_s": 500, "sigma_b": 750, "type": "塑性"},
    "铝合金": {"E": 70, "nu": 0.33, "sigma_s": 280, "sigma_b": 310, "type": "塑性"},
    "铸铁": {"E": 120, "nu": 0.25, "sigma_s": 200, "sigma_b": 250, "type": "脆性"},
    "混凝土": {"E": 30, "nu": 0.20, "sigma_s": 30, "sigma_b": 30, "type": "脆性"},
}


def set_chinese_font(fig):
    fig.update_layout(
        font=dict(family="SimHei, Microsoft YaHei, Arial Unicode MS, sans-serif")
    )
    return fig


def principal_stresses(sx, sy, txy):
    avg = (sx + sy) / 2
    R = np.sqrt(((sx - sy) / 2) ** 2 + txy ** 2)
    sigma1 = avg + R
    sigma2 = avg - R
    tau_max = R
    return sigma1, sigma2, tau_max


def strength_theories(s1, s2, nu):
    """计算四大强度理论等效应力"""
    sigma_r1 = s1
    sigma_r2 = s1 - nu * s2
    sigma_r3 = s1 - s2
    sigma_r4 = np.sqrt(s1 ** 2 + s2 ** 2 - s1 * s2)
    return [sigma_r1, sigma_r2, sigma_r3, sigma_r4]


# ============================================================
# 1. 理论体系
# ============================================================
if module == "📖 理论体系":
    st.title("📖 四大强度理论 · 理论体系")

    tab1, tab2, tab3, tab4 = st.tabs(["📌 基本概念", "📐 强度理论详解", "📊 组合变形", "🔗 知识图谱"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 📌 什么是强度理论？

            强度理论是判断材料在**复杂应力状态**下是否失效的理论。

            ### 📌 为什么需要强度理论？
            - 实际构件受力复杂，多处于**组合变形**状态
            - 不能直接使用单向拉伸实验数据
            - 需要建立**等效应力**与**许用应力**的对比关系

            ### 📌 材料失效的两种形式
            | 失效形式 | 材料类型 | 特征 |
            |----------|----------|------|
            | **屈服** | 塑性材料 | 出现明显塑性变形 |
            | **断裂** | 脆性材料 | 突然断裂无预兆 |
            """)
        with col2:
            st.markdown("""
            ### 📌 四大强度理论概览

            | 理论 | 名称 | 适用材料 |
            |------|------|----------|
            | 第一 | 最大拉应力理论 | 脆性材料 |
            | 第二 | 最大拉应变理论 | 脆性材料 |
            | 第三 | 最大切应力理论 | 塑性材料 |
            | 第四 | 畸变能理论 | 塑性材料 |

            ### 📌 组合变形
            构件同时承受**两种或以上**基本变形的受力状态。

            **常见类型**：
            - 拉弯组合（偏心拉伸/压缩）
            - 压弯组合
            - 弯扭组合
            - 拉扭组合
            """)

    with tab2:
        st.markdown("""
        ### 📐 四大强度理论详解

        #### 第一强度理论（最大拉应力理论）
        **失效判据**：最大拉应力达到材料的极限应力
        $$\\sigma_{r1} = \\sigma_1 \\leq [\\sigma]$$
        **适用**：脆性材料（铸铁、混凝土、陶瓷）
        **优点**：形式简单
        **缺点**：未考虑其他应力分量的影响

        #### 第二强度理论（最大拉应变理论）
        **失效判据**：最大拉应变达到材料的极限应变
        $$\\sigma_{r2} = \\sigma_1 - \\nu(\\sigma_2 + \\sigma_3) \\leq [\\sigma]$$
        **适用**：脆性材料（受拉为主的工况）
        **优点**：考虑了泊松效应

        #### 第三强度理论（最大切应力理论）
        **失效判据**：最大切应力达到材料的极限切应力
        $$\\sigma_{r3} = \\sigma_1 - \\sigma_3 \\leq [\\sigma]$$
        **适用**：塑性材料（低碳钢、铝合金）
        **优点**：偏于安全
        **缺点**：未考虑中间主应力影响

        #### 第四强度理论（畸变能理论）
        **失效判据**：畸变能达到材料的极限值
        $$\\sigma_{r4} = \\sqrt{\\frac{(\\sigma_1-\\sigma_2)^2+(\\sigma_2-\\sigma_3)^2+(\\sigma_3-\\sigma_1)^2}{2}} \\leq [\\sigma]$$
        **适用**：塑性材料
        **优点**：更符合实验数据
        **缺点**：计算稍复杂
        """)

    with tab3:
        st.markdown("""
        ### 📊 组合变形

        #### 什么是组合变形？
        构件同时承受两种或以上基本变形的受力状态。

        #### 分析方法：**叠加原理**
        1. 将组合变形分解为各基本变形
        2. 分别计算各基本变形的应力
        3. 叠加得到组合应力
        4. 用强度理论进行校核

        #### 常见组合变形类型

        **1. 拉弯组合（偏心拉伸）**
        $$\\sigma = \\frac{F}{A} \\pm \\frac{M \\cdot y}{I}$$

        **2. 弯扭组合（传动轴）**
        - 弯曲正应力：$\\sigma = \\frac{M}{W}$
        - 扭转切应力：$\\tau = \\frac{T}{W_p}$
        - 等效应力：$\\sigma_{r4} = \\sqrt{\\sigma^2 + 3\\tau^2}$

        **3. 压弯组合**
        $$\\sigma = -\\frac{F}{A} \\pm \\frac{M \\cdot y}{I}$$

        **4. 拉扭组合**
        $$\\sigma_{r4} = \\sqrt{\\sigma^2 + 3\\tau^2}$$
        """)

    with tab4:
        st.markdown("### 🧠 知识图谱")
        st.graphviz_chart('''
        digraph {
            "强度理论" -> "第一(最大拉应力)"
            "强度理论" -> "第二(最大拉应变)"
            "强度理论" -> "第三(最大切应力)"
            "强度理论" -> "第四(畸变能)"
            "组合变形" -> "拉弯组合"
            "组合变形" -> "弯扭组合"
            "组合变形" -> "压弯组合"
            "组合变形" -> "拉扭组合"
            "第一" -> "脆性材料"
            "第二" -> "脆性材料"
            "第三" -> "塑性材料"
            "第四" -> "塑性材料"
            "拉弯组合" -> "σ=F/A ± M/W"
            "弯扭组合" -> "σ_r4=√(σ²+3τ²)"
            "第三" -> "σ_r3=σ₁-σ₃"
            "第四" -> "σ_r4=√(σ₁²+σ₂²-σ₁σ₂)"
        }
        ''')

# ============================================================
# 2. 组合变形计算
# ============================================================
elif module == "📊 组合变形计算":
    st.title("📊 组合变形计算器")
    st.markdown("输入载荷和截面参数，实时计算组合应力")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### ⚙️ 载荷参数")
        deform_type = st.selectbox("组合变形类型", ["拉弯组合", "弯扭组合", "压弯组合", "拉扭组合"])

        F = st.number_input("轴向力 F (N)", value=50000, step=5000)
        M = st.number_input("弯矩 M (N·m)", value=2000, step=100)
        T = st.number_input("扭矩 T (N·m)", value=1500, step=100)

        st.markdown("### 📐 截面参数")
        st.info("⚠️ 仅供教学演示，采用简化计算")
        d = st.slider("直径 d (mm)", 20, 120, 50, 2)

        # 计算截面属性
        A = np.pi * d ** 2 / 4
        I = np.pi * d ** 4 / 64
        W = I / (d / 2)
        J = np.pi * d ** 4 / 32
        Wp = J / (d / 2)

        # 计算应力
        sigma_N = F / A / 1e6  # MPa
        sigma_M = M / W / 1e6  # MPa
        tau_T = T / Wp / 1e6  # MPa

        if deform_type == "拉弯组合":
            sigma_comb_max = sigma_N + sigma_M
            sigma_comb_min = sigma_N - sigma_M
            sigma3 = 0
            tau_comb = 0
        elif deform_type == "弯扭组合":
            sigma_comb_max = sigma_M
            sigma_comb_min = -sigma_M
            sigma3 = 0
            tau_comb = tau_T
        elif deform_type == "压弯组合":
            sigma_comb_max = -sigma_N + sigma_M
            sigma_comb_min = -sigma_N - sigma_M
            sigma3 = 0
            tau_comb = 0
        else:  # 拉扭组合
            sigma_comb_max = sigma_N
            sigma_comb_min = sigma_N
            sigma3 = 0
            tau_comb = tau_T

        st.markdown("---")
        st.markdown("### 📊 各应力分量")
        st.metric("轴向应力 σ_N", f"{sigma_N:.2f} MPa")
        st.metric("弯曲应力 σ_M", f"{sigma_M:.2f} MPa")
        st.metric("扭转切应力 τ_T", f"{tau_T:.2f} MPa")

    with col2:
        # 计算主应力
        sigma1, sigma2, tau_max = principal_stresses(sigma_comb_max, sigma_comb_min, tau_comb)

        # 计算四大强度理论等效应力
        nu = 0.3
        sigma_r = strength_theories(sigma1, sigma2, nu)

        st.markdown("### 📊 组合应力结果")
        st.metric("最大组合应力", f"{sigma_comb_max:.2f} MPa")
        st.metric("最小组合应力", f"{sigma_comb_min:.2f} MPa")
        st.metric("最大切应力", f"{tau_max:.2f} MPa")

        st.markdown("### 📊 强度理论等效应力")
        theories = ["第一强度理论", "第二强度理论", "第三强度理论", "第四强度理论"]
        for name, val in zip(theories, sigma_r):
            st.metric(name, f"{val:.2f} MPa")

        # 材料选择与校核
        material = st.selectbox("选择材料进行校核", list(MATERIALS.keys()))
        mat = MATERIALS[material]
        sigma_allow = mat["sigma_s"] / 2.0

        selected_theory = st.selectbox("选择强度理论", ["第一强度理论", "第二强度理论", "第三强度理论", "第四强度理论"])
        theory_map = {"第一强度理论": 0, "第二强度理论": 1, "第三强度理论": 2, "第四强度理论": 3}
        sigma_r_selected = sigma_r[theory_map[selected_theory]]

        if sigma_r_selected <= sigma_allow:
            st.success(f"✅ {material} 在 {selected_theory} 下安全")
            st.write(f"σ_r = {sigma_r_selected:.2f} MPa ≤ [{sigma}] = {sigma_allow:.2f} MPa")
        else:
            st.error(f"❌ {material} 在 {selected_theory} 下不安全")
            st.write(f"σ_r = {sigma_r_selected:.2f} MPa > [{sigma}] = {sigma_allow:.2f} MPa")

# ============================================================
# 3. 强度理论对比
# ============================================================
elif module == "💪 强度理论对比":
    st.title("💪 四大强度理论对比")
    st.markdown("在同一应力状态下对比各理论的计算结果")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### ⚙️ 输入应力状态")
        sigma1_input = st.slider("主应力 σ₁ (MPa)", -100, 300, 100, 5)
        sigma2_input = st.slider("主应力 σ₂ (MPa)", -100, 200, 40, 5)
        sigma3_input = st.slider("主应力 σ₃ (MPa)", -100, 100, 0, 5)
        nu_input = st.slider("泊松比 ν", 0.1, 0.45, 0.3, 0.01)

        material_type = st.selectbox("材料类型", ["塑性材料", "脆性材料"])

        # 计算四大强度理论
        sigma_r1 = sigma1_input
        sigma_r2 = sigma1_input - nu_input * (sigma2_input + sigma3_input)
        sigma_r3 = sigma1_input - sigma3_input
        sigma_r4 = np.sqrt(((sigma1_input - sigma2_input) ** 2 +
                            (sigma2_input - sigma3_input) ** 2 +
                            (sigma3_input - sigma1_input) ** 2) / 2)

    with col2:
        # 显示对比表
        data = {
            "理论": ["第一强度理论 (最大拉应力)", "第二强度理论 (最大拉应变)",
                     "第三强度理论 (最大切应力)", "第四强度理论 (畸变能)"],
            "等效应力 (MPa)": [f"{sigma_r1:.2f}", f"{sigma_r2:.2f}", f"{sigma_r3:.2f}", f"{sigma_r4:.2f}"],
            "适用材料": ["脆性材料", "脆性材料", "塑性材料", "塑性材料"],
            "特点": ["形式简单", "考虑泊松效应", "偏于安全", "符合实验"]
        }
        df = pd.DataFrame(data)
        st.table(df)

        # 推荐
        if material_type == "塑性材料":
            st.info("📌 推荐使用 **第三强度理论**（偏安全）或 **第四强度理论**（更精确）")
        else:
            st.info("📌 推荐使用 **第一强度理论** 或 **第二强度理论**（脆性材料）")

        # 条形图对比
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["第一理论", "第二理论", "第三理论", "第四理论"],
            y=[sigma_r1, sigma_r2, sigma_r3, sigma_r4],
            marker_color=['red', 'orange', 'blue', 'green'],
            text=[f"{sigma_r1:.1f}", f"{sigma_r2:.1f}", f"{sigma_r3:.1f}", f"{sigma_r4:.1f}"],
            textposition='outside'
        ))
        fig.update_layout(title="四大强度理论等效应力对比",
                          yaxis_title="等效应力 (MPa)", height=350)
        fig = set_chinese_font(fig)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 4. 强度理论选择
# ============================================================
elif module == "🎯 强度理论选择":
    st.title("🎯 强度理论选择助手")
    st.markdown("根据材料类型和受力状态推荐合适的强度理论")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### 🔧 材料信息")
        material = st.selectbox("选择材料", list(MATERIALS.keys()))
        mat = MATERIALS[material]
        st.write(f"材料类型: **{mat['type']}**")
        st.write(f"屈服强度: {mat['sigma_s']} MPa")
        st.write(f"抗拉强度: {mat['sigma_b']} MPa")

        st.markdown("### 📊 应力状态")
        stress_state = st.selectbox("应力状态类型", ["单向拉伸", "单向压缩", "纯剪切", "二向应力", "三向应力"])

        st.markdown("### 🎯 失效形式")
        failure_mode = st.selectbox("预期失效形式", ["屈服", "断裂", "不确定"])

    with col2:
        st.markdown("### 💡 推荐结果")

        # 推荐逻辑
        if mat["type"] == "脆性":
            if stress_state in ["单向拉伸", "二向应力"]:
                recommended = "第一强度理论 (最大拉应力理论)"
                reason = "脆性材料在拉应力作用下易发生断裂，适合用最大拉应力理论"
            else:
                recommended = "第二强度理论 (最大拉应变理论)"
                reason = "脆性材料在复杂应力状态下用最大拉应变理论更准确"
        else:  # 塑性
            if failure_mode == "屈服":
                if stress_state in ["单向拉伸", "纯剪切"]:
                    recommended = "第三强度理论 (最大切应力理论)"
                    reason = "简单应力状态下第三强度理论偏于安全，计算简单"
                else:
                    recommended = "第四强度理论 (畸变能理论)"
                    reason = "复杂应力状态下第四强度理论更符合实验数据"
            else:
                recommended = "第四强度理论 (畸变能理论)"
                reason = "工程中塑性材料常用第四强度理论，更为精确"

        st.success(f"**推荐：{recommended}**")
        st.info(f"理由：{reason}")

        st.markdown("---")
        st.markdown("### 📋 选型指南")
        st.markdown("""
        | 材料类型 | 推荐理论 | 适用场景 |
        |----------|----------|----------|
        | 塑性材料 | 第三/第四 | 弯扭组合、复杂应力 |
        | 脆性材料 | 第一/第二 | 受拉构件、铸件 |
        | 接近屈服 | 第三 | 保守设计 |
        | 复杂应力 | 第四 | 精确设计 |
        """)

# ============================================================
# 5. 工程应用
# ============================================================
elif module == "🏗️ 工程应用":
    st.title("🏗️ 工程应用案例")

    case = st.selectbox("选择案例", ["传动轴设计", "偏心柱设计", "压力容器接管", "机器人关节"])

    if case == "传动轴设计":
        st.markdown("""
        ### 🏗️ 传动轴弯扭组合设计

        **工程背景**：
        某传动轴同时承受弯矩和扭矩，是典型的**弯扭组合**变形。
        要求：选择合适的轴径，满足强度要求。
        """)

        col1, col2 = st.columns(2)
        with col1:
            P = st.slider("传递功率 P (kW)", 5, 100, 30, 5)
            n = st.slider("转速 n (rpm)", 100, 2000, 500, 50)
            M_b = st.slider("弯矩 M (N·m)", 100, 5000, 1000, 50)
            material = st.selectbox("材料", ["45钢", "40Cr钢", "Q235钢"])
            n_s = st.slider("安全系数", 1.5, 4.0, 2.0, 0.5)

        with col2:
            # 计算扭矩
            T = 9550 * P / n
            mat = MATERIALS[material]
            sigma_allow = mat["sigma_s"] / n_s

            # 按第四强度理论设计轴径
            # σ_r4 = √(σ² + 3τ²) ≤ [σ]
            # σ = 32M/(πd³), τ = 16T/(πd³)
            # 代入得: d ≥ [16/(π[σ]) * √(M² + T²)]^(1/3)

            d_min = (16 / (np.pi * sigma_allow) * np.sqrt(M_b ** 2 + T ** 2) * 1000) ** (1 / 3) * 1000
            d_select = int(np.ceil(d_min / 5)) * 5

            st.metric("扭矩 T", f"{T:.1f} N·m")
            st.metric("所需最小直径", f"{d_min:.1f} mm")
            st.metric("选用直径", f"{d_select} mm")

            # 校核
            d_check = d_select / 1000
            sigma_calc = 32 * M_b / (np.pi * d_check ** 3) / 1e6
            tau_calc = 16 * T / (np.pi * d_check ** 3) / 1e6
            sigma_r4 = np.sqrt(sigma_calc ** 2 + 3 * tau_calc ** 2)

            st.metric("实际应力", f"{sigma_r4:.2f} MPa",
                      delta=f"裕度 {(sigma_allow / sigma_r4 - 1) * 100:.1f}%" if sigma_r4 <= sigma_allow else "超限")

            if sigma_r4 <= sigma_allow:
                st.success("✅ 设计合格")
            else:
                st.error("❌ 需增大直径")

# ============================================================
# 6. 案例分析
# ============================================================
elif module == "📐 案例分析":
    st.title("📐 案例分析：弯扭组合轴")

    st.markdown("""
    ### 📌 问题描述

    某传动轴传递功率 **P = 40 kW**，转速 **n = 600 rpm**，
    同时承受弯矩 **M = 800 N·m**。

    轴材料为 **45钢**（σ_s = 355 MPa），安全系数 **n = 2**。
    要求：
    1. 设计轴的最小直径
    2. 用第四强度理论校核
    3. 对比第三和第四强度理论的结果
    """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        P = st.slider("功率 P (kW)", 10, 100, 40, 5)
        n = st.slider("转速 n (rpm)", 100, 1500, 600, 50)
        M = st.slider("弯矩 M (N·m)", 200, 2000, 800, 50)
        material = st.selectbox("材料", ["45钢", "40Cr钢", "Q235钢"])
        n_s = st.slider("安全系数", 1.5, 4.0, 2.0, 0.5)

    with col2:
        T = 9550 * P / n
        mat = MATERIALS[material]
        sigma_allow = mat["sigma_s"] / n_s

        # 第四强度理论设计
        d_4 = (16 / (np.pi * sigma_allow) * np.sqrt(M ** 2 + T ** 2) * 1000) ** (1 / 3) * 1000

        # 第三强度理论设计
        d_3 = (32 / (np.pi * sigma_allow) * np.sqrt(M ** 2 + T ** 2) * 1000) ** (1 / 3) * 1000

        st.metric("扭矩 T", f"{T:.1f} N·m")
        st.metric("第四强度理论直径", f"{d_4:.1f} mm")
        st.metric("第三强度理论直径", f"{d_3:.1f} mm")
        st.metric("直径差", f"{d_3 - d_4:.1f} mm",
                  delta="第三理论偏保守" if d_3 > d_4 else "第四理论偏保守")

        # 选用直径
        d_sel = int(np.ceil(max(d_3, d_4) / 5)) * 5
        st.info(f"建议选用直径: **{d_sel} mm**")

# ============================================================
# 7. 应力云图
# ============================================================
elif module == "🎨 应力云图":
    st.title("🎨 组合变形应力云图")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        deform_type = st.selectbox("组合类型", ["拉弯组合", "弯扭组合", "压弯组合"])
        sigma_N = st.slider("轴向应力 σ_N (MPa)", -100, 100, 20, 5)
        sigma_M = st.slider("弯曲应力 σ_M (MPa)", 0, 200, 60, 5)
        tau_T = st.slider("切应力 τ (MPa)", 0, 100, 30, 5)

    with col2:
        if deform_type == "拉弯组合":
            sigma_total = sigma_N + sigma_M * np.ones((50, 50))
            for i in range(50):
                sigma_total[i, :] = sigma_N + sigma_M * (i - 25) / 25
            title = "拉弯组合应力分布"
        elif deform_type == "弯扭组合":
            sigma_total = sigma_M * (np.arange(50).reshape(50, 1) - 25) / 25
            title = "弯扭组合应力分布"
        else:
            sigma_total = -sigma_N + sigma_M * (np.arange(50).reshape(50, 1) - 25) / 25
            title = "压弯组合应力分布"

        fig = go.Figure(data=go.Heatmap(
            z=sigma_total,
            colorscale='RdBu_r',
            zmid=0,
            colorbar=dict(title="应力 (MPa)")
        ))
        fig.update_layout(title=f"{title} 云图", height=450)
        fig = set_chinese_font(fig)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 8. 3D可视化
# ============================================================
elif module == "🔄 3D可视化":
    st.title("🔄 3D应力状态可视化")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        sigma_x = st.slider("σ_x (MPa)", -100, 200, 80, 5)
        sigma_y = st.slider("σ_y (MPa)", -80, 150, 30, 5)
        sigma_z = st.slider("σ_z (MPa)", -80, 150, 20, 5)
        tau_xy = st.slider("τ_xy (MPa)", -80, 80, 40, 5)
        nu = st.slider("泊松比 ν", 0.1, 0.45, 0.3, 0.01)

    with col2:
        # 3D应力张量
        stress_tensor = np.array([
            [sigma_x, tau_xy, 0],
            [tau_xy, sigma_y, 0],
            [0, 0, sigma_z]
        ])

        fig = go.Figure(data=go.Heatmap(
            z=stress_tensor,
            x=["σx", "τxy", "τxz"],
            y=["σx", "τyx", "τzx"],
            text=[[f"{v:.0f}" for v in row] for row in stress_tensor],
            texttemplate="%{text}",
            textfont={"size": 16},
            colorscale='RdBu_r',
            zmid=0
        ))
        fig.update_layout(title="应力张量", height=400)
        fig = set_chinese_font(fig)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 9. 虚拟实验
# ============================================================
elif module == "🧪 虚拟实验":
    st.title("🧪 虚拟组合变形实验")

    st.markdown("""
    ### 🔬 虚拟实验：组合变形与强度理论

    调整载荷参数，观察应力状态和强度理论等效应力的变化。
    """)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        F = st.slider("轴向力 F (kN)", 0, 200, 50, 5)
        M = st.slider("弯矩 M (kN·m)", 0, 10, 2, 0.1)
        T = st.slider("扭矩 T (kN·m)", 0, 8, 1.5, 0.1)
        d = st.slider("轴径 d (mm)", 20, 100, 50, 2)
        material = st.selectbox("材料", list(MATERIALS.keys()))
        mat = MATERIALS[material]
        n = st.slider("安全系数", 1.5, 4.0, 2.0, 0.5)
        sigma_allow = mat["sigma_s"] / n

    with col2:
        # 计算应力
        A = np.pi * d ** 2 / 4
        W = np.pi * d ** 3 / 32
        Wp = np.pi * d ** 3 / 16

        sigma_N = F * 1000 / A / 1e6
        sigma_M = M * 1000 / W / 1e6
        tau_T = T * 1000 / Wp / 1e6

        sigma_comb = np.sqrt((sigma_N + sigma_M) ** 2 + 3 * tau_T ** 2)

        st.metric("轴向应力", f"{sigma_N:.2f} MPa")
        st.metric("弯曲应力", f"{sigma_M:.2f} MPa")
        st.metric("切应力", f"{tau_T:.2f} MPa")
        st.metric("等效应力 σ_r4", f"{sigma_comb:.2f} MPa")
        st.metric("许用应力", f"{sigma_allow:.2f} MPa")

        if sigma_comb <= sigma_allow:
            st.success("✅ 安全")
            st.balloons()
        else:
            st.error("❌ 不安全")

st.markdown("---")
st.caption("⚙️ 四大强度理论·组合变形 | 智能学习系统")