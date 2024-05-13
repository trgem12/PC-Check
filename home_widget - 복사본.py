# home_widget.py
import json
import os

import plotly.graph_objects as go
import plotly.io as pio
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolTip
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pyqtgraph as pg
from PyQt5.QtChart import QBarSet, QBarSeries, QChart, QBarCategoryAxis, QValueAxis, QChartView, QLineSeries, \
    QDateTimeAxis
from datetime import datetime
from main import ScoreLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 메인 레이아웃 설정
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 좌측 레이아웃 생성 및 메인 레이아웃에 추가
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 5)

        # 우측 레이아웃 생성 및 메인 레이아웃에 추가
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        # 점수판 레이아웃 생성 및 좌측 레이아웃에 추가
        self.scoreboard_layout = QVBoxLayout()
        self.update_scoreboard()
        self.scoreboard_layout.setContentsMargins(50, 0, 0, 0)  # 최소 너비 설정
        left_layout.addLayout(self.scoreboard_layout)

        # 최근 검사 그래프 레이아웃을 생성하고 오른쪽 레이아웃에 추가
        self.recent_inspection_layout = QVBoxLayout()
        self.update_recent_inspection_graph()
        self.recent_inspection_layout.setContentsMargins(20, 30, 30, 0)  # 최소 너비 설정
        right_layout.addLayout(self.recent_inspection_layout)

        # Create a security check trend graph layout
        self.security_check_trend_layout = QVBoxLayout()
        self.update_security_check_trend()
        self.security_check_trend_layout.setContentsMargins(20, 0, 30, 30)  # 최소 너비 설정
        right_layout.addLayout(self.security_check_trend_layout)

    def update_scoreboard(self):
        # JSON 파일에서 최신 'total_score' 값을 읽어옵니다.
        # file_path = 'C:\\security_check_history.json'
        file_path = 'security_check_history.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                history = json.load(file)
                latest_score = history[-1]['total_score']  # 최신 점수
        except Exception as e:
            print(e)
            latest_score = 'No information'  # 파일 읽기 오류 시

        if isinstance(latest_score, float):
            latest_score = int(latest_score)

        # 배경색, 이미지 경로, 텍스트 설정
        if isinstance(latest_score, (int, float)):
            if latest_score > 90:
                background_color = QColor('green')
                # image_path = r'D:\pythonProject\green.png'
                image_path = os.path.join(os.getcwd(), "_internal", "batch_files", "green.png")
            elif latest_score > 70:
                background_color = QColor('#FFC041')
                # image_path = r'D:\pythonProject\yellow.png'
                image_path = os.path.join(os.getcwd(), "_internal", "batch_files", "yellow.png")
            else:
                background_color = QColor('red')
                image_path = os.path.join(os.getcwd(), "_internal", "batch_files", "sred.png")
                # image_path = r'D:\pythonProject\sred.png'
        else:
            background_color = QColor('gray')
            image_path = None  # 점수 정보가 없을 때 이미지 없음

        # ScoreLabel 인스턴스 생성 및 스코어보드 레이아웃에 추가
        score_label = ScoreLabel(latest_score, image_path, background_color)
        self.scoreboard_layout.addWidget(score_label)

    def update_recent_inspection_graph(self):
        # Read inspection data from JSON file
        # file_path = 'C:\\security_check_history.json'
        file_path = 'security_check_history.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                history = json.load(file)
                latest_inspection = history[-1]['summary']  # Most recent inspection summary information
        except Exception as e:
            print(e)
            latest_inspection = {'양호한 항목': 0, '취약한 항목': 0, '점검 불가 항목': 0}

        # Prepare data for JavaScript
        data = [latest_inspection['양호한 항목'], latest_inspection['취약한 항목'], latest_inspection['점검 불가 항목']]
        labels = ['양호 항목', '취약 항목', '검사 불가 항목']

        # Create HTML with embedded JavaScript
        html = f"""
        <!DOCTYPE html>
        <html>
        <body>
        <canvas id="myChart" style="width:100%;height:100%;background-color:#31363B;"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: ['점검 결과'],
                datasets: [
                    {{
                        label: '양호한 항목',
                        data: [{data[0]}],
                        backgroundColor: 'rgba(75, 192, 192, 1)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }},
                    {{
                        label: '취약한 항목',
                        data: [{data[1]}],
                        backgroundColor: 'rgba(255, 99, 132, 1)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }},
                    {{
                        label: '점검 불가 항목',
                        data: [{data[2]}],
                        backgroundColor: 'rgba(54, 162, 235, 1)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                aspectRatio: 4.2,  // 그래프의 높이를 두 배로 늘립니다.
                legend: {{
                    display: true  // 레전드를 표시합니다.
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }},
                    x: {{
                        gridLines: {{
                            display: false  // 세로 줄을 제거합니다.
                        }}
                    }}
                }}
            }}
        }});
        </script>
        </body>
        </html>
        """

        # Create QWebEngineView, and set HTML
        view = QWebEngineView()
        view.setHtml(html)
        view.setFixedSize(790, 200)  # Set the size of the QWebEngineView

        # Remove widgets from existing layout
        for i in reversed(range(self.recent_inspection_layout.count())):
            self.recent_inspection_layout.itemAt(i).widget().setParent(None)

        # Add QWebEngineView to layout
        self.recent_inspection_layout.addWidget(view, stretch=2)

    def update_security_check_trend(self):
        # Read inspection data from JSON file
        # file_path = 'C:\\security_check_history.json'
        file_path = 'security_check_history.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                history = json.load(file)
        except Exception as e:
            print(e)
            history = []

        # Prepare data for JavaScript
        data = [entry['total_score'] for entry in history]
        labels = [entry['completion_time'] for entry in history]

        # Create HTML with embedded JavaScript
        html = f"""
        <!DOCTYPE html>
        <html>
        <body>
        <canvas id="myChart" style="width:100%;height:100%;background-color:#31363B;"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {labels},
                datasets: [{{
                    label: '점검 점수 추이',
                    data: {data},
                    backgroundColor: 'rgba(75, 192, 192, 1)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
            aspectRatio: 4.2,  // 그래프의 높이를 두 배로 늘립니다.
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        </script>
        </body>
        </html>
        """

        # Create QWebEngineView, and set HTML
        view = QWebEngineView()
        view.setHtml(html)
        view.setFixedSize(790, 200)  # Set the size of the QWebEngineView

        # Remove widgets from existing layout
        for i in reversed(range(self.security_check_trend_layout.count())):
            self.security_check_trend_layout.itemAt(i).widget().setParent(None)

        # Add QWebEngineView to layout
        self.security_check_trend_layout.addWidget(view, stretch=2)