# customer_info_search_widget.py
import string
import threading
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox, \
    QTableWidgetItem, QTableWidget, QLabel
import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class CustomerInfoSearchWidget(QWidget):
    def __init__(self):
        super().__init__()  # 부모 클래스의 __init__ 메소드 호출

        # 메인 수평 레이아웃 설정
        main_layout = QHBoxLayout(self)

        # 왼쪽 레이아웃 설정 (3개의 세부 레이아웃 포함)
        left_layout = QVBoxLayout()

        # 1번 레이아웃: 레이블을 위한 레이아웃
        label_layout = QVBoxLayout()

        self.label = QLabel("※ 개인정보 의심 파일 및 문서관리 Tool")
        self.label.setStyleSheet("font-weight: bold;")
        label_layout.addWidget(self.label)

        label_layout.setSpacing(10)

        self.additional_label = QLabel("▶ 검색 경로: PC 내 전체 드라이브")
        self.additional_label.setStyleSheet("font-size: 12px;")
        label_layout.addWidget(self.additional_label)

        # self.additional2_label = QLabel("▶ 검색단어: 고객 및 개인정보 관련 단어")
        self.additional2_label = QLabel(
            '<a href="link" style="text-decoration: none; color: white;">▶ 검색단어: 고객 및 개인정보 관련 단어(클릭)</a>')
        self.additional2_label.setStyleSheet("font-size: 12px;")
        self.additional2_label.setOpenExternalLinks(False)  # 외부 링크를 열지 않도록 설정
        self.additional2_label.linkActivated.connect(self.open_log_file)  # 링크 클릭 시 open_log_file 메소드 호출
        label_layout.addWidget(self.additional2_label)

        self.additional3_label = QLabel("▶ 5년 이상 지난 업무 문서/파일 삭제")
        self.additional3_label.setStyleSheet("font-size: 12px;")
        label_layout.addWidget(self.additional3_label)

        self.additional4_label = QLabel("▶ 업무 종료 후 3개월 이상 경과된 개인정보 파일 삭제")
        self.additional4_label.setStyleSheet("font-size: 12px;")
        label_layout.addWidget(self.additional4_label)

        self.additional5_label = QLabel("▶ 현재 업무와 연관성 없는 이전 업무 파일 삭제")
        self.additional5_label.setStyleSheet("font-size: 12px;")
        label_layout.addWidget(self.additional5_label)

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
        self.search_button.setFixedHeight(45)
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
        self.stop_button.setFixedHeight(45)
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
        self.clear_button.setFixedHeight(45)
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
        self.delete_button.setFixedHeight(45)
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
        self.open_button.setFixedHeight(45)
        self.open_button.clicked.connect(self.open_folder_path)
        button_layout.addWidget(self.open_button)

        left_layout.addLayout(button_layout)

        status_layout = QVBoxLayout()


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
        self.path_label.setStyleSheet("font-size: 12px;")
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
        self.result_table.horizontalHeader().sectionClicked.connect(
            self.handle_header_clicked)  # '수정 날짜' 열을 클릭했을 때 정렬을 처리하는 이벤트 핸들러 연결
        self.date_sort_order = Qt.DescendingOrder  # '수정 날짜' 열의 정렬 방향을 저장할 변수
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
            self.result_table.setRowCount(0)  # 결과 테이블의 내용을 초기화
            # 새 검색 스레드를 시작합니다.
            self.search_thread = threading.Thread(target=self.search_files)
            self.search_thread.start()
        else:
            QMessageBox.information(self, "검색 중", "이미 검색이 진행 중입니다.")

    def search_files(self):
        # print("파일 검색 시작")
        extensions = ['csv', 'pdf', 'doc', 'docx', 'xls', 'txt', 'zip', 'jpg', 'jpeg', 'png', 'ppt', 'pptx', 'hwp',
                      'bmp', 'tiff', 'html']
        keywords = ['고객', 'voc', '통화 품질', '상담', '목록', '리스트', '퀄리티', 'quality', '대외', '만족도', '보상', '작업지시', '통계', '민원',
                    '임대', '현황', '계약', '통장', '사본', '협의', '동의', '품의', '주민', '등본', '면허', '증명', '공사현장', '신입', '구성원', '직원',
                    '연락', '퇴직', '퇴사', '이력서', '가족', '원천징수', '소득', '연말', '급여', '인사', '평가', '자격', '연락처', '전화', '번호', '주소',
                    '군부대', '건물주', '내역', '출입', '전자파', '법인', '투자']
        # drives = ['D:/']
        drives = [f"{d}:/" for d in string.ascii_uppercase if os.path.exists(f"{d}:/")]

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
        selected_rows = set(item.row() for item in self.result_table.selectedItems())
        if selected_rows:
            confirm = QMessageBox.question(self, "삭제 확인", "정말로 선택한 파일들을 삭제하시겠습니까?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                for row in sorted(selected_rows, reverse=True):
                    file_path = self.result_table.item(row, 2).text()
                    try:
                        os.remove(file_path)
                        self.result_table.removeRow(row)
                    except Exception as e:
                        QMessageBox.warning(self, "오류", f"파일 삭제 중 오류가 발생했습니다: {e}")
                QMessageBox.information(self, "성공", "파일이 삭제되었습니다.")
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

    def open_log_file(self, link):
        log_file_path = os.path.join(os.getcwd(), "_internal", "batch_files", "search_word.LOG")  # 로그 파일 경로를 지정하세요
        try:
            os.startfile(log_file_path)
        except Exception as e:
            QMessageBox.warning(self, "오류", f"파일 열기 중 오류가 발생했습니다: {e}")