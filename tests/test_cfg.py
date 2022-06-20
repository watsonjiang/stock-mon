from unittest import TestCase

from stockmon import model
from stockmon.app import StockMonApplication
from stockmon.model import StockDao
from stockmon.views.cfg import HqCfgView


class TestHqCfgView(TestCase):
    def test_view(self):
        app = StockMonApplication.instance()
        db_path = StockMonApplication.get_res_path('stock_db.sqlite3')
        db_engine = model.init_engine("sqlite:///" + db_path)
        app.stock_dao = StockDao(db_engine)
        view = HqCfgView()

        view.show()
        app.qt_app.exec_()
