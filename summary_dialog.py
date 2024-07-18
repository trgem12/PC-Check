# summary_dialog.py
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame


class SummaryDialog(QDialog):
    def __init__(self, summary_data, parent=None):
        super(SummaryDialog, self).__init__(parent)
        self.setWindowTitle('점검 완료')
        self.setFixedSize(310, 180)  # 결과 창의 크기를 설정

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # 상태 레이블과 수치를 표시하는 레이아웃
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.create_status_label('양호', 'green', summary_data.get('양호한 항목', 0)))
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
        completion_time = QLabel(f"점검 완료 시간({current_time})")
        completion_time.setFont(QFont('Arial', 8))
        layout.addWidget(completion_time)

        # 자동진단 결과 저장 문구 추가
        save_results_message = QLabel("자동진단 결과 저장 버튼 클릭!!")
        save_results_message.setFont(QFont('Arial', 10))
        save_results_message.setAlignment(Qt.AlignCenter)  # Center align the text
        save_results_message.setStyleSheet("color: red;")  # Change the text color to red
        layout.addWidget(save_results_message)

    def create_status_label(self, text, color, count):
        label = QLabel(f"{text}\n{count} 개")
        label.setStyleSheet(f"background-color: {color}; color: white; padding: 5px; border-radius: 5px;")
        label.setAlignment(Qt.AlignCenter)
        return label