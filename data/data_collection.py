import yfinance as yf
import numpy as np
import pandas as pd
from typing import Optional, Tuple

class StockData:
    def __init__(self, ticket: str, start: str, end: str):
        self.ticket = ticket
        self.start = start
        self.end = end
        self.default_file_name = f'{ticket}_{start}_{end}.csv'

    def data_col(self) -> str:
        try:
            data = yf.download(self.ticket, self.start, self.end, progress=False, auto_adjust=True)

            if data.empty:
                print('Нет данных')
                return False

            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

            data.to_csv(self.default_file_name)
            print('Данные загружены')
            return self.default_file_name
        except Exception as e:
            print(f'Error {e}')
            return None

    @staticmethod
    def data_read(filename: str) -> Optional[pd.DataFrame]:
        try:
            return pd.read_csv(filename, parse_dates=True, index_col=0)
        except FileNotFoundError:
            print(f'File {filename} not found')
            return None
        
class StockAnalyzed(StockData):
    def __init__(self, ticket: str, start: str, end: str):
        super().__init__(ticket, start, end)
    
    
    def sma(self, days: int) -> Optional[pd.DataFrame]:

        data = pd.read_csv(self.default_file_name)

        try:
            if len(data) < days:
                print('Ошибка, загрузите больше данных')
                return None

            data[f'SMA_{days}'] = data['Close'].rolling(window=days, min_periods=days).mean()   

            data.to_csv(self.default_file_name)

            return data
        except Exception as e:
            print(f'Error {e}')
            return None
    
    def rsi(self, days: int) -> Tuple[pd.DataFrame, str]:
        data = pd.read_csv(self.default_file_name)

        try:
            data['Close'] = pd.to_numeric(data['Close'], errors='coerce')

            delta = data['Close'].diff()

            high = (delta.where(delta > 0, 0)).rolling(window=days, min_periods=1).mean()
            loss = (delta.where(delta <= 0, 0)).rolling(window=days, min_periods=1).mean()

            loss = loss.replace(0, 1)


            rs = high / loss
            rsi = 100 - (100 / (1 + rs))

            data[f'RSI_{days}'] = rsi
            data.to_csv(self.default_file_name, index = False)

            last_rsi = rsi.iloc[-1] if not rsi.empty else np.nan
            if pd.isna(last_rsi):
                trend = "Недостаточно данных для анализа"
            elif last_rsi > 70:
                trend = "Перекупленность (возможен спад)"
            elif last_rsi < 30:
                trend = "Перепроданность (возможен рост)"
            else:
                trend = "Нейтральный тренд"

            return data, trend

        except Exception as e:
            print(f'Error {e}')
            return None            