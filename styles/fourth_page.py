import streamlit as st


# 스타일 설정
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
        .main-content {
            margin-top: 20px;
            padding-bottom: 60px;
        }
        .car-info-container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .car-info-header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .car-specs {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .spec-item {
            padding: 5px 0;
            font-size: 16px;
        }
        .spec-label {
            font-weight: bold;
            color: #555;
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
        .car-title {
            color: #02584B;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            padding-top: 20px;
            border-bottom: 2px solid #F6C248;
        }
        .review-stats {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        .review-metric {
            font-size: 18px;
            font-weight: bold;
            color: #F6C248;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .star-rating {
            color: #F6C248;
            font-size: 20px;
            letter-spacing: 2px;
        }
        .star-empty {
            color: #ddd;
        }
        .participant-count {
            color: #666;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .graph-container {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .review-button {
            margin-top: 10px;
        }
        .review-button button {
            background-color: #F6C248 !important;
            color: white !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            font-size: 14px !important;
        }
        .review-button button:hover {
            background-color: #e5b43c !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }
        .comment-section {
            margin-top: 20px;
            padding: 20px;
       
            border-radius: 10px;
        }
        .comment-card {
            background-color: white;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 3px solid #F6C248;
        }
        .comment-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            color: #666;
            font-size: 14px;
        }
        .comment-content {
            color: #333;
            line-height: 1.5;
        }
        .graph-title {
            font-size: 16px;
            font-weight: bold;
            color: #02584B;
            margin-bottom: 10px;
            text-align: center;
        }
        .rating-box {
            background-color: white;
            padding: 10px;
            padding-left: 40px;
            border-radius: 8px;
            text-align: center;
            max-width: 200px;
            margin-bottom: 20px;
        }
        .average-score {
            font-size: 36px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .participant-count {
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }
        .rating-description {
            color: #666;
            font-size: 13px;
            line-height: 1.4;
            text-align: center;
        }
        .star-rating {
            color: #F6C248;
            font-size: 24px;
            letter-spacing: 2px;
            margin: 10px 0;
        }
        .car-image-container {
            width: 100%;
            max-height: 250px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .car-image-container img {
            width: 100%;
            height: auto;
            object-fit: contain;
            vertical-align: middle;
        }
        .st-emotion-cache-16tyu1 h2 {
            font-size: 1.5rem;
        }
        .image-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        .review-button {
            margin-top: 0 !important;
        }
        .review-button button {
            background-color: #F6C248 !important;
            color: white !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            font-size: 14px !important;
            width: 100% !important;
        }
        .review-button button:hover {
            background-color: #e5b43c !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }
        .age-group-container {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .car-rank {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }
        .rank-label {
            font-weight: bold;
            color: #02584B;
            min-width: 30px;
        }
        .car-info {
            flex-grow: 1;
        }
        .age-title {
            color: #02584B;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #F6C248;
        }
        .car-rank-container {
            display: flex;
            justify-content: space-between;
            gap: 15px;
            margin-top: 15px;
        }
        .car-rank {
            flex: 1;
            text-align: center;
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .car-image {
            width: 100%;
            height: 150px;
            object-fit: contain;
            margin-top: 10px;
        }
        .age-column {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            height: 100%;
        }
        .car-rank {
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .rank-label {
            font-weight: bold;
            color: #02584B;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .car-info {
            margin: 10px 0;
            text-align: center;
        }
        .car-image {
            width: 100%;
            height: 150px;
            object-fit: contain;
            margin-top: 10px;
        }
        .age-title {
            color: #02584B;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #F6C248;
            text-align: center;
        }
        .age-row {
            background-color: #EDF3F9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .age-label {
            color: #02584B;
            font-size: 28px;
            font-weight: bold;
            margin-right: 30px;
            min-width: 80px;
        }
        .cars-container {
            display: flex;
            align-items: center;
            gap: 30px;
        }
        .car-list {
            display: flex;
            gap: 30px;
            flex-grow: 1;
        }
        .car-item {
            flex: 1;
            text-align: center;
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: relative;
        }
        .car-image {
            width: 100%;
            height: 120px;
            object-fit: contain;
            margin-bottom: 10px;
        }
        .car-rank {
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #F6C248;
            color: white;
            padding: 3px 15px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
  
        .car-name {
            font-weight: bold;
            color: #333;
            margin: 10px 0 5px 0;
            font-size: 15px;
        }
        .car-count {
            color: #666;
            font-size: 13px;
        }
        .rank-divider {
            width: 30px;
            height: 2px;
            background-color: #ddd;
            margin: 0 10px;
        }
        .age-stats-container {
            background-color: #EDF3F9;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding-top: 20px;
        }
        .st-emotion-cache-16tyu1 h3 {
            font-size: 1.2rem;
            padding: 2rem 0px 1rem;
        }
        
        p, ol, ul, dl {
        
        }
        
        .age-group-title {
            color: #02584B;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .car-card {
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: relative;
            min-height: 280px;
            display: flex;
            flex-direction: column;
        }
        .car-rank-badge {
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #F6C248;
            color: white;
            padding: 3px 15px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .car-image {
            width: 100%;
            height: 120px;
            object-fit: contain;
            margin: 10px 0;
        }
        .car-title {
            font-weight: bold;
            color: #333;
            margin: 10px 0 5px 0;
            font-size: 15px;
            text-align: center;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .car-count {
            color: #666;
            font-size: 13px;
            text-align: center;
        }
        .gender-stats-table {
            font-size: 14px;
            margin-top: 15px;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
