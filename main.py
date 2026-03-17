from data_collection import StockAnalyzed
from os import remove

def get_user() -> tuple[str, str, str, int]:
    print("\nВведите параметры для скачивания данных акций:")
    ticker = input("Тикер акции (например MSFT, AAPL, TSLA): ").strip().upper()
    start_date = input("Начальная дата (YYYY-MM-DD): ").strip()
    end_date = input("Конечная дата (YYYY-MM-DD): ").strip()
    days = int(input("Количесво дней для вычисления SMA/RSI: "))

    return ticker, start_date, end_date, days


ticker, start_date, end_date, days = get_user()
analyzer = StockAnalyzed(ticker, start_date, end_date)


def main():

    global ticker, start_date, end_date, days

    print('Загружаю данные...')

    global analyzer

    filename = analyzer.data_col()

    print(analyzer.data_read(filename))

    sma_data = analyzer.sma(days)
    if sma_data is None:
        print('Неудалось расчитать SMA')
        return

    rsi_data, trend = analyzer.rsi(days)
    if rsi_data is None:
        print(trend)
        return

    print(rsi_data[['Date', 'Close', f'SMA_{days}', f'RSI_{days}']].tail().to_string(index=False))
    print(f'Тренд RSI: {trend}')



if __name__ == '__main__':
    main()
    remove(analyzer.default_file_name)

