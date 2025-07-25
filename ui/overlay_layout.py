from PyQt5.QtWidgets import QLayout, QWidgetItem
from PyQt5.QtCore import Qt

class QOverlayLayout(QLayout):
    """Un layout personnalisé pour superposer des widgets (comme un badge sur une icône)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []
        self.positions = {}  # Pour stocker les alignements

    def addWidget(self, widget, alignment=None):
        item = QWidgetItem(widget)
        self.addItem(item)
        if alignment is not None:
            self.positions[widget] = alignment
        return item

    def addItem(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)

    def itemAt(self, index):
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def setGeometry(self, rect):
        super().setGeometry(rect)

        for i in range(self.count()):
            item = self.itemAt(i)
            if item is None:
                continue

            widget = item.widget()
            if widget is None:
                continue

            # Position par défaut (remplit tout l'espace)
            widget_rect = rect

            # Appliquer l'alignement si spécifié
            if widget in self.positions:
                alignment = self.positions[widget]
                size = widget.sizeHint()

                if alignment & Qt.AlignTop:
                    widget_rect.setTop(rect.top())
                    widget_rect.setBottom(rect.top() + size.height())
                elif alignment & Qt.AlignBottom:
                    widget_rect.setTop(rect.bottom() - size.height())
                    widget_rect.setBottom(rect.bottom())

                if alignment & Qt.AlignLeft:
                    widget_rect.setLeft(rect.left())
                    widget_rect.setRight(rect.left() + size.width())
                elif alignment & Qt.AlignRight:
                    widget_rect.setLeft(rect.right() - size.width())
                    widget_rect.setRight(rect.right())

                if alignment & Qt.AlignHCenter:
                    widget_rect.setLeft(rect.left() + (rect.width() - size.width()) // 2)
                    widget_rect.setRight(widget_rect.left() + size.width())
                elif alignment & Qt.AlignVCenter:
                    widget_rect.setTop(rect.top() + (rect.height() - size.height()) // 2)
                    widget_rect.setBottom(widget_rect.top() + size.height())

            widget.setGeometry(widget_rect)
