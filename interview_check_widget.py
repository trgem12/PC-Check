# interview_check_widget.py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox


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
        self.tableWidget.setColumnWidth(0, 160)  # "구분" 열의 너비를 100픽셀로 설정
        self.tableWidget.setColumnWidth(1, 700)  # "점검 항목" 열의 너비를 200픽셀로 설정
        self.tableWidget.setColumnWidth(2, 150)  # "결과" 열의 너비를 150픽셀로 설정

        # 예제 데이터 추가
        example_data = [
            ("고객정보보호",
             "고객/개인정보 파일(하드 카피본 포함) 정리 및 Masking 처리 유무\n-파일 내 불필요한 고객정보는 SKT 기준에 부합하는 Masking 처리 후 보관 시행\n※ 업무중인 경우:MAX 3개월까지 보관 가능 단, 업무 종료 후 즉시 파기(evEraser를 이용한 완전 삭제 시행)\n※가족/개인/구성원 정보 또한 보관 금지, 업무상 필요 시 사용하고 업무 종료 즉시 파기\n▶양호:PC 내 고객/개인정보 정리 및 Masking 수행\n▶미흡:PC 내 고객/개인정보 정리 및 Masking 미수행",
             ""),
            (
            "고객정보보호", "고객정보 취급자 망 분리 상태 유무\n※Swing, RealT 시스템 사용자 중 고객정보 다운로드 가능자/권한자는 망분리 솔루션(VM, Fort, myDesk) 필수 설치\n▶양호:고객정보 취급자 경우 망 분리를 한 경우\n▶미흡:고객정보 취급자 경우 망 분리를 하지 않은 경우\n▶해당사항 없음:고객정보 취급자가 아닌 경우",
            ""),
            ("고객정보보호",
             "계약서/중요문서 등 보관상태 및 출력/복사/파기 현황 점검\n※ 업무 중인 계약서 및 중요문서는 시건장치가 있는 곳에 보관해야 하며, 업무 종료 시 즉시 파쇄\n※ 계약서 출력/복사 시 최종 파쇄까지 관리를 해야 함(관리대장 기재)\n※ 개인정보를 수집하는 중요문서 같은 경우 고객정보보호법 의거 고객정보 수집에 관한 이용 동의서 징구 유무 확인\n▶양호:계약서/중요문서 등을 잠금장치가 있는 곳에 보관 O 및 현황 점검하고 있는 경우\n▶미흡:계약서/중요문서 등을 잠금장치가 있는 곳에 보관 X 및 현황 미점검한 경우",
             ""),
            ("고객정보보호", "이글아이 자가진단 시행 여부 확인\n※ 매일 PC 종료 전 자동 검사 검출 내역 확인 및 파일 관리 시행\n▶양호:이글아이 자가진단 시행 후 검출 파일 삭제/보유등록 처리한 경우\n▶미흡:이글아이 자가진단 시행하지 않았거나 검출 파일 삭제/보유등록 미처리한 경우", ""),
            ("고객정보보호",
             "NateOn Biz 쪽지함 및 E-Mail내 고객정보 유무 확인\n - 업무상 필요한 경우 메일 개별 저장 시행(단, 고객정보가 담긴 메일은 저장 금지)\n※ Biz 쪽지함 및 E-Mail 내 첨부된 고객정보 파일 또는 내용 유무를 확인하고 업무 종료 시 즉시 삭제 시행\n※ E-Mail 자동 저장 프로그램 사용 금지\n▶양호:NateOn Biz 쪽지함, e-Mail 내 고객정보 확인 후 삭제한 경우\n▶미흡:NateOn Biz 쪽지함, e-Mail 내 고객정보 미확인 또는 삭제하지 않은 경우",
             ""),
            ("고객정보보호",
             "Real.T/ERP 사용자 불필요 물건 및 고객 정보 조회/다운/카피 금지\n - 파일/문서상 고객정보 확인 시 Making 처리 필수 (파일 스캔본 포함)\n※ 업무상 불필요한 고객정보는 절대 조회나 다운로드 하지 않으며 복사본 이용 또한 금지\n▶양호:파일/문서 내 고객정보 확인 시 Masking 처리한 경우\n▶미흡:파일/문서 내 고객정보 확인 시 Masking 처리를 하지 않은 경우\n▶해당사항 없음:Real.T/ERP 미사용하는 경우",
             ""),
            ("IT보안",
             "CISO, CPO, 정보보호 책임자, 담당자 인지여부\n※ (CISO, CPO: 안전보건담당, 정보보안책임자: 각 담당, 담당자: 각 팀 팀장, TL\n▶양호:SKO CISO, CPO, 책임자/담당자 인지하고 있는 경우\n▶미흡:SKO CISO, CPO, 책임자/담당자를 모르고 있는 경우",
             ""),
            ("IT보안",
             "정보보안 침해사고 발생 보고절차 인지 여부\n※ 침해사고 발생 시 구성원 측면에서는 보안담당자(팀장)에게 즉시 보고하고 부재 시 보안책임자에게 즉시 보고한다.\n▶양호:정보보안 침해사고 발생 보고 절차를 인지하고 있는 경우\n▶미흡:정보보안 침해사고 발생 보고 절차를 모르고 있는 경우",
             ""),
            ("IT보안",
             "OA망/감시망 관리 정상 유무\n※ 150점대 업무용 PC와 200,60점대 폐쇄망 PC는 혼용하여 사용 불가\n▶양호:1개 PC에서 OA망과 폐쇄망을 혼용해서 사용하고 있지 않은 경우\n▶미흡:1개 PC에서 OA망과 폐쇄망을 혼용해서 사용하고 있는 경우",
             ""),
            ("IT보안",
             "불법 소프트웨어 설치 유무 점검\n※ 시작 - 프로그램 추가/제거 내 게임, 증권, 파일공유, 캡쳐, 메모앱 등 프로그램 설치 금지\n※ 폐쇄망 감시용 PC는 감시 목적 프로그램(EMS, NMS 등)을 제외한 프로그램 설치 금지\n▶양호:PC 내 불법 소트프웨어가 설치되어 있지 않은 경우\n▶미흡:PC 내 불법 소트프웨어가 설치되어 있는 경우",
             ""),
            ("물적보안",
             "임직원 퇴근/외근 시 PC 방치 여부\n※ 외근(1시간 이상)이나 퇴근 시에는 PC를 반드시 시건장치가 있는 곳에 보관\n※ 점심시간에는 반드시 화면보호기 동작 생활화\n▶양호:퇴근/외근 시 PC를 잠금장치가 있는 곳에 보관하는 경우\n▶미흡:퇴근/외근 시 PC를 잠금장치가 있는 곳에 보관하지 않는 경우",
             ""),
            ("물적보안",
             "책상 위 경영정보 보관상태 유무(조직도 제외)\n※ SKO 조직도를 제외한 BP연락처, SKT조직도 등의 중요정보가 있는 문서는 시건장치가 있는 곳에 보관\n▶양호:책상 위 경영정보를 배치하고 있지 않은 경우\n▶미흡:책상 위 경영정보를 배치하고 있는 경우",
             ""),
            ("물적보안",
             "사물함 문서 파기 유무(과다보유 시 점검 대상)\n※ 개인서랍 및 공용 서랍장 내 과다문서 보관 정리\n▶양호:개인 서랍 및 공용 서랍장 내 과다문서가 보관되어 있지 않은 경우\n▶미흡:개인 서랍 및 공용 서랍장 내 과다문서가 보관된 경우",
             ""),
            ("물적보안",
             "개인서랍 비밀번호 최소 2자리 이상 설정 유무\n※ 구성원 개인 서랍 PW 설정 시 2자리 이상으로 설정\n※ 단순(00, 000, 1111 등) PW 설정 금지\n▶양호:개인 서랍 비밀번호 최소 2자리 이상 설정한 경우\n▶미흡:개인 서랍 비밀번호를 1자리로 설정한 경우",
             ""),
            ("인적보안",
             "사원증 상시 패용 유무(사옥/사무실)\n※ 사옥 외에서는 사원증 미패용\n▶양호:사옥/사무실 내에서 사원증을 패용하고 있는 경우\n▶미흡:사옥/사무실 외에서 사원증을 패용하고 있는 경우",
             ""),
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
            combo.setStyleSheet("QComboBox { color: white; }" "QComboBox QAbstractItemView { color: white; }")
            combo.addItem("선택")  # 초기 선택 항목을 빈 문자열로 설정
            combo.addItem("양호")
            combo.addItem("미흡")
            combo.addItem("해당사항 없음")
            combo.setCurrentIndex(0)  # 첫 번째 항목을 기본적으로 선택
            combo.currentIndexChanged.connect(self.on_combobox_changed)  # 콤보 박스의 currentIndexChanged 시그널에 슬롯 함수 연결
            self.tableWidget.setCellWidget(row, 2, combo)
            self.tableWidget.setRowHeight(row, 100)  # 행 높이를 50픽셀로 설정

        # self.tableWidget.resizeRowsToContents()  # 행 높이를 셀의 내용에 맞게 조정

        layout.addWidget(self.tableWidget)

    def on_combobox_changed(self, index):
        # 콤보 박스의 선택 항목이 변경되었을 때 수행할 동작을 여기에 작성합니다.
        # 예를 들어, 선택된 항목에 따라 다른 동작을 수행하려면 다음과 같이 작성할 수 있습니다:
        sender = self.sender()
        if index == 1:  # "양호" 선택
            print(f"{sender} was changed to '양호'")
        elif index == 2:  # "미흡" 선택
            print(f"{sender} was changed to '미흡'")
        elif index == 3:  # "해당사항 없음" 선택
            print(f"{sender} was changed to '해당사항 없음'")

    def get_table_data(self):
        table_data = [['구분', '점검항목', '결과']]  # 테이블 헤더 추가
        for row in range(self.tableWidget.rowCount()):
            id = self.tableWidget.item(row, 0).text()
            question = self.tableWidget.item(row, 1).text()
            result_widget = self.tableWidget.cellWidget(row, 2)
            if isinstance(result_widget, QComboBox):  # 결과 위젯이 QComboBox인지 확인
                result = result_widget.currentText()
            else:
                result = ""
            table_data.append([id, question, result])
        return table_data