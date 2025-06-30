"""
TalentScout AI Hiring Assistant - Streamlit Cloud Deployment Version
Optimized for cloud deployment with enhanced performance and security
"""

import streamlit as st
import json
import re
import os
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
import sqlite3
import logging
from pathlib import Path
import time
import random

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="TalentScout AI - Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/talentscout-ai',
        'Report a bug': 'https://github.com/yourusername/talentscout-ai/issues',
        'About': "# TalentScout AI Hiring Assistant\nAdvanced AI-powered technical candidate screening platform."
    }
)

# Configure logging for Streamlit Cloud
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom CSS for premium UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800;900&family=Fredoka:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles with Cute Pastels */
    .main {
        font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #FFE5F1 0%, #E5F3FF 25%, #F0E5FF 50%, #E5FFE5 75%, #FFF5E5 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Floating cute shapes background */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(255, 182, 193, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(173, 216, 230, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 60%, rgba(221, 160, 221, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 70% 30%, rgba(152, 251, 152, 0.3) 0%, transparent 50%);
        animation: floatShapes 20s ease-in-out infinite;
    }
    
    @keyframes floatShapes {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-20px) rotate(120deg); }
        66% { transform: translateY(10px) rotate(240deg); }
    }
    
    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Adorable glassmorphism header */
    .main-header {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 2px solid rgba(255, 182, 193, 0.3);
        padding: 3rem 2rem;
        border-radius: 35px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 
            0 25px 50px rgba(255, 182, 193, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        position: relative;
        overflow: hidden;
        transform: translateY(0);
        animation: headerFloat 6s ease-in-out infinite;
    }
    
    @keyframes headerFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .main-header::before {
        content: '✨';
        position: absolute;
        top: 20px;
        right: 30px;
        font-size: 2rem;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    .main-header::after {
        content: '🌸';
        position: absolute;
        bottom: 20px;
        left: 30px;
        font-size: 1.5rem;
        animation: sparkle 2s ease-in-out infinite 1s;
    }
    
    @keyframes sparkle {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.7; }
        50% { transform: scale(1.2) rotate(180deg); opacity: 1; }
    }
    
    .main-header h1 {
        font-family: 'Fredoka', cursive;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF69B4 0%, #87CEEB 25%, #DDA0DD 50%, #98FB98 75%, #FFB6C1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(255, 105, 180, 0.3);
        animation: textShimmer 3s ease-in-out infinite;
    }
    
    @keyframes textShimmer {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(30deg); }
    }
    
    .main-header p {
        font-size: 1.4rem;
        color: #8B7D8B;
        font-weight: 500;
        margin: 0;
    }
    
    /* Floating cute particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .particle {
        position: absolute;
        border-radius: 50%;
        animation: floatParticle 8s infinite ease-in-out;
    }
    
    .particle:nth-child(1) {
        width: 8px; height: 8px;
        background: #FFB6C1;
        left: 10%; animation-delay: 0s;
    }
    .particle:nth-child(2) {
        width: 12px; height: 12px;
        background: #87CEEB;
        left: 20%; animation-delay: 1s;
    }
    .particle:nth-child(3) {
        width: 6px; height: 6px;
        background: #DDA0DD;
        left: 30%; animation-delay: 2s;
    }
    .particle:nth-child(4) {
        width: 10px; height: 10px;
        background: #98FB98;
        left: 40%; animation-delay: 3s;
    }
    .particle:nth-child(5) {
        width: 14px; height: 14px;
        background: #F0E68C;
        left: 50%; animation-delay: 4s;
    }
    .particle:nth-child(6) {
        width: 8px; height: 8px;
        background: #FFA07A;
        left: 60%; animation-delay: 5s;
    }
    .particle:nth-child(7) {
        width: 16px; height: 16px;
        background: #E6E6FA;
        left: 70%; animation-delay: 6s;
    }
    .particle:nth-child(8) {
        width: 10px; height: 10px;
        background: #F5DEB3;
        left: 80%; animation-delay: 7s;
    }
    .particle:nth-child(9) {
        width: 12px; height: 12px;
        background: #FFE4E1;
        left: 90%; animation-delay: 8s;
    }
    
    @keyframes floatParticle {
        0%, 100% { 
            transform: translateY(100vh) rotate(0deg) scale(0); 
            opacity: 0; 
        }
        10% { 
            opacity: 1; 
            transform: translateY(90vh) rotate(45deg) scale(1); 
        }
        90% { 
            opacity: 1; 
            transform: translateY(-10vh) rotate(315deg) scale(1); 
        }
        100% { 
            opacity: 0; 
            transform: translateY(-20vh) rotate(360deg) scale(0); 
        }
    }
    
    /* Adorable chat messages */
    .chat-message {
        padding: 2rem;
        border-radius: 25px;
        margin: 1.5rem 0;
        position: relative;
        animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        transform: translateY(0);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .chat-message:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes bounceIn {
        0% { 
            opacity: 0; 
            transform: translateY(50px) scale(0.8) rotate(-5deg); 
        }
        60% { 
            opacity: 1; 
            transform: translateY(-10px) scale(1.05) rotate(2deg); 
        }
        100% { 
            opacity: 1; 
            transform: translateY(0) scale(1) rotate(0deg); 
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(255, 182, 193, 0.3) 0%, rgba(255, 218, 185, 0.3) 100%);
        border-left: 5px solid #FFB6C1;
        margin-left: 3rem;
        position: relative;
    }
    
    .user-message::before {
        content: '💭';
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 1.5rem;
        animation: bounce 2s infinite;
    }
    
    .bot-message {
        background: linear-gradient(135deg, rgba(173, 216, 230, 0.3) 0%, rgba(221, 160, 221, 0.3) 100%);
        border-left: 5px solid #87CEEB;
        margin-right: 3rem;
        position: relative;
    }
    
    .bot-message::before {
        content: '🤖';
        position: absolute;
        top: -10px;
        left: 20px;
        font-size: 1.5rem;
        animation: wiggle 3s infinite;
    }
    
    .system-message {
        background: linear-gradient(135deg, rgba(152, 251, 152, 0.3) 0%, rgba(240, 230, 140, 0.3) 100%);
        border-left: 5px solid #98FB98;
        text-align: center;
        font-style: italic;
        position: relative;
    }
    
    .system-message::before {
        content: '💡';
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 1.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    @keyframes wiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(5deg); }
        75% { transform: rotate(-5deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: translateX(-50%) scale(1); }
        50% { transform: translateX(-50%) scale(1.2); }
    }
    
    .message-header {
        font-family: 'Fredoka', cursive;
        font-weight: 600;
        font-size: 1.1rem;
        color: #6B5B73;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .message-content {
        line-height: 1.8;
        color: #5D4E75;
        font-size: 1.05rem;
        font-weight: 400;
    }
    
    .message-time {
        font-size: 0.85rem;
        color: #9B8AA3;
        margin-top: 1rem;
        text-align: right;
        font-weight: 500;
    }
    
    /* Cute sidebar cards */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        padding: 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 40px rgba(255, 182, 193, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        border: 2px solid rgba(255, 182, 193, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
        opacity: 0;
    }
    
    .sidebar-card:hover {
        transform: translateY(-8px) rotate(1deg);
        box-shadow: 
            0 30px 60px rgba(255, 182, 193, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    
    .sidebar-card:hover::before {
        opacity: 1;
        left: 100%;
    }
    
    .sidebar-title {
        font-family: 'Fredoka', cursive;
        font-weight: 600;
        font-size: 1.3rem;
        color: #6B5B73;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    /* Adorable progress bar */
    .progress-container {
        margin: 1.5rem 0;
        position: relative;
    }
    
    .progress-bar {
        background: rgba(255, 182, 193, 0.2);
        border-radius: 20px;
        height: 20px;
        overflow: hidden;
        position: relative;
        border: 2px solid rgba(255, 182, 193, 0.3);
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #FFB6C1, #87CEEB, #DDA0DD, #98FB98);
        background-size: 200% 100%;
        height: 100%;
        border-radius: 18px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        animation: progressFlow 3s linear infinite;
    }
    
    @keyframes progressFlow {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
        animation: progressShimmer 2s infinite;
    }
    
    @keyframes progressShimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Cute info items */
    .info-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        border-bottom: 1px solid rgba(255, 182, 193, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 15px;
        margin: 0.5rem 0;
        position: relative;
    }
    
    .info-item:hover {
        background: rgba(255, 182, 193, 0.1);
        transform: translateX(10px) scale(1.02);
        border-bottom-color: rgba(255, 182, 193, 0.3);
    }
    
    .info-item:last-child {
        border-bottom: none;
    }
    
    /* Adorable tech badges */
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FFB6C1, #87CEEB);
        color: white;
        padding: 0.6rem 1.4rem;
        border-radius: 25px;
        font-size: 0.9rem;
        margin: 0.4rem;
        font-weight: 600;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .tech-badge:hover {
        transform: translateY(-3px) scale(1.1) rotate(2deg);
        box-shadow: 0 15px 30px rgba(255, 182, 193, 0.6);
        background: linear-gradient(135deg, #FF69B4, #00BFFF);
    }
    
    .tech-badge::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .tech-badge:hover::before {
        left: 100%;
    }
    
    /* Floating buttons - the star of the show! */
    .stButton > button {
        background: linear-gradient(135deg, #FFB6C1 0%, #87CEEB 50%, #DDA0DD 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1.2rem 3rem;
        font-family: 'Fredoka', cursive;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 15px 35px rgba(255, 182, 193, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        position: relative;
        overflow: hidden;
        text-transform: none;
        letter-spacing: 0.5px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        animation: buttonFloat 4s ease-in-out infinite;
    }
    
    @keyframes buttonFloat {
        0%, 100% { 
            transform: translateY(0px) rotate(0deg); 
            box-shadow: 0 15px 35px rgba(255, 182, 193, 0.4);
        }
        50% { 
            transform: translateY(-8px) rotate(1deg); 
            box-shadow: 0 25px 50px rgba(255, 182, 193, 0.6);
        }
    }
    
    .stButton > button:hover {
        transform: translateY(-12px) scale(1.05) rotate(-1deg);
        box-shadow: 
            0 30px 60px rgba(255, 182, 193, 0.8),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        background: linear-gradient(135deg, #FF69B4 0%, #00BFFF 50%, #DA70D6 100%);
        animation: none;
    }
    
    .stButton > button:active {
        transform: translateY(-8px) scale(0.98) rotate(0deg);
        box-shadow: 0 20px 40px rgba(255, 182, 193, 0.6);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Cute input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 20px;
        border: 2px solid rgba(255, 182, 193, 0.3);
        padding: 1.2rem;
        font-size: 1.05rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(255, 182, 193, 0.1);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #FFB6C1;
        box-shadow: 
            0 0 0 4px rgba(255, 182, 193, 0.2),
            0 15px 35px rgba(255, 182, 193, 0.3);
        background: rgba(255, 255, 255, 1);
        transform: translateY(-2px);
    }
    
    /* Adorable typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem;
        color: #8B7D8B;
        font-style: italic;
        background: rgba(255, 182, 193, 0.15);
        border-radius: 25px;
        margin: 1.5rem 0;
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 182, 193, 0.2);
        animation: typingFloat 3s ease-in-out infinite;
    }
    
    @keyframes typingFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .typing-dots {
        display: flex;
        gap: 0.5rem;
    }
    
    .typing-dot {
        width: 12px;
        height: 12px;
        background: linear-gradient(135deg, #FFB6C1, #87CEEB);
        border-radius: 50%;
        animation: typingBounce 1.4s infinite ease-in-out;
        box-shadow: 0 4px 8px rgba(255, 182, 193, 0.3);
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    .typing-dot:nth-child(3) { animation-delay: 0s; }
    
    @keyframes typingBounce {
        0%, 80%, 100% { 
            transform: scale(0.8); 
            opacity: 0.5; 
        }
        40% { 
            transform: scale(1.4); 
            opacity: 1; 
        }
    }
    
    /* Cute status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .status-active {
        background: linear-gradient(135deg, #98FB98, #90EE90);
        color: #2F5233;
        animation: statusPulse 2s infinite;
    }
    
    .status-completed {
        background: linear-gradient(135deg, #87CEEB, #6495ED);
        color: #1E3A8A;
    }
    
    @keyframes statusPulse {
        0%, 100% { 
            box-shadow: 0 8px 20px rgba(152, 251, 152, 0.4); 
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 15px 35px rgba(152, 251, 152, 0.6); 
            transform: scale(1.05);
        }
    }
    
    /* Magical completion celebration */
    .completion-card {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(152, 251, 152, 0.2), rgba(173, 216, 230, 0.2));
        border-radius: 35px;
        margin: 2rem 0;
        backdrop-filter: blur(25px);
        border: 3px solid rgba(152, 251, 152, 0.3);
        box-shadow: 0 25px 50px rgba(152, 251, 152, 0.3);
        position: relative;
        overflow: hidden;
        animation: celebrationFloat 4s ease-in-out infinite;
    }
    
    @keyframes celebrationFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(1deg); }
    }
    
    .completion-card::before {
        content: '🎉✨🌟';
        position: absolute;
        font-size: 4rem;
        top: -1rem;
        right: -1rem;
        opacity: 0.3;
        animation: celebrationSpin 6s infinite ease-in-out;
    }
    
    @keyframes celebrationSpin {
        0%, 100% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.2); }
    }
    
    .completion-title {
        font-family: 'Fredoka', cursive;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2F5233;
        margin-bottom: 1rem;
        animation: titleBounce 2s ease-out;
    }
    
    @keyframes titleBounce {
        0% { transform: scale(0.3) rotate(-10deg); opacity: 0; }
        50% { transform: scale(1.1) rotate(5deg); }
        70% { transform: scale(0.9) rotate(-2deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    
    /* Adorable footer */
    .footer {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(25px);
        border-radius: 35px;
        margin-top: 4rem;
        border: 2px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 20px 40px rgba(255, 182, 193, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '💖';
        position: absolute;
        top: 20px;
        right: 30px;
        font-size: 2rem;
        animation: heartBeat 2s infinite;
    }
    
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    .footer h3 {
        font-family: 'Fredoka', cursive;
        background: linear-gradient(135deg, #FFB6C1 0%, #87CEEB 50%, #DDA0DD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Responsive design for mobile cuteness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .main-header p {
            font-size: 1.1rem;
        }
        
        .user-message {
            margin-left: 1rem;
        }
        
        .bot-message {
            margin-right: 1rem;
        }
        
        .sidebar-card {
            padding: 1.5rem;
        }
        
        .stButton > button {
            padding: 1rem 2rem;
            font-size: 1rem;
        }
    }
    
    /* Custom scrollbar with pastel colors */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 182, 193, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFB6C1, #87CEEB);
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FF69B4, #00BFFF);
    }
    
    /* Extra cute animations for special elements */
    .cute-emoji {
        display: inline-block;
        animation: emojiDance 3s infinite ease-in-out;
    }
    
    @keyframes emojiDance {
        0%, 100% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(10deg) scale(1.1); }
        75% { transform: rotate(-10deg) scale(0.9); }
    }
</style>
""", unsafe_allow_html=True)

# Add floating particles
st.markdown("""
<div class="particles">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
</div>
""", unsafe_allow_html=True)

@dataclass
class CandidateInfo:
    """Data class for storing candidate information"""
    session_id: str = ""
    full_name: str = ""
    email: str = ""
    phone: str = ""
    experience_years: str = ""
    desired_position: str = ""
    location: str = ""
    tech_stack: List[str] = field(default_factory=list)
    technical_answers: Dict[str, str] = field(default_factory=dict)
    created_at: str = ""
    
    def __post_init__(self):
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class DatabaseManager:
    """Handles database operations for Streamlit Cloud"""
    
    def __init__(self, db_path: str = "candidates.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS candidates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        full_name TEXT,
                        email TEXT,
                        phone TEXT,
                        experience_years TEXT,
                        desired_position TEXT,
                        location TEXT,
                        tech_stack TEXT,
                        technical_answers TEXT,
                        created_at TEXT,
                        updated_at TEXT
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        message_type TEXT,
                        content TEXT,
                        timestamp TEXT,
                        stage TEXT,
                        FOREIGN KEY (session_id) REFERENCES candidates (session_id)
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def save_candidate(self, candidate: CandidateInfo):
        """Save candidate information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO candidates 
                    (session_id, full_name, email, phone, experience_years, 
                     desired_position, location, tech_stack, technical_answers, 
                     created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    candidate.session_id,
                    candidate.full_name,
                    candidate.email,
                    candidate.phone,
                    candidate.experience_years,
                    candidate.desired_position,
                    candidate.location,
                    json.dumps(candidate.tech_stack),
                    json.dumps(candidate.technical_answers),
                    candidate.created_at,
                    datetime.now().isoformat()
                ))
                conn.commit()
                logger.info(f"Candidate data saved for session: {candidate.session_id}")
        except Exception as e:
            logger.error(f"Error saving candidate data: {e}")
    
    def log_conversation(self, session_id: str, message_type: str, content: str, stage: str = ""):
        """Log conversation messages"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO conversations 
                    (session_id, message_type, content, timestamp, stage)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    session_id,
                    message_type,
                    content[:500],  # Limit content length
                    datetime.now().isoformat(),
                    stage
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Error logging conversation: {e}")

class HiringAssistant:
    """Main chatbot class optimized for Streamlit Cloud"""
    
    def __init__(self):
        self.conversation_stages = [
            "greeting", "name_collection", "email_collection", "phone_collection",
            "experience_collection", "position_collection", "location_collection",
            "tech_stack_collection", "technical_questions", "conclusion"
        ]
        
        self.stage_names = {
            "greeting": "Welcome & Introduction",
            "name_collection": "Personal Information",
            "email_collection": "Contact Details",
            "phone_collection": "Phone Verification",
            "experience_collection": "Experience Assessment",
            "position_collection": "Position Interest",
            "location_collection": "Location Information",
            "tech_stack_collection": "Technical Skills",
            "tech_stack_collection": "Technical Skills Assessment",
            "technical_questions": "Technical Interview",
            "conclusion": "Interview Completion"
        }
        
        self.current_stage_index = 0
        self.candidate_info = CandidateInfo()
        self.technical_questions = []
        self.current_question_index = 0
        self.conversation_ended = False
        self.db_manager = DatabaseManager()
        
        # Comprehensive tech keywords
        self.tech_keywords = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'csharp',
                'php', 'ruby', 'go', 'golang', 'rust', 'kotlin', 'swift', 'scala',
                'r', 'dart', 'elixir', 'haskell', 'clojure'
            ],
            'frontend_frameworks': [
                'react', 'angular', 'vue', 'vue.js', 'svelte', 'ember', 'backbone',
                'jquery', 'bootstrap', 'tailwind', 'material-ui', 'next.js', 'nuxt',
                'gatsby', 'alpine.js'
            ],
            'backend_frameworks': [
                'django', 'flask', 'fastapi', 'spring', 'spring boot', 'express',
                'node.js', 'laravel', 'symfony', 'rails', 'sinatra', 'gin', 'echo',
                'asp.net', 'nest.js'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle',
                'sql server', 'cassandra', 'elasticsearch', 'firebase', 'dynamodb',
                'supabase', 'planetscale'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'vercel', 'netlify', 'railway', 'render'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
                'terraform', 'ansible', 'prometheus', 'grafana'
            ]
        }
        
        # Fallback technical questions
        self.fallback_questions = {
            'python': [
                "What is the difference between list and tuple in Python?",
                "Explain Python's GIL and its implications for multithreading.",
                "How do you handle exceptions in Python?"
            ],
            'javascript': [
                "What is the difference between == and === in JavaScript?",
                "Explain closures in JavaScript with an example.",
                "What is the event loop in JavaScript?"
            ],
            'react': [
                "What is the difference between state and props in React?",
                "Explain React component lifecycle methods.",
                "What are React Hooks and their benefits?"
            ],
            'general': [
                "Describe a challenging technical problem you've solved recently.",
                "How do you stay updated with new technologies?",
                "What's your approach to debugging complex issues?"
            ]
        }
        
        self.exit_keywords = [
            'bye', 'goodbye', 'exit', 'quit', 'end', 'stop', 'finish',
            'terminate', 'close', 'done', 'thanks', 'thank you'
        ]
    
    def is_exit_keyword(self, user_input: str) -> bool:
        """Check if user wants to exit"""
        return any(keyword in user_input.lower().strip() for keyword in self.exit_keywords)
    
    def get_current_stage(self) -> str:
        """Get current conversation stage"""
        if self.current_stage_index < len(self.conversation_stages):
            return self.conversation_stages[self.current_stage_index]
        return "conclusion"
    
    def get_stage_name(self, stage: str) -> str:
        """Get human-readable stage name"""
        return self.stage_names.get(stage, stage.replace('_', ' ').title())
    
    def get_progress(self) -> float:
        """Calculate progress percentage"""
        return (self.current_stage_index / len(self.conversation_stages)) * 100
    
    def advance_stage(self):
        """Move to next stage"""
        self.current_stage_index += 1
        logger.info(f"Advanced to stage: {self.get_current_stage()}")
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number"""
        digits_only = re.sub(r'\D', '', phone)
        return 10 <= len(digits_only) <= 15
    
    def extract_tech_stack(self, user_input: str) -> List[str]:
        """Extract technologies from user input"""
        found_tech = []
        user_lower = user_input.lower()
        
        for category, keywords in self.tech_keywords.items():
            for tech in keywords:
                if tech in user_lower and tech.title() not in found_tech:
                    found_tech.append(tech.title())
        
        return sorted(list(set(found_tech)))
    
    def generate_technical_questions(self, tech_stack: List[str]) -> List[str]:
        """Generate technical questions based on tech stack"""
        questions = []
        
        for tech in tech_stack[:3]:
            tech_lower = tech.lower()
            if tech_lower in self.fallback_questions:
                questions.extend(self.fallback_questions[tech_lower][:2])
        
        if not questions:
            questions = self.fallback_questions['general'][:3]
        
        return questions[:5]
    
    def get_response(self, user_input: str) -> str:
        """Main conversation handler"""
        
        # Log conversation
        self.db_manager.log_conversation(
            self.candidate_info.session_id,
            "user",
            user_input,
            self.get_current_stage()
        )
        
        # Check for exit
        if self.is_exit_keyword(user_input):
            self.conversation_ended = True
            self.db_manager.save_candidate(self.candidate_info)
            return """Thank you for your time! 👋

I hope you found this screening process helpful. Our recruitment team will review your information and get back to you within 2-3 business days if your profile matches our current openings.

Best of luck with your job search! 🌟"""
        
        current_stage = self.get_current_stage()
        response = ""
        
        try:
            if current_stage == "greeting":
                self.advance_stage()
                response = """Hello and welcome! 👋

I'm the **TalentScout AI Hiring Assistant**, your intelligent partner for technical candidate screening.

**What I'll do:**
• 📝 Collect basic information about your background
• 🛠️ Learn about your technical skills and experience
• 🧠 Ask relevant technical questions based on your expertise
• ✨ Provide a smooth, conversational interview experience

**Privacy & Security:**
Your information is handled securely and used only for recruitment purposes.

This process takes about 5-10 minutes. You can end our conversation anytime by typing 'exit'.

Let's get started! **What's your full name?**"""

            elif current_stage == "name_collection":
                if user_input.strip() and len(user_input.strip()) >= 2:
                    self.candidate_info.full_name = user_input.strip()
                    self.advance_stage()
                    response = f"""Nice to meet you, **{self.candidate_info.full_name}**! 😊

Now I'll need some contact information.

**What's your email address?**"""
                else:
                    response = "Please provide your full name to continue."

            elif current_stage == "email_collection":
                if self.validate_email(user_input):
                    self.candidate_info.email = user_input.strip()
                    self.advance_stage()
                    response = """Perfect! ✅

**What's your phone number?** (Include area code)"""
                else:
                    response = "Please provide a valid email address (e.g., john@example.com)."

            elif current_stage == "phone_collection":
                if self.validate_phone(user_input):
                    self.candidate_info.phone = user_input.strip()
                    self.advance_stage()
                    response = """Great! 📱

**How many years of professional experience do you have in technology?**

You can say something like "3 years", "5+ years", "Fresh graduate", etc."""
                else:
                    response = "Please provide a valid phone number."

            elif current_stage == "experience_collection":
                if user_input.strip():
                    self.candidate_info.experience_years = user_input.strip()
                    self.advance_stage()
                    response = """Excellent! 💼

**What position(s) are you most interested in?**

Examples:
• Software Developer/Engineer
• Data Scientist/Analyst
• DevOps Engineer
• Full Stack Developer
• Frontend/Backend Developer
• Mobile App Developer"""
                else:
                    response = "Please specify your years of experience."

            elif current_stage == "position_collection":
                if user_input.strip():
                    self.candidate_info.desired_position = user_input.strip()
                    self.advance_stage()
                    response = """Perfect! 🎯

**What's your current location?** (City, State/Country)

This helps us match you with relevant opportunities."""
                else:
                    response = "Please specify the position you're interested in."

            elif current_stage == "location_collection":
                if user_input.strip():
                    self.candidate_info.location = user_input.strip()
                    self.advance_stage()
                    response = """Great! 📍

Now for the exciting part - let's talk about your **technical skills**! 💻

**Please tell me about your tech stack.** List the programming languages, frameworks, databases, and tools you're proficient in.

**Examples:**
• "Python, Django, React, PostgreSQL, AWS"
• "Java, Spring Boot, Angular, MySQL"
• "JavaScript, Node.js, Vue.js, MongoDB"

Just mention the main technologies you're comfortable with."""
                else:
                    response = "Please provide your current location."

            elif current_stage == "tech_stack_collection":
                if user_input.strip():
                    tech_stack = self.extract_tech_stack(user_input)
                    if tech_stack:
                        self.candidate_info.tech_stack = tech_stack
                        self.technical_questions = self.generate_technical_questions(tech_stack)
                        self.advance_stage()
                        
                        tech_list = ", ".join(tech_stack)
                        response = f"""Excellent! I've identified your expertise in: **{tech_list}** 🛠️

Now I'll ask you **{len(self.technical_questions)}** technical questions tailored to your skills.

Please answer to the best of your ability. I'm interested in your thought process and understanding.

---

**Technical Question 1:**

**{self.technical_questions[0]}**"""
                    else:
                        response = """I couldn't identify specific technologies. Please mention specific programming languages, frameworks, or tools:

• Programming languages: Python, Java, JavaScript, etc.
• Frameworks: React, Django, Spring, etc.
• Databases: MySQL, PostgreSQL, MongoDB, etc.
• Tools: Git, Docker, AWS, etc.

**What technologies are you proficient in?**"""
                else:
                    response = "Please tell me about your technical skills."

            elif current_stage == "technical_questions":
                if user_input.strip():
                    # Store answer
                    self.candidate_info.technical_answers[f"Q{self.current_question_index + 1}"] = {
                        "question": self.technical_questions[self.current_question_index],
                        "answer": user_input.strip(),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    self.current_question_index += 1
                    
                    if self.current_question_index < len(self.technical_questions):
                        response = f"""Thank you for your answer! 👍

---

**Technical Question {self.current_question_index + 1}:**

**{self.technical_questions[self.current_question_index]}**"""
                    else:
                        self.advance_stage()
                        response = f"""Excellent work! You've completed all {len(self.technical_questions)} technical questions! 🎉

**Interview Summary:**
• **Name:** {self.candidate_info.full_name}
• **Position:** {self.candidate_info.desired_position}
• **Experience:** {self.candidate_info.experience_years}
• **Location:** {self.candidate_info.location}
• **Tech Stack:** {', '.join(self.candidate_info.tech_stack)}
• **Questions Completed:** {len(self.technical_questions)}

**What's Next?**
1. Our team will review your responses within 2-3 business days
2. If your profile matches our openings, we'll contact you
3. You may be invited for a detailed technical interview

**Is there anything else you'd like to know about TalentScout or our process?**

Type 'goodbye' to end our conversation."""
                else:
                    response = "Please provide an answer to continue."

            else:  # conclusion
                self.conversation_ended = True
                response = """Thank you for your interest in TalentScout! 🌟

Your screening has been completed successfully and your information has been securely recorded.

**Next Steps:**
• Our recruitment team will review your profile
• You'll hear back within 2-3 business days if there's a match
• Keep an eye on your email (including spam folder)

**Tips:**
• Continue building your skills
• Connect with us on LinkedIn
• The tech industry is always evolving!

Have a wonderful day and best of luck with your career journey! 🚀

*Thank you for choosing TalentScout - where talent meets opportunity.*"""

            # Log response
            self.db_manager.log_conversation(
                self.candidate_info.session_id,
                "assistant",
                response,
                self.get_current_stage()
            )
            
            # Save candidate data
            if self.candidate_info.full_name:
                self.db_manager.save_candidate(self.candidate_info)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            return "I apologize for the technical issue. Please try rephrasing your response or type 'exit' to end our conversation."

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = HiringAssistant()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'typing' not in st.session_state:
        st.session_state.typing = False
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

def main():
    """Main application function"""
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1><span class="cute-emoji">🤖</span> TalentScout AI <span class="cute-emoji">✨</span></h1>
        <p>Adorably Smart Technical Candidate Screening 💕</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create layout
    col1, col2 = st.columns([1, 2])
    
    # Sidebar content
    with col1:
        # About section
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-title">ℹ️ About This Assistant</div>
            <div class="info-item">
                <span>🎯</span>
                <span>AI-powered candidate screening</span>
            </div>
            <div class="info-item">
                <span>🧠</span>
                <span>Intelligent question generation</span>
            </div>
            <div class="info-item">
                <span>⚡</span>
                <span>Real-time conversation flow</span>
            </div>
            <div class="info-item">
                <span>🔒</span>
                <span>Secure data handling</span>
            </div>
            <div class="info-item">
                <span>📊</span>
                <span>Comprehensive profiling</span>
            </div>
            <div style="margin-top: 1.5rem; padding: 1.2rem; background: rgba(102, 126, 234, 0.1); border-radius: 15px; font-size: 0.9rem;">
                <strong>🔐 Privacy & Security:</strong><br>
                Your information is encrypted and stored securely in compliance with privacy regulations.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress section
        current_stage = st.session_state.assistant.get_current_stage()
        progress = st.session_state.assistant.get_progress()
        stage_name = st.session_state.assistant.get_stage_name(current_stage)
        
        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-title">📊 Interview Progress</div>
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <div style="font-weight: 600; color: #333; margin-bottom: 0.5rem;">
                    Current Stage: {stage_name}
                </div>
                <div style="font-size: 0.9rem; color: #666; margin-bottom: 1rem;">
                    Progress: {int(progress)}% Complete
                </div>
                <div class="status-badge {'status-active' if not st.session_state.assistant.conversation_ended else 'status-completed'}">
                    {'🟢 Active Interview' if not st.session_state.assistant.conversation_ended else '✅ Interview Completed'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Candidate information
        candidate = st.session_state.assistant.candidate_info
        if candidate.full_name:
            info_html = '<div class="sidebar-card"><div class="sidebar-title">👤 Candidate Profile</div>'
            
            if candidate.full_name:
                info_html += f'<div class="info-item"><span>👤</span><span><strong>{candidate.full_name}</strong></span></div>'
            if candidate.email:
                info_html += f'<div class="info-item"><span>📧</span><span>{candidate.email}</span></div>'
            if candidate.phone:
                info_html += f'<div class="info-item"><span>📱</span><span>{candidate.phone}</span></div>'
            if candidate.experience_years:
                info_html += f'<div class="info-item"><span>⏱️</span><span>{candidate.experience_years} experience</span></div>'
            if candidate.desired_position:
                info_html += f'<div class="info-item"><span>💼</span><span>{candidate.desired_position}</span></div>'
            if candidate.location:
                info_html += f'<div class="info-item"><span>📍</span><span>{candidate.location}</span></div>'
            if candidate.tech_stack:
                info_html += '<div style="margin-top: 1.5rem;"><div style="font-weight: 600; margin-bottom: 1rem; color: #333;">🛠️ Technical Skills:</div>'
                for tech in candidate.tech_stack:
                    info_html += f'<span class="tech-badge">{tech}</span>'
                info_html += '</div>'
            
            if candidate.technical_answers:
                info_html += f'<div style="margin-top: 1.5rem; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 15px; border: 1px solid rgba(16, 185, 129, 0.3);"><div style="font-weight: 600; color: #059669;">✅ Technical Assessment</div><div style="font-size: 0.9rem; color: #047857;">{len(candidate.technical_answers)} questions completed</div></div>'
            
            info_html += '</div>'
            st.markdown(info_html, unsafe_allow_html=True)
    
    # Main chat area
    with col2:
        st.markdown('<div class="sidebar-title">💬 AI Interview Assistant</div>', unsafe_allow_html=True)
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display messages
            for message in st.session_state.messages:
                timestamp = datetime.now().strftime("%H:%M")
                
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-header">
                            👤 You
                        </div>
                        <div class="message-content">{message["content"]}</div>
                        <div class="message-time">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif message["role"] == "assistant":
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <div class="message-header">
                            🤖 TalentScout AI Assistant
                        </div>
                        <div class="message-content">{message["content"]}</div>
                        <div class="message-time">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # system message
                    st.markdown(f"""
                    <div class="chat-message system-message">
                        <div class="message-content">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Typing indicator
            if st.session_state.typing:
                st.markdown("""
                <div class="typing-indicator">
                    <span>🤖 AI Assistant is processing your response</span>
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Input section
        if not st.session_state.conversation_started:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 2rem; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); border-radius: 25px; margin: 2rem 0; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);">
                <h3 style="color: #333; margin-bottom: 1rem; font-size: 1.8rem; font-weight: 700;">Ready to Start Your AI Interview? 🚀</h3>
                <p style="color: #666; margin-bottom: 2rem; font-size: 1.1rem;">Experience the future of technical candidate screening with our advanced AI assistant.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Start AI Interview Process", key="start_btn"):
                st.session_state.conversation_started = True
                st.session_state.typing = True
                st.rerun()
        
        elif st.session_state.typing:
            # Simulate AI processing
            time.sleep(2)
            if not st.session_state.messages or st.session_state.messages[-1]["role"] != "assistant":
                # Initial greeting
                welcome_message = st.session_state.assistant.get_response("")
                st.session_state.messages.append({"role": "assistant", "content": welcome_message})
            else:
                # Response to user input
                last_user_message = None
                for msg in reversed(st.session_state.messages):
                    if msg["role"] == "user":
                        last_user_message = msg["content"]
                        break
                
                if last_user_message:
                    response = st.session_state.assistant.get_response(last_user_message)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.session_state.typing = False
            st.rerun()
        
        elif not st.session_state.assistant.conversation_ended:
            # Chat input
            st.markdown("---")
            
            user_input = st.text_area(
                "Your Response:",
                height=120,
                placeholder="Type your response here... (You can type 'exit' or 'goodbye' to end the conversation)",
                key="user_input"
            )
            
            # Button row
            col_send, col_clear, col_help = st.columns([2, 1, 1])
            
            with col_send:
                send_clicked = st.button("📤 Send Response", key="send_btn", type="primary")
            
            with col_clear:
                if st.button("🗑️ Clear", key="clear_btn"):
                    st.session_state.user_input = ""
                    st.rerun()
            
            with col_help:
                if st.button("❓ Help", key="help_btn"):
                    help_message = "💡 **Tip:** Answer naturally and provide as much detail as you're comfortable with. The AI adapts to your responses!"
                    st.session_state.messages.append({"role": "system", "content": help_message})
                    st.rerun()
            
            # Handle send
            if send_clicked and user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.typing = True
                st.rerun()
        
        else:
            # Conversation completed
            st.markdown("""
            <div class="completion-card">
                <div class="completion-title">🎉 Interview Completed!</div>
                <p style="color: #059669; font-size: 1.2rem; margin-bottom: 2rem;">
                    Thank you for completing the TalentScout AI screening process.<br>
                    Your responses have been securely recorded.
                </p>
                <div style="background: rgba(255,255,255,0.8); padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0;">
                    <strong style="color: #059669;">Next Steps:</strong><br>
                    <span style="color: #047857;">• Review within 2-3 business days<br>
                    • Email notification if profile matches<br>
                    • Potential follow-up interview invitation</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_restart, col_export = st.columns(2)
            
            with col_restart:
                if st.button("🔄 Start New Interview", key="restart_btn"):
                    # Reset everything
                    st.session_state.assistant = HiringAssistant()
                    st.session_state.messages = []
                    st.session_state.conversation_started = False
                    st.session_state.typing = False
                    st.session_state.session_id = str(uuid.uuid4())
                    st.rerun()
            
            with col_export:
                if st.button("📄 Download Summary", key="export_btn"):
                    # Create summary
                    candidate = st.session_state.assistant.candidate_info
                    summary = {
                        "candidate_info": {
                            "name": candidate.full_name,
                            "email": candidate.email,
                            "phone": candidate.phone,
                            "experience": candidate.experience_years,
                            "position": candidate.desired_position,
                            "location": candidate.location,
                            "tech_stack": candidate.tech_stack
                        },
                        "technical_assessment": candidate.technical_answers,
                        "session_info": {
                            "session_id": candidate.session_id,
                            "completed_at": datetime.now().isoformat(),
                            "total_questions": len(candidate.technical_answers)
                        }
                    }
                    
                    st.download_button(
                        label="📥 Download Interview Summary",
                        data=json.dumps(summary, indent=2),
                        file_name=f"interview_summary_{candidate.session_id[:8]}.json",
                        mime="application/json"
                    )
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>🏢 TalentScout AI - Revolutionizing Technical Recruitment</h3>
        <p style="margin: 1rem 0; color: #666;">
            <strong>Powered by:</strong> Advanced AI • Modern UI/UX • Secure Data Handling<br>
            <strong>Built with:</strong> Streamlit • Python • SQLite • Premium Design
        </p>
        <p style="font-size: 0.9rem; color: #888;">
            © 2024 TalentScout AI. Built for the developer community with ❤️
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
