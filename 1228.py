import sys, subprocess, os, threading, socket, webbrowser, time, platform
import json
from datetime import datetime
import win32com
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QTabWidget, QLabel, QTextEdit, QStackedWidget, QDockWidget, QListWidget, QHeaderView, QDialog, \
    QFrame, QHBoxLayout, QMessageBox, QTreeWidgetItem, QTreeWidget, QAbstractItemView, QLayout, QComboBox
from reportlab.lib.pagesizes import landscape, letter, A4, A3
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from PyQt5.QtChart import QBarSet, QBarSeries, QChart, QBarCategoryAxis, QValueAxis, QChartView, QLineSeries, \
    QDateTimeAxis
import pyqtgraph as pg
from reportlab.platypus import Paragraph



# PC취약점 진단
class VulnerabilityScanner(QWidget):
    def __init__(self, customer_info_widget=None):
        super().__init__()
        self.customer_info_widget = customer_info_widget
        self.report_data = {
            '점검 완료 시간': '',
            'Check score': '',
            '점검 결과': {}
        }
        self.completion_time = None  # 점검 완료 시간을 저장할 속성 추가
        self.total_score = 0  # 점검 점수를 저장할 속성 추가
        self.summary_data = {'안전한 항목': 0, '취약한 항목': 0, '점검 불가 항목': 0} # 점검 결과 요약을 저장할 속성 추가

        # 메인 수직 레이아웃 설정
        main_layout = QVBoxLayout(self)

        # 레이아웃 1: 버튼들을 위한 레이아웃
        buttons_layout = QHBoxLayout()
        # 점검결과 점수를 표시할 QLabel 위젯 추가
        self.score_label = QLabel("점검결과: 00점")
        self.score_label.setStyleSheet("""
        QLabel {
        font-weight: bold;
        font-size: 14px;
        color: black;
        }
        """)
        buttons_layout.addWidget(self.score_label)

        self.all_check_button = QPushButton("전체 점검", self)
        self.all_check_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.all_check_button.clicked.connect(self.run_all_checks)
        buttons_layout.addWidget(self.all_check_button)

        self.individual_check_button = QPushButton("개별 항목 점검", self)
        self.individual_check_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.individual_check_button.clicked.connect(self.run_individual_check)
        buttons_layout.addWidget(self.individual_check_button)

        # "보고서 생성" 버튼 추가
        self.create_report_button = QPushButton("보고서 생성", self)
        self.create_report_button.setStyleSheet("""
        QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 8px;
        }
        QPushButton:hover {
        background-color: #2980b9;
        }
        """)
        self.create_report_button.clicked.connect(self.save_report)
        buttons_layout.addWidget(self.create_report_button)

        # 레이아웃 1를 메인 레이아웃에 추가
        main_layout.addLayout(buttons_layout)

        # 레이아웃 2: 결과 테이블을 위한 레이아웃
        result_table_layout = QVBoxLayout()
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["카테고리", "점검항목", "결과"])
        result_table_layout.addWidget(self.result_table)

        # 테이블 열 너비 및 사용자 조정 방지 설정
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.result_table.setColumnWidth(0, 200)
        self.result_table.setColumnWidth(1, 600)
        self.result_table.setColumnWidth(2, 200)

        # 레이아웃 2을 메인 레이아웃에 추가
        main_layout.addLayout(result_table_layout)

        # 레이아웃 3: 상세 정보 출력 및 추가 정보 표시를 위한 레이아웃
        layout_3 = QHBoxLayout()

        # 추가 정보를 표시하기 위한 레이아웃
        additional_info_layout = QVBoxLayout()
        self.check_pc_label = QLabel(f"점검 PC 이름: {socket.gethostname()}")
        self.start_time_label = QLabel("점검 시작 시간: 대기 중")
        self.end_time_label = QLabel("점검 완료 시간: 대기 중")
        self.status_label = QLabel("상태: 대기 중")
        self.report_label = QLabel("보고서 저장: 대기중 ")

        # 추가 정보 레이아웃에 QLabel 위젯들을 추가
        additional_info_layout.addWidget(self.check_pc_label)
        additional_info_layout.addWidget(self.start_time_label)
        additional_info_layout.addWidget(self.end_time_label)
        additional_info_layout.addWidget(self.status_label)
        additional_info_layout.addWidget(self.report_label)

        # 레이아웃 3에 추가 정보 레이아웃과 상세 정보 출력 레이아웃을 추가
        layout_3.addLayout(additional_info_layout)

        # 레이아웃 3: 세부 정보 출력을 위한 QTextEdit
        detail_info_layout = QVBoxLayout()
        self.detail_info = QTextEdit(self)
        self.detail_info.setReadOnly(True)
        detail_info_layout.addWidget(self.detail_info)
        self.result_table.itemClicked.connect(self.show_detail_info)

        layout_3.addLayout(detail_info_layout)

        # 레이아웃 3을 메인 레이아웃에 추가
        main_layout.addLayout(layout_3)

        self.results = {
            "서비스 관리": ["공유 폴더 점검", "멀티 OS 점검", "NTFS 설정 점검"],
            "패치 관리": ["윈도우 최신 버전 점검", "윈도우 업데이트 점검"],
            "계정 관리": ["패스워드 변경 주기 점검", "패스워드 최소길이 점검", "패스워드 복잡성 점검", "복구 콘솔 자동로그온 점검"],
            "보안 관리": ["화면 보호기 설정", "화면보호기 10분 이내 설정", "백신 프로그램 업데이트 점검", "백신 프로그램 실시간 감시", "Windows Defender방화벽 실행 점검", "휴지통 점검"],
            "SW 관리": ["이글아이 설치 점검", "문서보안 설치 점검", "SKT-AD 설치 점검", "SKT-DLP 설치 점검", "evEraser 설치 점검"]
        }

        self.populate_table()

    def update_score(self, score):
        # 점검 결과 점수 업데이트 함수
        formatted_score = f"{score:.1f}"  # 소수점 첫 번째 자리까지 포맷팅
        self.score_label.setText(f"점검결과: {formatted_score}점")

        # 점수에 따라 색상 선택
        if score >= 80:
            color = "green"
        elif score >= 31:
            color = "yellow"
        else:
            color = "red"

        # 색상을 적용하여 QLabel의 스타일 업데이트
        self.score_label.setStyleSheet(f"""
        QLabel {{
            font-weight: bold;
            font-size: 18px;
            color: {color};
        }}
        """)

    def populate_table(self):
        row_count = sum(len(items) for items in self.results.values())
        self.result_table.setRowCount(row_count)
        row = 0
        for category, items in self.results.items():
            for item in items:
                self.result_table.setItem(row, 0, QTableWidgetItem(category))
                self.result_table.setItem(row, 1, QTableWidgetItem(item))
                self.result_table.setItem(row, 2, QTableWidgetItem("대기중"))
                row += 1

    def run_all_checks(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start_time_label.setText(f"점검 시작 시간: {current_time}")
        self.status_label.setText("상태: 점검 중")
        total_items = sum(len(items) for items in self.results.values())  # 총 점검 항목 수 계산
        item_score = 100 / total_items  # 각 항목당 점수 계산
        total_score = 0  # 총 점수 초기화

        for category, items in self.results.items():
            for item in items:
                score = self.run_check(category, item)  # 점검 실행 및 점수 받기
                if score:
                    total_score += item_score  # 양호한 항목의 점수 누적

        self.update_score(total_score)  # 총 점수 업데이트
        self.show_summary()  # 요약 창 표시
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time_label.setText(f"점검 완료 시간: {completion_time}")
        self.status_label.setText("상태: 점검 완료")
        self.completion_time = completion_time  # 점검 완료 시간을 속성에 저장
        self.total_score = total_score  # 점검 점수를 속성에 저장
    def show_summary(self):
        # 요약 정보를 저장할 딕셔너리 초기화
        summary_data = {
            '안전한 항목': 0,
            '취약한 항목': 0,
            '점검 불가 항목': 0
        }
        # 결과를 순회하면서 카운트
        for row in range(self.result_table.rowCount()):
            result = self.result_table.item(row, 2).text()
            if result == "양호":
                summary_data['안전한 항목'] += 1
            elif result == "미흡":
                summary_data['취약한 항목'] += 1
            elif result == "점검 스크립트가 없습니다.":
                summary_data['점검 불가 항목'] += 1
        # 동적 데이터로 요약 창 표시
        dialog = SummaryDialog(summary_data, self)
        dialog.exec_()
        self.summary_data = summary_data  # Update class property with the summary data

    def run_individual_check(self):
        selected_items = self.result_table.selectedItems()
        if selected_items:
            row = self.result_table.row(selected_items[0])
            category = self.result_table.item(row, 0).text()
            item = self.result_table.item(row, 1).text()
            self.run_check(category, item)
            self.recalculate_score()  # 전체 점수 재계산 및 업데이트

    def recalculate_score(self):
        total_items = sum(len(items) for items in self.results.values())  # 총 점검 항목 수 계산
        item_score = 100 / total_items  # 각 항목당 점수 계산
        total_score = 0  # 총 점수 초기화

        for row in range(self.result_table.rowCount()):
            result = self.result_table.item(row, 2).text()
            if result == "양호":
                total_score += item_score  # 양호한 항목의 점수 누적
        self.update_score(total_score)  # 총 점수 업데이트
        self.total_score = total_score  # 점검 점수를 속성에 저장
        return total_score

    def run_check(self, category, item):
        batch_file = self.get_batch_file_path(category, item)
        detailed_info = ""  # '미흡'인 경우의 상세 정보를 저장할 변수
        score = False  # 점수 초기화 (양호하면 True, 미흡하면 False)
        if not batch_file:
            result = "점검 스크립트가 없습니다."
        else:
            try:
                completed_process = subprocess.run(batch_file, capture_output=True, text=True, shell=True)
                output = completed_process.stdout.strip()
                print(f"[DEBUG] Output from batch file ({batch_file}): '{output}'")
                if "미흡" in output:
                    result = "미흡"
                    detailed_info = output
                elif "양호" in output:
                    result = "양호"
                    score = True # 양호한 경우 점수 True로 설정
                else:
                    result = "스크립트 수정"  # 점검 결과가 명확하지 않은 경우
            except Exception as e:
                result = f"Error: {str(e)}"
        self.update_result(category, item, result, detailed_info)
        return score  # 점수 반환

    def get_batch_file_path(self, category, item):
        # Define the mapping from category and item to the batch file path
        batch_files = {
            ("서비스 관리", "멀티 OS 점검"): "D:\pythonProject\multibooting.bat",
            ("서비스 관리", "NTFS 설정 점검"): "D:\pythonProject\diskntfs.bat",
            ("서비스 관리", "공유 폴더 점검"): "D:\pythonProject\sharedfolder.bat",
            ("패치 관리", "윈도우 최신 버전 점검"): "D:\pythonProject\winverupgrade.bat",
            ("패치 관리", "윈도우 업데이트 점검"): "D:\pythonProject\HOTFIX_month.bat",
            ("보안 관리", "화면 보호기 설정"): "D:\pythonProject\screensaver.bat",
            ("보안 관리", "휴지통 점검"): "D:\pythonProject\strachcheck.bat",
            ("보안 관리", "화면보호기 10분 이내 설정"): "D:\pythonProject\screensaversetting.bat",
            ("보안 관리", "Windows Defender방화벽 실행 점검"): "D:\pythonProject\sfirewallcheck.bat",
            ("보안 관리", "백신 프로그램 업데이트 점검"): "D:\pythonProject\svaccine_update.bat",
            ("보안 관리", "백신 프로그램 실시간 감시"): "D:\pythonProject\svaccinertmonitor.bat",
            ("계정 관리", "패스워드 변경 주기 점검"): "D:\pythonProject\passwordch.bat.bat",
            ("계정 관리", "패스워드 최소길이 점검"): "D:\pythonProject\minpwlen.bat",
            ("계정 관리", "패스워드 복잡성 점검"): "D:\pythonProject\pwsecset.bat",
            ("계정 관리", "복구 콘솔 자동로그온 점검"): "D:\pythonProject\srecoverconsole.bat",
            ("SW 관리", "SKT-DLP 설치 점검"): "D:\pythonProject\sktdlpch.bat",
            ("SW 관리", "이글아이 설치 점검"): "D:\pythonProject\eagleyecheck.bat.bat",
            ("SW 관리", "문서보안 설치 점검"): "D:\pythonProject\softcampcheck.bat",
            ("SW 관리", "evEraser 설치 점검"): "D:\pythonProject\everaserch.bat",
            ("SW 관리", "SKT-AD 설치 점검"): "D:\pythonProject\sadcheck.bat",
            # ... add other mappings ...
        }
        return batch_files.get((category, item))

    def update_result(self, category, item, result, detailed_info=""):
        # 결과와 상세 정보를 테이블에 업데이트
        for row in range(self.result_table.rowCount()):
            if self.result_table.item(row, 0).text() == category and self.result_table.item(row, 1).text() == item:
                self.result_table.setItem(row, 2, QTableWidgetItem(result))
                # 상세 정보를 저장
                self.result_table.item(row, 2).setData(Qt.UserRole, detailed_info)
                self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                break
    def show_detail_info(self, item):
        row = item.row()
        category = self.result_table.item(row, 0).text()
        inspection_item = self.result_table.item(row, 1).text()
        result = self.result_table.item(row, 2).text()
        detailed_info = self.result_table.item(row, 2).data(Qt.UserRole)

        detail_text = f"<b>Category:</b> {category}<br><b>Item:</b> {inspection_item}<br><b>Result:</b> {result}"

        if result == "미흡" and detailed_info:
            # '미흡'인 경우 상세 정보에 줄바꿈 적용
            # "미흡 -" 다음과 "조치 방법:" 전에 줄바꿈 추가
            detailed_info_html = detailed_info.replace("현재 상태: ", "<br>현재 상태: ").replace("조치 방법: ", "<br>조치 방법: ")
            detail_text += f"<br><b>Detailed Information:</b><br>{detailed_info_html}"

        self.detail_info.setHtml(detail_text)

    def interpret_batch_output(self, output):
        # Interpret the output of the batch file and return an appropriate status
        if "insufficient" in output.lower():
            return "Insufficient - Immediate action required"
        else:
            return "Good - No action required"

    # 보안 점검 결과를 JSON 파일에 저장하는 함수
    def save_security_check_result(self, completion_time, summary_data, total_score):
        file_path = 'C:\\security_check_history.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        new_record = {
            'completion_time': completion_time,
            'summary': summary_data,
            'total_score': total_score
        }
        history.append(new_record)
        history = history[-5:]  # 최신 5개 기록만 유지

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
        print(json.dumps(history, indent=4, ensure_ascii=False))


    def save_report(self):
        # 한글 폰트 파일 경로 설정 및 폰트 등록
        korean_font_path = r'D:\pythonProject\나눔고딕.ttf'  # 실제 경로로 수정 필요
        pdfmetrics.registerFont(TTFont('NanumGothic', korean_font_path))

        # PDF 파일 이름 설정
        pdf_file_name = f"점검결과_{socket.gethostname()}_{self.completion_time.replace(':', '_').replace(' ', '_')}.pdf"
        doc = SimpleDocTemplate(pdf_file_name, pagesize=A3)

        # 스타일 시트 설정
        styles = getSampleStyleSheet()
        # 제목을 위한 스타일 추가
        styles.add(ParagraphStyle(name='KoreanTitle', fontName='NanumGothic', fontSize=20, leading=22))
        # 2번째 텍스트 및 표를 위한 스타일 추가
        styles.add(ParagraphStyle(name='Korean', fontName='NanumGothic', fontSize=18, leading=14))
        styles.add(ParagraphStyle(name='KoreanBasic', fontName='NanumGothic', fontSize=16, leading=14))

        # 문서에 추가할 요소 리스트
        elements = []

        # 제목 추가 - 수정된 스타일을 적용
        report_title = Paragraph("PC 보안 점검 결과 보고서", styles['KoreanTitle'])
        elements.append(report_title)
        elements.append(Spacer(1, 12))

        # 1. 사용자 정보 추가
        user_info_title = Paragraph('1. 사용자 정보', styles['Korean'])
        elements.append(user_info_title)
        elements.append(Spacer(1, 12))

        # 컴퓨터 이름 가져오기
        computer_name = socket.gethostname()

        # 운영체제 정보 가져오기
        os_info = platform.platform()

        # 호스트의 IP 주소 가져오기
        ip_address = socket.gethostbyname(socket.gethostname())

        # 배치 파일 실행하여 결과 가져오기
        process = subprocess.Popen(r'D:\pythonProject\userinfo.bat.bat', stdout=subprocess.PIPE)
        output, error = process.communicate()
        user_info = output.decode('cp949').strip()

        # 사용자 정보 및 기타 변수 설정
        self.computer_name = computer_name
        self.os_info = os_info

        # 사용자 정보 표 작성
        user_info_data = [
            ['컴퓨터 이름', self.computer_name],
            ['IP Address', ip_address],
            ['사용자 정보', user_info],
            ['운영체제 정보', self.os_info]
        ]

        user_info_table = Table(user_info_data, colWidths=[200, 400])
        user_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(user_info_table)
        elements.append(Spacer(1, 12))

        section_title = Paragraph('2. PC 보안 점검 결과(요약)', styles['Korean'])
        elements.append(section_title)
        elements.append(Spacer(1, 12))  # 텍스트와 표 사이에 공간 추가

        elements.append(Spacer(100, 0))

        basic_info_data = [
            ['점검 완료 시간', self.completion_time],
            ['점검 결과 요약', f"{self.summary_data['안전한 항목']}건 양호 / {self.summary_data['취약한 항목']}건 미흡 / {self.summary_data['점검 불가 항목']}건 점검 불가"],
            ['점검 결과 점수', f"{self.total_score}점"]
        ]

        # Table 객체 생성
        basic_info_table = Table(basic_info_data, colWidths=[200, 400])

        # 표 스타일 설정
        table_style = TableStyle([
            # 첫 번째 열의 배경색을 회색으로 설정
            ('BACKGROUND', (0, 0), (0, -1), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 모든 텍스트 색상을 검은색으로 설정
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 모든 셀의 텍스트를 왼쪽 정렬
            ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),  # 모든 셀에 한글 폰트 지정
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # 모든 셀의 폰트 크기 설정
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # 모든 셀의 아래쪽 여백 설정
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # 표의 테두리 설정
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 표의 그리드 설정
        ])
        basic_info_table.setStyle(table_style)

        # elements 리스트에 표 추가
        elements.append(basic_info_table)
        elements.append(Spacer(1, 12))

        section_title = Paragraph('3. PC 보안 점검 결과(세부)', styles['Korean'])
        elements.append(section_title)
        elements.append(Spacer(1, 12))  # 텍스트와 표 사이에 공간 추가

        section_title = Paragraph('&nbsp;&nbsp;가. 자동 보안 점검 결과', styles['Korean'])
        elements.append(section_title)
        elements.append(Spacer(1, 12))  # 텍스트와 표 사이에 공간 추가

        # 첫 번째 테이블의 데이터 준비
        table_data = [['카테고리', '점검 항목', '결과']]
        for row in range(self.result_table.rowCount()):
            category = self.result_table.item(row, 0).text()
            item = self.result_table.item(row, 1).text()
            result = self.result_table.item(row, 2).text()
            table_data.append([category, item, result])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),
            ('BORDER', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        first_table = Table(table_data, colWidths=[150, 300, 150])
        first_table.setStyle(table_style)
        elements.append(first_table)

        def truncate_text(text, max_length=40):
            """텍스트를 최대 길이에 맞게 자르고 '...'을 추가하는 함수"""
            if len(text) > max_length:
                return text[:max_length - 3] + "..."
            return text

        section_title = Paragraph('&nbsp;&nbsp;다. (의심)고객, 개인정보 파일 보유 현황', styles['Korean'])
        elements.append(section_title)
        elements.append(Spacer(1, 12))  # 텍스트와 표 사이에 공간 추가

        # 두 번째 테이블 데이터 및 스타일 설정
        raw_data = self.customer_info_widget.get_result_data()
        second_table_data = [['파일명', '수정 날짜', '경로']]  # 테이블 헤더

        for row in raw_data:
            truncated_row = [truncate_text(item) for item in row]  # 각 항목을 truncate_text 함수로 처리
            second_table_data.append(truncated_row)

        second_table = Table(second_table_data, colWidths=[300, 130, 300], repeatRows=1)
        second_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 왼쪽 정렬
            ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),  # 한글 폰트 사용
            ('BORDER', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(second_table)

        # PDF 문서 생성
        doc.build(elements)

        # 보안 점검 결과를 JSON 파일에 저장
        self.save_security_check_result(self.completion_time, self.summary_data, self.total_score)

        self.report_label.setText("보고서 저장: Success")

class SummaryDialog(QDialog):
    def __init__(self, summary_data, parent=None):
        super(SummaryDialog, self).__init__(parent)
        self.setWindowTitle('점검 완료')
        self.setFixedSize(350, 150)  # 결과 창의 크기를 설정

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # 상태 레이블과 수치를 표시하는 레이아웃
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.create_status_label('안전', 'green', summary_data.get('안전한 항목', 0)))
        status_layout.addWidget(self.create_status_label('취약', 'red', summary_data.get('취약한 항목', 0)))
        status_layout.addWidget(self.create_status_label('점검 필요', 'orange', summary_data.get('점검 불가 항목', 0)))
        layout.addLayout(status_layout)

        # 상태 메시지
        status_message = QLabel("전체 결과 개수를 확인하려면 버튼을 클릭하세요.")
        status_message.setFont(QFont('Arial', 10))
        layout.addWidget(status_message)

        # 확인 버튼
        close_button = QPushButton('확인', self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        # 세로 구분선 추가
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # 점검 완료 시간
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        completion_time = QLabel(f"점검 결과 생성 완료 시간({current_time})")
        completion_time.setFont(QFont('Arial', 8))
        layout.addWidget(completion_time)

    def create_status_label(self, text, color, count):
        label = QLabel(f"{text}\n{count} 개")
        label.setStyleSheet(f"background-color: {color}; color: white; padding: 5px; border-radius: 5px;")
        label.setAlignment(Qt.AlignCenter)
        return label

# Main Layout
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PC 보안 점검 프로그램')
        self.resize(1074, 518)  # 크기 조정

        # 메뉴 바 생성
        self.menu_bar = self.menuBar()

        # 메뉴 항목 생성
        self.home_menu = self.menu_bar.addMenu('HOME')
        self.pc_check_menu = self.menu_bar.addMenu('PC 점검')
        self.customer_info_menu = self.menu_bar.addMenu('고객 정보 검색 도구')
        self.PC_optimization_menu = self.menu_bar.addMenu('PC 최적화')
        self.interview_check_menu = self.menu_bar.addMenu('인터뷰 점검 항목')  # '인터뷰 점검 항목' 메뉴 생성
        self.etc_menu = self.menu_bar.addMenu('사용법')

        # 중앙에 위치할 스택 위젯 생성
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # HOME 위젯 생성 및 스택 위젯에 추가
        self.home_widget = HomeWidget()
        self.stacked_widget.addWidget(self.home_widget)

        # CustomerInfoSearchWidget 인스턴스 생성
        self.customer_info_search_page = CustomerInfoSearchWidget()
        self.stacked_widget.addWidget(self.customer_info_search_page)

        # VulnerabilityScanner 인스턴스 생성 및 CustomerInfoSearchWidget 인스턴스 전달
        self.vulnerability_scanner_page = VulnerabilityScanner(customer_info_widget=self.customer_info_search_page)
        self.stacked_widget.addWidget(self.vulnerability_scanner_page)

        # PC 최적화 위젯 생성 및 스택 위젯에 추가
        self.pc_optimization_widget = PCOptimizationWidget()
        self.stacked_widget.addWidget(self.pc_optimization_widget)

        # '인터뷰 점검 항목' 위젯 생성 및 스택 위젯에 추가
        self.interview_check_widget = InterviewCheckWidget()  # InterviewCheckWidget 클래스를 정의해야 합니다.
        self.stacked_widget.addWidget(self.interview_check_widget)

        # 메뉴 액션 추가 및 연결
        self.home_action = self.home_menu.addAction('Home Page')
        self.pc_check_action = self.pc_check_menu.addAction('PC 보안 점검')
        self.customer_info_action = self.customer_info_menu.addAction('고객 정보 검색')
        self.PC_optimization_menu_action = self.PC_optimization_menu.addAction('PC 최적화')
        self.interview_check_action = self.interview_check_menu.addAction('인터뷰 점검')  # '인터뷰 점검' 액션 생성
        self.etc_action = self.etc_menu.addAction('사용법')

        # 액션에 메서드 연결
        self.home_action.triggered.connect(lambda: self.change_page(0))
        self.customer_info_action.triggered.connect(lambda: self.change_page(1))
        self.pc_check_action.triggered.connect(lambda: self.change_page(2))
        self.PC_optimization_menu_action.triggered.connect(lambda: self.change_page(3))
        self.interview_check_action.triggered.connect(lambda: self.change_page(4))  # '인터뷰 점검' 액션에 메서드 연결
        self.etc_action.triggered.connect(lambda: self.change_page(5))

    def change_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

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
        file_path = 'C:\\security_check_history.json'
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
                image_path = r'D:\pythonProject\green.png'
            elif latest_score > 70:
                background_color = QColor('yellow')
                image_path = r'D:\pythonProject\yellow.png'
            else:
                background_color = QColor('red')
                image_path = r'D:\pythonProject\sred.png'
        else:
            background_color = QColor('gray')
            image_path = None  # 점수 정보가 없을 때 이미지 없음

        # ScoreLabel 인스턴스 생성 및 스코어보드 레이아웃에 추가
        score_label = ScoreLabel(latest_score, image_path, background_color)
        self.scoreboard_layout.addWidget(score_label)

    def update_recent_inspection_graph(self):
        # Read inspection data from JSON file
        file_path = 'C:\\security_check_history.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                history = json.load(file)
                latest_inspection = history[-1]['summary']  # Most recent inspection summary information
        except Exception as e:
            print(e)
            latest_inspection = {'안전한 항목': 0, '취약한 항목': 0, '점검 불가 항목': 0}

        # 막대 그래프 데이터 설정
        set0 = QBarSet('검사 항목')
        set0.append([latest_inspection['안전한 항목'], latest_inspection['취약한 항목'], latest_inspection['점검 불가 항목']])

        # 막대 그래프 시리즈 생성
        series = QBarSeries()
        series.append(set0)

        # 차트 생성 및 설정
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('최근 검사 결과')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # 축 설정
        categories = ['안전 항목', '취약 항목', '검사 불가 항목']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max(latest_inspection.values()) + 1) # Y축 범위 설정
        chart.setAxisY(axisY, series)

        chart.legend().hide()
        axisX.setGridLineVisible(False)
        axisY.setGridLineVisible(False)

        # 차트 뷰 생성 및 레이아웃에 추가
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # 기존 레이아웃에 있는 위젯들 제거
        for i in reversed(range(self.recent_inspection_layout.count())):
            self.recent_inspection_layout.itemAt(i).widget().setParent(None)

        self.recent_inspection_layout.addWidget(chartView)

    def update_security_check_trend(self):
        try:
            with open('C:\\security_check_history.json', 'r', encoding='utf-8') as file:
                history = json.load(file)

            # Data extract
            data = []  # (x, y) List to contain data points

            for entry in history:
                completion_time = entry["completion_time"]
                total_score = entry["total_score"]

                # Add data only if completion_time is not null
                if completion_time is not None:
                    # 문자열에서 QDateTime 객체로 변환
                    x = QDateTime.fromString(completion_time, "yyyy-MM-dd HH:mm:ss")
                    data.append((x, total_score))

            # Sort data by date
            data.sort(key=lambda x: x[0])

            # Bar graph data settings
            set0 = QBarSet('Total Score')  # 하나의 막대 그래프 세트 생성

            for point in data:
                x, y = point
                set0.append(y)  # Y 축 데이터 추가

            # Create a bar graph series
            series = QBarSeries()
            series.append(set0)

            # Create and set charts
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("점검 점수 추이")
            chart.setAnimationOptions(QChart.AllAnimations)

            # X-axis settings
            axisX = QBarCategoryAxis()
            categories = [x.toString('MM월 dd일 HH:mm') for x, _ in data]  # X 축 레이블 생성
            axisX.append(categories)  # X 축 레이블 추가
            chart.addAxis(axisX, Qt.AlignBottom)
            series.attachAxis(axisX)

            # Y axis settings
            axisY = QValueAxis()
            axisY.setLabelFormat("%.1f")
            chart.addAxis(axisY, Qt.AlignLeft)
            series.attachAxis(axisY)

            chart.legend().hide()
            axisX.setGridLineVisible(False)
            axisY.setGridLineVisible(False)

            # Chart view creation and rendering settings
            chartView = QChartView(chart)
            chartView.setRenderHint(QPainter.Antialiasing)

            # Remove widgets from existing layout and add new chart view
            for i in reversed(range(self.security_check_trend_layout.count())):
                self.security_check_trend_layout.itemAt(i).widget().setParent(None)

            self.security_check_trend_layout.addWidget(chartView)

        except Exception as e:
            print(e)

