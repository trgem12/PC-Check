# score_label.py
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtProperty
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor

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
            iy -= 90  # 이미지를 위로 10픽셀 이동
            painter.drawPixmap(ix, iy, iw, ih, image)
        # 텍스트 그리기
        painter.setPen(QColor('white'))
        painter.setFont(QFont('Arial', 8, QFont.Bold))  # 폰트 크기를 조정하여 상단 텍스트에 적용
        painter.drawText(self.rect().adjusted(0, 50, 0, 0), Qt.AlignCenter, "최근 PC 점검 점수")  # 상단 텍스트 위치 조정
        painter.setFont(QFont('Arial', 20, QFont.Bold))
        # painter.drawText(self.rect(), Qt.AlignCenter, f"{self.score}점")
        painter.drawText(self.rect().adjusted(0, 100, 0, 0), Qt.AlignCenter, f"{self.score}점")
        painter.end()