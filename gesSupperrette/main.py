from ui import StockApp

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())