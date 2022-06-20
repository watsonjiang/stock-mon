from unittest import TestCase

import pandas as pd

from stockmon import model
from stockmon.app import StockMonApplication
from stockmon.model import StockDao, CompanyInfoEntity


def update_sse(stock_dao, xlsx_path):
    df = pd.read_excel(xlsx_path)
    df = df[['A股代码', '证券简称']]

    buf = []
    for idx, row in df.iterrows():
        comp = CompanyInfoEntity(code=row['A股代码'], name=row['证券简称'])
        print('----', idx, comp.code, comp.name)
        buf.append(comp)
        if len(buf) == 1000:
            stock_dao.save_company(buf)
            buf = []

    if buf:
        stock_dao.save_company(buf)


def update_szse(stock_dao, xlsx_path):
    df = pd.read_excel(xlsx_path)
    df = df[['A股代码', 'A股简称']]

    buf = []
    for idx, row in df.iterrows():
        comp = CompanyInfoEntity(code='{:06d}'.format(int(row['A股代码'])), name=row['A股简称'])
        print('----', idx, comp.code, comp.name)
        buf.append(comp)
        if len(buf) == 1000:
            stock_dao.save_company(buf)
            buf = []

    if buf:
        stock_dao.save_company(buf)


class TestHq(TestCase):

    def test_update_all_company_info(self):
        """更新数据库公司信息.
           数据源来自:
           https://www.szse.cn/market/product/stock/list/
           http://www.sse.com.cn/assortment/stock/list/share/
        """
        db_path = StockMonApplication.get_res_path('stock_db.sqlite3')
        db_engine = model.init_engine("sqlite:///" + db_path)
        stock_dao = StockDao(db_engine)
        xlsx_path = StockMonApplication.get_res_path('sse-20220620.xls')
        update_sse(stock_dao, xlsx_path)
        xlsx_path = StockMonApplication.get_res_path('szse-20220620.xlsx')
        update_szse(stock_dao, xlsx_path)
        stock_dao.iter_all_company(lambda x: print(x.code, x.name))

    def test_list_all_company(self):
        db_path = StockMonApplication.get_res_path('stock_db.sqlite3')
        db_engine = model.init_engine("sqlite:///" + db_path)
        stock_dao = StockDao(db_engine)
        total = 0

        def echo(x: CompanyInfoEntity):
            nonlocal total
            total += 1
            print(x.code, x.name)

        stock_dao.iter_all_company(echo)
        print('-----total', total)
