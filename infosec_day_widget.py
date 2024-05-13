import os
import json
from reportlab.lib import colors
import socket
import subprocess
import platform
from datetime import datetime

from interview_check_widget import InterviewCheckWidget
from vulnerability_scanner import VulnerabilityScanner
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox
from reportlab.lib.pagesizes import A3
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class InfoSecDayWidget(QWidget):
    def __init__(self, vulnerability_scanner, interview_check_widget, customer_info_search_widget, parent=None):
        super().__init__(parent)

        self.vulnerability_scanner = vulnerability_scanner
        self.interview_check_widget = interview_check_widget
        self.customer_info_search_widget = customer_info_search_widget

        # '보고서 생성' 버튼 생성
        self.generate_report_button = QPushButton('보고서 생성', self)
        self.generate_report_button.setStyleSheet("""
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
        self.generate_report_button.setFixedWidth(200)
        self.generate_report_button.clicked.connect(self.save_report)

        # '저장 경로 열기' 버튼 생성
        self.open_folder_button = QPushButton('저장 경로 열기', self)
        self.open_folder_button.setStyleSheet("""
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
        self.open_folder_button.setFixedWidth(200)
        self.open_folder_button.clicked.connect(self.open_report_folder)

        # 세로 레이아웃 생성 및 버튼 추가
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.generate_report_button)
        v_layout.addWidget(self.open_folder_button)

        # 가로 레이아웃 생성 및 세로 레이아웃 추가
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addLayout(v_layout)
        h_layout.addStretch()

        # 위젯의 레이아웃으로 설정
        self.setLayout(h_layout)

    def save_report(self):
        try:
            # 한글 폰트 파일 경로 설정 및 폰트 등록
            # korean_font_path = r'D:\pythonProject\나눔고딕.ttf'  # 실제 경로로 수정 필요
            korean_font_path = os.path.join(os.getcwd(), "_internal", "batch_files", "나눔고딕.ttf")
            pdfmetrics.registerFont(TTFont('NanumGothic', korean_font_path))

            # VulnerabilityScanner 인스턴스 생성
            scanner = VulnerabilityScanner()

            # # completion_time이 None인 경우 현재 시간을 설정
            if scanner.completion_time is None:
                scanner.completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # JSON 파일에서 데이터를 읽어옵니다.
            # with open(r'C:\\security_check_history.json', 'r', encoding='utf-8') as file:
            with open('security_check_history.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            last_record = data[-1]  # 가장 최근의 기록 가져오기

            # JSON 파일에서 가져온 값 사용
            scanner.completion_time = last_record['completion_time']
            scanner.summary_data = last_record['summary']
            scanner.total_score = last_record['total_score']

            # 배치 파일 실행하여 결과 가져오기
            batch_file_path = os.path.join(os.getcwd(), "_internal", "batch_files", "userinfo.bat.bat")
            process = subprocess.Popen(batch_file_path, stdout=subprocess.PIPE)
            output, error = process.communicate()
            user_info = output.decode('cp949').strip()

            user_info_modified = user_info.replace('/', '_')

            # PDF 파일 이름 설정
            pdf_file_name = f"점검결과_{user_info_modified}_{scanner.completion_time.replace(':', '_').replace(' ', '_')}.pdf"
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
            # batch_file_path = os.path.join(os.getcwd(), "_internal", "batch_files", "userinfo.bat.bat")
            # process = subprocess.Popen(batch_file_path, stdout=subprocess.PIPE)
            # output, error = process.communicate()
            # user_info = output.decode('cp949').strip()

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
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(user_info_table)
            elements.append(Spacer(1, 12))

            section_title = Paragraph('2. PC 보안 점검 결과(요약)', styles['Korean'])
            elements.append(section_title)
            elements.append(Spacer(1, 12))  # 텍스트와 표 사이에 공간 추가

            elements.append(Spacer(100, 0))

            self.completion_time = scanner.completion_time

            basic_info_data = [
                ['점검 완료 시간', scanner.completion_time],
                ['점검 결과 요약',
                 f"{scanner.summary_data['양호한 항목']}건 양호 / {scanner.summary_data['취약한 항목']}건 미흡 / {scanner.summary_data['점검 불가 항목']}건 점검 불가"],
                ['점검 결과 점수', f"{scanner.total_score}점"]
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
            for row in range(self.vulnerability_scanner.result_table.rowCount()):
                category = self.vulnerability_scanner.result_table.item(row, 0).text()
                item = self.vulnerability_scanner.result_table.item(row, 1).text()
                result = self.vulnerability_scanner.result_table.item(row, 2).text()
                table_data.append([category, item, result])

            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),
                ('BORDER', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            first_table = Table(table_data, colWidths=[190, 350, 190])
            first_table.setStyle(table_style)
            elements.append(first_table)

            def truncate_text(text, max_length=200):
                """텍스트를 최대 길이에 맞게 자르고 '...'을 추가하는 함수"""
                if len(text) > max_length:
                    return text[:max_length - 3] + "..."
                return text

            # '나. 인터뷰 점검 항목' 섹션 제목 추가
            section_title = Paragraph('&nbsp;&nbsp;나. 인터뷰 점검 항목', styles['Korean'])
            elements.append(section_title)
            elements.append(Spacer(1, 12))  # 텍스트와 표 사이에 공간 추가

            # InterviewCheckWidget 인스턴스 생성
            interview_check_widget = InterviewCheckWidget()
            # InterviewCheckWidget의 테이블 데이터 가져오기
            interview_table_data = self.interview_check_widget.get_table_data()  # 속성의 인스턴스를 사용

            # 가져온 데이터로 테이블 생성
            interview_table = Table(interview_table_data, colWidths=[115, 500, 115])

            # 테이블 스타일 설정
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),
                ('BORDER', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # 테이블 스타일 적용
            interview_table.setStyle(table_style)

            # elements 리스트에 테이블 추가
            elements.append(interview_table)

            def truncate_text(text, max_length=40):
                """텍스트를 최대 길이에 맞게 자르고 '...'을 추가하는 함수"""
                if len(text) > max_length:
                    return text[:max_length - 3] + "..."
                return text

            section_title = Paragraph('&nbsp;&nbsp;다. (의심)고객/개인정보 및 업무 문서 보유 현황', styles['Korean'])
            elements.append(section_title)
            elements.append(Spacer(1, 12))  # 텍스트와 표 사이에 공간 추가

            # 세 번째 테이블 데이터 및 스타일 설정
            raw_data = self.customer_info_search_widget.get_result_data()
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
            msg = QMessageBox()
            msg.setWindowTitle("보고서 생성")
            msg.setText("보고서 저장이 완료되었습니다.")
            msg.exec_()

        except Exception as e:
            # 팝업창 생성 및 표시
            msg = QMessageBox()
            msg.setWindowTitle("보고서 생성 오류")
            msg.setText(f"보고서 저장이 되지 않았습니다. 사유: {str(e)}")
            msg.exec_()

    def open_report_folder(self):
        # 보고서가 저장된 폴더 열기
        report_folder_path = os.getcwd()  # 보고서가 저장된 폴더 경로를 지정하세요
        os.startfile(report_folder_path)