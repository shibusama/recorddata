import sqlite3
from ctpwrapper import MdApiPy

# 定义 CTP 行情服务器信息
BROKER_ID = "9999"
USER_ID = "212893"
PASSWORD = "Zc@1319119251"
MD_FRONT_ADDR = "tcp://180.168.146.187:10131"

# 定义要订阅的期货合约列表
INSTRUMENT_IDS = ["FG505", "SR505"]  # 示例合约，可根据需求修改


# 继承 MdApi 类，实现回调方法
class MyMdApi(MdApiPy):
    def __init__(self, broker_id, user_id, password, md_front_addr):
        super().__init__()
        self.broker_id = broker_id
        self.user_id = user_id
        self.password = password
        self.md_front_addr = md_front_addr
        self.conn = sqlite3.connect('futures_market_data.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # 创建表来存储期货行情数据
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS futures_market_data (
                InstrumentID TEXT,
                LastPrice REAL,
                PreSettlementPrice REAL,
                PreClosePrice REAL,
                PreOpenInterest REAL,
                OpenPrice REAL,
                HighestPrice REAL,
                LowestPrice REAL,
                Volume INTEGER,
                Turnover REAL,
                OpenInterest REAL,
                ClosePrice REAL,
                SettlementPrice REAL,
                UpperLimitPrice REAL,
                LowerLimitPrice REAL,
                UpdateTime TEXT,
                UpdateMillisec INTEGER,
                BidPrice1 REAL,
                BidVolume1 INTEGER,
                AskPrice1 REAL,
                AskVolume1 INTEGER
            )
        ''')
        self.conn.commit()

    def save_to_database(self, data):
        # 将行情数据保存到数据库
        try:
            self.cursor.execute('''
                INSERT INTO futures_market_data (
                    InstrumentID, LastPrice, PreSettlementPrice, PreClosePrice, PreOpenInterest,
                    OpenPrice, HighestPrice, LowestPrice, Volume, Turnover,
                    OpenInterest, ClosePrice, SettlementPrice, UpperLimitPrice, LowerLimitPrice,
                    UpdateTime, UpdateMillisec, BidPrice1, BidVolume1, AskPrice1, AskVolume1
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                data['InstrumentID'], data['LastPrice'], data['PreSettlementPrice'], data['PreClosePrice'],
                data['PreOpenInterest'], data['OpenPrice'], data['HighestPrice'], data['LowestPrice'],
                data['Volume'], data['Turnover'], data['OpenInterest'], data['ClosePrice'],
                data['SettlementPrice'], data['UpperLimitPrice'], data['LowerLimitPrice'],
                data['UpdateTime'], data['UpdateMillisec'], data['BidPrice1'], data['BidVolume1'],
                data['AskPrice1'], data['AskVolume1']
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Error saving data to database: {e}")

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        if pRspInfo['ErrorID'] == 0:
            print("登录成功")
            # 订阅行情
            self.SubscribeMarketData(INSTRUMENT_IDS)
        else:
            print(f"登录失败，错误码: {pRspInfo['ErrorID']}, 错误信息: {pRspInfo['ErrorMsg']}")

    def OnRtnDepthMarketData(self, pDepthMarketData):
        # 处理行情数据
        print(f"收到行情数据: {pDepthMarketData['InstrumentID']}")
        self.save_to_database(pDepthMarketData)


if __name__ == "__main__":
    md_api = MyMdApi(BROKER_ID, USER_ID, PASSWORD, MD_FRONT_ADDR)
    md_api.RegisterFront(MD_FRONT_ADDR)
    md_api.Init()
    input("按任意键退出...")
    md_api.Release()
    md_api.conn.close()