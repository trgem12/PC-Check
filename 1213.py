import os
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QHBoxLayout, QMenuBar, QAction, \
    QToolBar
from interview_check_widget import InterviewCheckWidget
from pc_optimization_widget import PCOptimizationWidget
from customer_info_search_widget import CustomerInfoSearchWidget
from home_widget import HomeWidget
from score_label import ScoreLabel
from vulnerability_scanner import VulnerabilityScanner
from infosec_day_widget import InfoSecDayWidget
from qt_material import apply_stylesheet
from qt_material import QtStyleTools

class CustomMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.oldPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
        super().mousePressEvent(event)  # 메뉴의 클릭 이벤트를 처리

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.oldPos:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.parent().move(self.parent().x() + delta.x(), self.parent().y() + delta.y())
            self.oldPos = event.globalPos()
        super().mouseMoveEvent(event)  # 메뉴의 클릭 이벤트를 처리
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PC 보안 점검 프로그램')
        self.resize(1074, 518)  # 크기 조정

        # 기본 타이틀 바 숨기기
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # 아이콘 파일의 절대 경로 생성
        icon_path = os.path.join(os.getcwd(), "_internal", "batch_files", "security.png")

        # 윈도우 타이틀 바 아이콘 설정
        self.setWindowIcon(QIcon(icon_path))

        # 중앙에 위치할 스택 위젯 생성
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # HOME 위젯 생성 및 스택 위젯에 추가
        self.home_widget = HomeWidget()
        self.stacked_widget.addWidget(self.home_widget)

        # InterviewCheckWidget 클래스를 import하여 사용
        self.interview_check_widget = InterviewCheckWidget()
        self.stacked_widget.addWidget(self.interview_check_widget)

        # PC 최적화 위젯 생성 및 스택 위젯에 추가
        self.pc_optimization_widget = PCOptimizationWidget()
        self.stacked_widget.addWidget(self.pc_optimization_widget)

        # CustomerInfoSearchWidget 인스턴스 생성
        self.customer_info_search_widget = CustomerInfoSearchWidget()
        self.stacked_widget.addWidget(self.customer_info_search_widget)

        # ScoreLabel 인스턴스 생성
        score = 0  # 점수를 0으로 초기화
        image_path = ""  # 이미지 경로를 빈 문자열로 초기화
        background_color = None  # 배경색을 None으로 초기화
        self.score_label = ScoreLabel(score, image_path, background_color)

        # VulnerabilityScanner 인스턴스 생성
        self.vulnerability_scanner_page = VulnerabilityScanner(customer_info_widget=self.customer_info_search_widget, home_widget=self.home_widget)
        self.stacked_widget.addWidget(self.vulnerability_scanner_page)

        #'정보보호의 날' 위젯 생성 및 스택 위젯에 추가
        self.infosec_day_widget = InfoSecDayWidget(self.vulnerability_scanner_page, self.interview_check_widget,
                                                   self.customer_info_search_widget)
        self.stacked_widget.addWidget(self.infosec_day_widget)


        # 메뉴 바 생성
        self.menu_bar = CustomMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #1F1F1F;
                color: white;
            }
        """)

        self.home_action = QAction('HOME', self)
        self.pc_check_action = QAction('PC 점검', self)
        self.customer_info_action = QAction('고객 정보 검색 도구', self)
        self.PC_optimization_action = QAction('PC 최적화', self)
        self.interview_check_action = QAction('인터뷰 점검 항목', self)
        self.infosec_day_action = QAction('정보보호의 날 점검 결과', self)
        # self.etc_action = QAction('사용법', self)

        self.menu_bar.addAction(self.home_action)
        self.menu_bar.addAction(self.pc_check_action)
        self.menu_bar.addAction(self.customer_info_action)
        self.menu_bar.addAction(self.interview_check_action)
        self.menu_bar.addAction(self.infosec_day_action)
        self.menu_bar.addAction(self.PC_optimization_action)
        # self.menu_bar.addAction(self.etc_action)

        self.menu_bar.addSeparator()  # 메뉴 항목 사이에 빈 공간 추가

        # self.exit_action = QAction('Exit', self)
        # self.menu_bar.addAction(self.exit_action)
        # self.exit_action.triggered.connect(self.close)

        self.home_action.triggered.connect(lambda: self.change_page(0))
        self.pc_check_action.triggered.connect(lambda: self.change_page(4))
        self.customer_info_action.triggered.connect(lambda: self.change_page(3))
        self.PC_optimization_action.triggered.connect(lambda: self.change_page(2))
        self.interview_check_action.triggered.connect(lambda: self.change_page(1))
        self.infosec_day_action.triggered.connect(lambda: self.change_page(5))
        # self.etc_action.triggered.connect(lambda: self.change_page(5))

    def change_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    # Apply the stylesheet
    apply_stylesheet(app, theme='dark_teal.xml')

    sys.exit(app.exec_())