class ScoreLabel(QLabel):
    def __init__(self, score, image_path, background_color, parent=None):
        super().__init__(parent)
        self.score = score
        self.image_path = image_path
        self.background_color = background_color
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(200, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        # 배경색 채우기
        painter.fillRect(self.rect(), self.background_color)
        # 이미지 그리기
        if self.image_path:
            image = QPixmap(self.image_path).scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # 이미지 위치를 중앙에 맞추기 위한 계산
            iw, ih = image.width(), image.height()
            ix, iy = (self.width() - iw) // 2, (self.height() - ih) // 2
            iy -= 90 # 이미지를 위로 10픽셀 이동
            painter.drawPixmap(ix, iy, iw, ih, image)
        # 텍스트 그리기
        painter.setPen(QColor('white'))
        painter.setFont(QFont('Arial', 8, QFont.Bold))  # 폰트 크기를 조정하여 상단 텍스트에 적용
        painter.drawText(self.rect().adjusted(0, 50, 0, 0), Qt.AlignCenter, "최근 PC 점검 점수")  # 상단 텍스트 위치 조정
        painter.setFont(QFont('Arial', 20, QFont.Bold))
        # painter.drawText(self.rect(), Qt.AlignCenter, f"{self.score}점")
        painter.drawText(self.rect().adjusted(0, 100, 0, 0), Qt.AlignCenter, f"{self.score}점")
        painter.end()

class CustomerInfoSearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 메인 수평 레이아웃 설정
        main_layout = QHBoxLayout(self)

        # 왼쪽 레이아웃 설정 (3개의 세부 레이아웃 포함)
        left_layout = QVBoxLayout()

        # 1번 레이아웃: 레이블을 위한 레이아웃
        label_layout = QVBoxLayout()

        self.label = QLabel("※ 개인정보 의심 파일을 검색하는 Tool입니다.")
        self.label.setStyleSheet("font-weight: bold; color: black;")
        label_layout.addWidget(self.label)

        label_layout.setSpacing(10)

        self.additional_label = QLabel("▶ 검색 경로: C,D 드라이브")
        self.additional_label.setStyleSheet("font-size: 12px; color: black;")
        label_layout.addWidget(self.additional_label)

        self.additional2_label = QLabel("▶ 검색단어: 고객 및 개인정보 관련 단어")
        self.additional2_label.setStyleSheet("font-size: 12px; color: black;")
        label_layout.addWidget(self.additional2_label)

        left_layout.addLayout(label_layout)
        label_layout.addStretch(1)  # Stretch factor 추가

        # 2번 레이아웃: 버튼을 위한 레이아웃
        button_layout = QVBoxLayout()
        self.search_button = QPushButton("검색 시작")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.search_button.clicked.connect(self.start_search)
        button_layout.addWidget(self.search_button)

        self.stop_button = QPushButton("검색 중단")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.stop_button.clicked.connect(self.stop_search)
        button_layout.addWidget(self.stop_button)

        self.clear_button = QPushButton("결과 초기화")
        self.clear_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF;
                        color: black;
                        border-radius: 5px;
                        padding: 8px;
                        border: 1px solid #9E9E9E;
                    }
                    QPushButton:hover {
                        background-color: #eeeeee;
                    }
                """)
        self.clear_button.clicked.connect(self.clear_results)
        button_layout.addWidget(self.clear_button)

        self.delete_button = QPushButton("파일 삭제")
        self.delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF;
                        color: black;
                        border-radius: 5px;
                        padding: 8px;
                        border: 1px solid #9E9E9E;
                    }
                    QPushButton:hover {
                        background-color: #eeeeee;
                    }
                """)
        self.delete_button.clicked.connect(self.delete_files)
        button_layout.addWidget(self.delete_button)

        self.open_button = QPushButton("경로 열기")
        self.open_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF;
                        color: black;
                        border-radius: 5px;
                        padding: 8px;
                        border: 1px solid #9E9E9E;
                    }
                    QPushButton:hover {
                        background-color: #eeeeee;
                    }
                """)
        self.open_button.clicked.connect(self.open_folder_path)
        button_layout.addWidget(self.open_button)

        left_layout.addLayout(button_layout)

        status_layout = QVBoxLayout()
        #status_layout.setSpacing(10)

        # 3번 레이아웃: 상태 레이블을 위한 레이아웃
        status_layout = QVBoxLayout()
        self.search_start_time_label = QLabel("검색 시작 시간: 대기중")
        self.search_start_time_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(self.search_start_time_label)
        status_layout.setSpacing(10)
        self.search_end_time_label = QLabel("검색 종료 시간: 대기중")
        self.search_end_time_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(self.search_end_time_label)
        status_layout.setSpacing(10)
        self.status_label = QLabel("상태: 대기중")
        self.status_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(self.status_label)
        left_layout.addLayout(status_layout)

        main_layout.addLayout(left_layout)

        # 오른쪽 레이아웃 설정
        right_layout = QVBoxLayout()

        # 1번 레이아웃: "경로 표시" 라벨을 위한 레이아웃
        path_label_layout = QVBoxLayout()
        self.path_label = QLabel("※ 경로 표시: ")
        self.path_label.setAlignment(Qt.AlignLeft)
        self.path_label.setStyleSheet("font-size: 12px; color: black;")
        self.path_label.setWordWrap(True)  # 텍스트가 길 경우 자동으로 줄바꿈
        path_label_layout.addWidget(self.path_label)
        right_layout.addLayout(path_label_layout)

        right_layout.addSpacing(10)

        # 2번 레이아웃: 결과 테이블을 위한 레이아웃
        result_table_layout = QVBoxLayout()
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["파일명", "수정 날짜", "경로"])
        # 각 열의 너비 설정
        self.result_table.setColumnWidth(0, 150)  # '파일명' 열 너비 설정
        self.result_table.setColumnWidth(1, 150)  # '수정 날짜' 열 너비 설정
        self.result_table.setColumnWidth(2, 500)  # '경로' 열 너비 설정
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        result_table_layout.addWidget(self.result_table)
        self.result_table.itemSelectionChanged.connect(self.handle_selection_changed)
        self.result_table.horizontalHeader().sectionClicked.connect(self.handle_header_clicked) # '수정 날짜' 열을 클릭했을 때 정렬을 처리하는 이벤트 핸들러 연결
        self.date_sort_order = Qt.DescendingOrder # '수정 날짜' 열의 정렬 방향을 저장할 변수
        right_layout.addLayout(result_table_layout)

        main_layout.addLayout(right_layout)

        # 현재 선택된 항목에 대한 정보를 저장할 변수
        self.selected_file_path = None

        # 검색 스레드 및 플래그 초기화
        self.search_thread = None
        self.stop_search_flag = False

    def start_search(self):
        print("검색 시작 버튼 클릭")
        self.search_start_time_label.setText(f"검색 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.status_label.setText("상태: 검사중")
        # 검색 스레드가 없거나 실행 중이지 않은 경우
        if self.search_thread is None or not self.search_thread.is_alive():
            self.stop_search_flag = False
            # 결과 테이블의 내용을 초기화합니다.
            self.result_table.setRowCount(0) # 결과 테이블의 내용을 초기화
            # 새 검색 스레드를 시작합니다.
            self.search_thread = threading.Thread(target=self.search_files)
            self.search_thread.start()
        else:
            QMessageBox.information(self, "검색 중", "이미 검색이 진행 중입니다.")

    def search_files(self):
        print("파일 검색 시작")
        extensions = ['csv', 'pdf', 'doc', 'docx', 'xls', 'txt', 'zip', 'jpg', 'jpeg', 'png', 'ppt', 'pptx', 'hwp', 'bmp', 'tiff', 'html']
        keywords = ['고객', 'voc', '통화 품질', '상담', '목록', '리스트', '퀄리티', 'quality', '대외', '만족도', '보상', '작업지시', '통계', '민원', '임대', '현황', '계약', '통장', '사본', '협의', '동의', '품의', '주민', '등본', '면허', '증명', '공사현장', '신입', '구성원', '직원', '연락', '퇴직', '퇴사', '이력서', '가족', '원천징수', '소득', '연말', '급여', '인사', '평가', '자격', '연락처', '전화', '번호', '주소', '군부대', '건물주', '내역', '출입', '전자파', '법인', '투자']
        drives = ['D:/']

        for drive in drives:
            for root, dirs, files in os.walk(drive):
                for file in files:
                    if self.stop_search_flag:
                        print("검색이 중단되었습니다.")
                        return
                    if any(file.endswith(ext) for ext in extensions) and \
                       any(keyword in file for keyword in keywords):
                        filepath = os.path.join(root, file)
                        # 결과 테이블에 파일 정보 추가
                        self.add_file_to_table(filepath)
                if self.stop_search_flag:
                    print("Search aborted.")
                    return
        print("File search completed.")
        self.search_end_time_label.setText(f"검색 종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.status_label.setText("상태: 검사완료")

    def add_file_to_table(self, filepath):
        # 파일의 수정 날짜를 가져옴
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')

        # 테이블에 행 추가
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)

        # 테이블에 파일 정보 추가 및 편집 불가 설정
        file_item = QTableWidgetItem(os.path.basename(filepath))
        file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)
        self.result_table.setItem(row_position, 0, file_item)

        mod_date_item = QTableWidgetItem(mod_time)
        mod_date_item.setFlags(mod_date_item.flags() & ~Qt.ItemIsEditable)
        self.result_table.setItem(row_position, 1, mod_date_item)

        path_item = QTableWidgetItem(filepath)
        path_item.setFlags(path_item.flags() & ~Qt.ItemIsEditable)
        self.result_table.setItem(row_position, 2, path_item)

    def get_result_data(self):
        data = []
        for row in range(self.result_table.rowCount()):
            row_data = []
            for column in range(self.result_table.columnCount()):
                item = self.result_table.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        return data

    # 테이블의 내용을 반환하는 메소드 추가
    def get_table_content(self):
        table_content = []
        for row in range(self.result_table.rowCount()):
            row_data = []
            for column in range(self.result_table.columnCount()):
                item = self.result_table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            table_content.append(row_data)
        return table_content

    def handle_selection_changed(self):
        selected_items = self.result_table.selectedItems()
        if selected_items:
            row = self.result_table.currentRow()
            file_path = self.result_table.item(row, 2).text()  # 경로 열에서 파일 경로를 가져옵니다.
            self.path_label.setText(f"경로 표시: {file_path}")  # path_label 레이블을 업데이트합니다.
            self.selected_file_path = file_path
            print(f"Selected file path: {self.selected_file_path}")
        else:
            self.path_label.setText("경로 표시: ")  # 선택된 항목이 없을 때 기본 텍스트를 표시합니다.

    def delete_files(self):
        selected_items = self.result_table.selectedItems()
        if selected_items:
            confirm = QMessageBox.question(self, "삭제 확인", "정말로 이 파일을 삭제하시겠습니까?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                row = self.result_table.currentRow()
                file_path = self.result_table.item(row, 2).text()
                try:
                    os.remove(file_path)
                    self.result_table.removeRow(row)
                    QMessageBox.information(self, "성공", "파일이 삭제되었습니다.")
                except Exception as e:
                    QMessageBox.warning(self, "오류", f"파일 삭제 중 오류가 발생했습니다: {e}")
        else:
            QMessageBox.warning(self, "선택된 파일 없음", "삭제할 파일을 선택해 주세요.")

    def open_folder_path(self):
        if self.selected_file_path:
            # 파일 경로에서 폴더 경로 추출
            folder_path = os.path.dirname(self.selected_file_path)
            # print("Opening folder:", folder_path)  # 디버깅을 위한 경로 출력
            # 폴더 열기
            try:
                os.startfile(folder_path)  # os.startfile 함수를 사용하여 폴더 열기
            except Exception as e:
                print("Error opening folder:", e)
        else:
            QMessageBox.warning(self, "Error", "No file selected.")

    def stop_search(self):
        self.stop_search_flag = True

    def clear_results(self):
        self.result_table.setRowCount(0)

    def handle_header_clicked(self, logical_index):
        """
        열 헤더 클릭 이벤트 처리
        """
        if logical_index == 1:  # '수정 날짜' 열을 클릭한 경우
            # '수정 날짜' 열을 클릭하여 정렬 방향을 반전시킴
            self.date_sort_order = Qt.DescendingOrder if self.date_sort_order == Qt.AscendingOrder else Qt.AscendingOrder
            # '수정 날짜' 열을 클릭한 열로 설정하여 정렬
            self.result_table.sortItems(logical_index, self.date_sort_order)

class PCOptimizationWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create vertical layout
        self.vertical_layout = QVBoxLayout()

        # Create horizontal layout
        self.button_layout = QHBoxLayout()

        # Create a ‘Clear all items’ button
        self.clear_all_button = QPushButton('전체 항목 지우기')
        self.clear_all_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF;
                        color: black;
                        border-radius: 5px;
                        padding: 8px;
                        border: 1px solid #9E9E9E;
                    }
                    QPushButton:hover {
                        background-color: #eeeeee;
                    }
                """)
        self.button_layout.addWidget(self.clear_all_button)

        # Create a ‘Clear selected items’ button
        self.clear_selected_button = QPushButton('선택한 항목 지우기')
        self.clear_selected_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF;
                        color: black;
                        border-radius: 5px;
                        padding: 8px;
                        border: 1px solid #9E9E9E;
                    }
                    QPushButton:hover {
                        background-color: #eeeeee;
                    }
                """)
        self.button_layout.addWidget(self.clear_selected_button)

        # Add button layout to vertical layout
        self.vertical_layout.addLayout(self.button_layout)

        # Create Tree Widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels([' '])

        # Add 'Windows System' item
        windows_system_item = QTreeWidgetItem(self.tree_widget, ['Windows System'])

        # Add 'Internet' item
        internet_item = QTreeWidgetItem(self.tree_widget, ['Internet Browser'])

        # Add optimization items for each item
        optimization_items1 = [
            'Windows 임시 파일',
            '휴지통'
        ]

        optimization_items2 = [
            '크롬:인터넷 임시 파일/쿠키/암호 자동 완성 기록(수동)',
            '엣지:인터넷 임시 파일/쿠키/암호 자동 완성 기록(수동)',
        ]

        for item in optimization_items1:
            item_widget = QTreeWidgetItem(windows_system_item, [item])
            item_widget.setCheckState(0, Qt.Unchecked)
            item_widget.item_type = 'file'  # Indication that the folder will be deleted

        for item in optimization_items2:
            item_widget = QTreeWidgetItem(internet_item, [item])
            item_widget.setCheckState(0, Qt.Unchecked)

        # Add a slot connected to the 'Clear selected items' button
        self.clear_selected_button.clicked.connect(self.delete_selected_items)

        # Clear All Items 버튼을 클릭했을 때 실행할 함수를 연결합니다.
        self.clear_all_button.clicked.connect(self.clear_all_items)

        # Add Tree Widget to vertical layout
        self.vertical_layout.addWidget(self.tree_widget)

        # Set the layout of the widget
        self.setLayout(self.vertical_layout)

    def delete_selected_items(self):
        checked_items = self.get_checked_items()

        if not checked_items:
            QMessageBox.warning(self, "No Items Selected", "선택한 항목이 없습니다.")
            return

        confirm = QMessageBox.question(self, "확인창", "정말 선택 항목 지우시겠습니까?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            for item in checked_items:
                print(f'Processing item: {item.text(0)}')
                if item.text(0) == 'Windows 임시 파일':
                    self.delete_windows_temporary_files()
                elif item.text(0) == '휴지통':
                    self.empty_trash()
                elif item.text(0) == '크롬:인터넷 임시 파일/쿠키/암호 자동 완성 기록(수동)':
                    self.open_chrome_clear_browsing_data()
                elif item.text(0) == '엣지:인터넷 임시 파일/쿠키/암호 자동 완성 기록(수동)':
                    self.open_edge_clear_browsing_data()
                print(f'항목 처리 완료: {item.text(0)}')

                # 항목 삭제가 완료되면 안내 메시지 표시
                QMessageBox.information(self, "완료", f"{item.text(0)} 항목이 삭제되었습니다.")

    def get_checked_items(self):
        checked_items = []
        for i in range(self.tree_widget.topLevelItemCount()):
            top_item = self.tree_widget.topLevelItem(i)
            for j in range(top_item.childCount()):
                child_item = top_item.child(j)
                if child_item.checkState(0) == Qt.Checked:
                    checked_items.append(child_item)
        return checked_items

    def delete_windows_temporary_files(self):
        folder_path = r'C:\Users\user\AppData\Local\Temp'
        try:
            file_list = os.listdir(folder_path)
            print(f'디렉토리 내 파일: {file_list}')
            for filename in file_list:
                file_path = os.path.join(folder_path, filename)
                try:
                    os.remove(file_path)
                    print(f'파일 삭제됨: {file_path}')
                except PermissionError as pe:
                    print(f'권한 오류, 파일 유지됨: {file_path} - {pe}')
                except Exception as e:
                    print(f'파일 삭제 오류: {file_path} - {e}')
        except FileNotFoundError:
            print(f'폴더를 찾을 수 없음: {folder_path}')
        except Exception as e:
            print(f'오류: {e}')

    def empty_trash(self):
        print('휴지통 비우는 중...')
        try:
            # Windows 휴지통 비우기 명령 실행
            result = subprocess.run("powershell -command \"Clear-RecycleBin -Confirm:$false\"", check=True, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print('휴지통이 비워졌습니다.')
        except subprocess.SubprocessError as e:
            print(f'휴지통 비우기 오류: {e}')

    def keep_browser_open(driver):
        while True:  # 'whileTrue:'를 'while True:'로 수정
            try:
                # 현재 탭의 제목을 확인하여 브라우저가 열려 있는지 확인
                title = driver.title
            except Exception as e:
                # 브라우저가 닫혔으면 while 루프 종료
                break

    def open_chrome_clear_browsing_data(self):
        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome()

        # Navigate to the Chrome settings page to clear browsing data
        url = "chrome://settings/clearBrowserData"
        driver.get(url)

        # Chrome 브라우저가 종료될 때까지 대기
        driver.wait()

    def open_chrome_clear_browsing_data(self):
        try:
            # Initialize the Chrome WebDriver
            driver = webdriver.Chrome()

            # Navigate to the Chrome settings page to clear browsing data
            url = "chrome://settings/clearBrowserData"
            driver.get(url)

            # Wait until Chrome browser quits
            self.keep_browser_open(driver)
        except Exception as e:
            print(f"오류 발생: {e}")

    def open_edge_clear_browsing_data(self):
        try:
            # Initialize the Edge WebDriver
            driver = webdriver.Edge()

            # Navigate to the Edge settings page to clear browsing data
            url = "edge://settings/clearBrowserData"
            driver.get(url)

            # Wait until Edge browser quits
            self.keep_browser_open(driver)
        except Exception as e:
            print(f"오류 발생: {e}")

    def keep_browser_open(self, driver):
        while True:
            try:
                # Check if the browser is open by checking the title of the current tab
                title = driver.title
            except Exception as e:
                # If the browser is closed, the while loop ends
                break

    # 모든 항목을 지우는 함수를 정의합니다.
    def clear_all_items(self):
        confirm = QMessageBox.question(self, "확인창", "모든 항목을 지우시겠습니까?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.delete_windows_temporary_files()
            time.sleep(5)
            self.empty_trash()
            time.sleep(2)
            self.open_chrome_clear_browsing_data()
            time.sleep(2)
            self.open_edge_clear_browsing_data()
            QMessageBox.information(self, "완료", "모든 항목이 삭제되었습니다.")

class InterviewCheckWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        # 레이아웃 설정
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 테이블 위젯 설정
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)  # 열의 수 설정
        self.tableWidget.setHorizontalHeaderLabels(["구분", "점검 항목", "결과"])
        self.tableWidget.setColumnWidth(0, 200)  # "구분" 열의 너비를 100픽셀로 설정
        self.tableWidget.setColumnWidth(1, 650)  # "점검 항목" 열의 너비를 200픽셀로 설정
        self.tableWidget.setColumnWidth(2, 150)  # "결과" 열의 너비를 150픽셀로 설정

        # 예제 데이터 추가
        example_data = [
            ("고객정보보호", "고객/개인정보 파일(하드 카피본 포함) 정리 및 Masking 처리 유무\n※ 업무중인 경우: MAX 3개월까지 보관 가능 단, 업무 종료 후 즉시 파기(evEraser를 이용한 완전 삭제 시행)\n-파일 내 불필요한 고객정보는 SKT 기준에 부합하는 Masking 처리 후 보관 시행\n※가족/개인/구성원 정보 또한 보관 금지, 업무상 필요 시 사용하고 업무 종료 즉시 파기", ""),
            ("고객정보보호", "고객정보 취급자 망 분리 상태 유무\n※Swing, RealT 시스템 사용자 중 고객정보 다운로드 가능자/권한자는 망분리 솔루션(VM, Fort, myDesk) 필수 설치", ""),
            ("고객정보보호", "계약서/중요문서 등 보관상태 및 출력/복사/파기 현황 점검\n※ 업무 중인 계약서 및 중요문서는 시건장치가 있는 곳에 보관해야 하며, 업무 종료 시 즉시 파쇄\n※ 계약서 출력/복사 시 최종 파쇄까지 관리를 해야 함(관리대장 기재)\n※ 개인정보를 수집하는 중요문서 같은 경우 고객정보보호법 의거 고객정보 수집에 관한 이용 동의서 징구 유무 확인", ""),
            ("고객정보보호", "이글아이 자가진단 시행 여부 확인\n※ 매일 PC 종료 전 자동 검사 검출 내역 확인 및 파일 관리 시행", ""),
            ("고객정보보호", "NateOn Biz 쪽지함 및 E-Mail내 고객정보 유무 확인\n※ Biz 쪽지함 및 E-Mail내 첨부된 고객정보 파일 또는 내용 유무를 확인하고 업무 종료 시 즉시 삭제 시행\n※ E-Mail 자동 저장 프로그램 사용 금지\n - 업무상 필요한 경우 메일 개별 저장 시행 (단, 고객정보가 담긴 메일은 저장 금지)", ""),
            ("고객정보보호", "Real.T/ERP 사용자 불필요 물건 및 고객 정보 조회/다운/카피 금지\n※ 업무상 불필요한 고객정보는 절대 조회나 다운로드 하지 않으며 복사본 이용 또한 금지 \n - 파일/문서상 고객정보 확인시 Making 처리 필수 (파일 스캔본 포함)", ""),
        ]

        self.tableWidget.setRowCount(len(example_data))  # 행의 수 설정

        for row, (id, question, result) in enumerate(example_data):
            id_item = QTableWidgetItem(id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)  # "구분" 열 편집 비활성화
            self.tableWidget.setItem(row, 0, id_item)

            question_item = QTableWidgetItem(question)
            question_item.setFlags(question_item.flags() & ~Qt.ItemIsEditable)  # "점검 항목" 열 편집 비활성화
            self.tableWidget.setItem(row, 1, question_item)

            combo = QComboBox()
            combo.addItem("")  # 초기 선택 항목을 빈 문자열로 설정
            combo.addItem("양호")
            combo.addItem("미흡")
            combo.addItem("해당사항 없음")
            self.tableWidget.setCellWidget(row, 2, combo)

        self.tableWidget.resizeRowsToContents()  # 행 높이를 셀의 내용에 맞게 조정

        layout.addWidget(self.tableWidget)

# Entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())