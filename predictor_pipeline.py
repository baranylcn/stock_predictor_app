def stock_prediction(company_name, month):
    # Import
    import yfinance as yf
    import pandas as pd
    from prophet import Prophet
    from datetime import datetime, timedelta
    from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

    symbol = [company_name]

    start_date = '2000-01-01'
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    # Read dataset
    df = yf.download(symbol, start=start_date, end=formatted_date,
                     group_by='ticker', auto_adjust=True, prepost=True)
    df = df[["Close"]] # Target

    df = df.reset_index() \
        .rename(columns={'Date': 'ds',
                         'Close': 'y'})

    # Adding Holidays
    cal = calendar()
    holidays = cal.holidays(start=df.index.min(),
                            end=df.index.max(),
                            return_name=True)
    holiday_df = pd.DataFrame(data=holidays,
                              columns=['holiday'])
    holiday_df = holiday_df.reset_index().rename(columns={'index': 'ds'})

    model_with_holidays = Prophet(holidays=holiday_df)
    model_with_holidays.fit(df)

    # Predict into the Future
    future = model_with_holidays.make_future_dataframe(periods=365 * 24, freq='h',
                                                       include_history=False)
    forecast = model_with_holidays.predict(future)
    forecast = forecast.set_index("ds")
    current_date = datetime.now()
    end_date = current_date + timedelta(days=30*month)
    forecast = forecast.loc[current_datetime:end_date]

    return forecast
