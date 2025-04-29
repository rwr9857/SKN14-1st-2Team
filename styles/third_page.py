# 스타일 설정
from turtle import st


def set_custom_styles():
    st.markdown(
        """
        <style>
        
        .stApp {
            background-color: white;
            min-height: 100vh;
            position: relative;
            padding-bottom: 60px;
        }
        .block-container {
            max-width: calc(100% - 400px) !important;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .st-emotion-cache-t1wise {
            padding: 2rem 1rem 10rem;
        }
 
        .copyright {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 1200px;
            text-align: center;
            padding: 1rem;
            background-color: white;
            color: #888;
            font-size: 1em;
            border-top: 1px solid #eee;
        }
        .close-button-container {
            position: absolute;
            top: 1rem;
            right: 1rem;
            z-index: 999999;
        }
        .close-button {
            width: 32px;
            height: 32px;
            background-color: #02584B;
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease;
            padding: 0;
            line-height: 1;
            text-decoration: none;
        }
        .close-button:hover {
            background-color: #036b5f;
            text-decoration: none;
            color: white;
        }
        .option-menu {
            background-color: #F8B94A;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .option-menu-item {
            color: #333;
        }
        .option-menu-item:hover {
            color: #EEB437;
        }
        .option-menu-item.active {
            color: #EEB437;
            font-weight: bold;
        }
        .section-title {
            color: #EEB437;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
            font-size: 20px;
        }
        .option-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 10px 0;
        }
        .option-button {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .option-button:hover {
            background-color: #FFF9E6;
            border-color: #EEB437;
        }
        .option-button.selected {
            background-color: #FFF9E6;
            border-color: #EEB437;
            color: #EEB437;
            font-weight: bold;
        }
        .stButton button {
            background-color: #EEB437;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            width: 100%; 
        }
        
        .st-emotion-cache-ocsh0s {
            min-height: 0rem;
        }
        .st-emotion-cache-180ybpv {
            flex : 1;
        }
        
        .st-emotion-cache-10c9vv9 {
            display: flex;
            background-color: #F6C248;
            width: 30px;
            height: 30px;
            justify-content: center;
            align-items: center;
            border-radius: 50%;
        }
       
        
        .st-emotion-cache-16tyu1 a {
            color: WHITE !important;
            text-decoration: none !important;
        }
        .stButton button:hover {
            background-color: #d69c2e;
        }
        .stProgress > div > div {
            background-color: #EEB437;
        }
        .sidebar-content {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .car-card {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #EEB437;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .car-title-container {
            padding: 0 50px;
            width: 100%;
        }
        .car-title {
            color: white;
            font-weight: bold;
            text-align: center;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            padding: 0.5rem 1rem;
            background-color: #EEB437;
            display: block;
        }
        .st-emotion-cache-16tyu1 h3 {
            padding: 0.2rem 0px 0.2rem;
            width: 100%;
            display: flex;
            justify-content: center;
        }
        .car-info {
            color: #333;
            margin-bottom: 5px;
        }
        
        .car-subtitle {
            font-size: 1.8rem;
            color: #02584B;
            margin-bottom: 2rem;
            background-color: #f8d66d;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            display: inline-block;
        }
        .car-image {
            text-align: center;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 70px;
        }
        .car-image img {
            max-width: 100%;
            height: auto;
        }
        .st-emotion-cache-u0yi3i {
            gap:0 !important;
        }
        
        .car-specs {
            width: 100%;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin-top: 2rem;
        }
        .spec-item {
            display: flex;
            align-items: center;
            gap: 0.1rem;
    
            color: #333;
            padding: 0.5rem;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .spec-label {
            color: #666;
            min-width: 80px;
        }
        .navigation-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem 0;
        }
        .navigation-button {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #02584B;
        }
        .car-info-right {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            padding: 1rem;
        }
        .stButton>button {
            background-color: transparent !important;
            border: none !important;
            color: black !important;
            font-weight: 900 !important;
            font-size: 24px !important;
            padding: 0 !important;
            box-shadow: none !important;
        }
        .stButton>button:hover {
            background-color: transparent !important;
            color: #333333 !important;
        }
        </style>
        
        <div class="close-button-container">
            <a href="fourth_page" target="_self" class="close-button">×</a>
        </div>
    """,
        unsafe_allow_html=True,
    )