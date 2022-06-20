from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QCompleter
from PyQt5.uic import loadUi

from stockmon.app import StockMonApplication
from stockmon.model import StockDao


class HqCfgView(QDialog):
    stock_dao: StockDao
   
    def __init__(self):
        super(HqCfgView, self).__init__()
        self.stock_dao = StockMonApplication.instance().get_stock_dao()
        self.init()

    def init(self):
        ui_path = StockMonApplication.get_res_path('win_cfg.ui')
        loadUi(ui_path, self)
        self.setWindowIcon(QIcon(StockMonApplication.get_res_path('stock.png')))
        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowContextHelpButtonHint)
        self.add_btn.clicked.connect(self.on_add)
        all_codes = []
        self.stock_dao.iter_all_company(lambda x: all_codes.append(x.code))
        completer = QCompleter(all_codes)
        self.stock_input.setCompleter(completer)
        self.stock_list.itemDoubleClicked.connect(self.on_remove)

    def on_add(self):
        """
        添加股票代码
        """
        code = self.stock_input.text()
        s = self.stock_dao.get_company_by_code(code)
        item = QListWidgetItem('{}({})'.format(s.name, s.code))
        self.stock_list.addItem(item)

    def on_remove(self, item:QListWidgetItem):
        idx = self.stock_list.row(item)
        self.stock_list.takeItem(idx)
