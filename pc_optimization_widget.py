# pc_optimization_widget.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox
import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

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