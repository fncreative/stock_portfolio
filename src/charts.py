import requests as req

import matplotlib

import pandas as pd
import numpy as np
import requests
import bokeh.plotting as bk
from bokeh.models import Label, HoverTool, BoxZoomTool, PanTool, ZoomInTool, ZoomOutTool, ResetTool, WheelZoomTool
from bokeh.embed import components

from json import JSONDecodeError

from flask import abort


def make_5y_stock_chart(company):
    API_URL = 'https://api.iextrading.com/1.0'
    STOCK = company

    try:
        res = req.get(f'{ API_URL }/stock/{ STOCK }/chart/5y')
        data = res.json()
    except JSONDecodeError:
        abort(404)

    df = pd.DataFrame(data)

    # TODO: this makes timestamps. bokeh plays nice with using timestamps for the x axis, but my glyphs break.
    # df['seqs'] = df['date'].apply((lambda x: pd.Timestamp(x)))
    seqs = np.arange(df.shape[0])
    df['seqs'] = pd.Series(seqs)

    df['changePercent'] = df['changePercent'].apply(lambda x: str(x) + '%')

    df['mid'] = df.apply(lambda x: (x['open'] + x['close']) / 2, axis=1)

    df['height'] = df.apply(
        lambda x: x['close'] - x['open'] if x['close'] != x['open'] else 0.01,
        axis=1
    )

    inc = df.close > df.open
    dec = df.close < df.open
    w = 0.3

    sourceInc = bk.ColumnDataSource(df.loc[inc])
    sourceDec = bk.ColumnDataSource(df.loc[dec])

    hover = HoverTool(
        tooltips=[
            ('Date', '@date'),
            ('Low', '@low'),
            ('High', '@high'),
            ('Open', '@open'),
            ('Close', '@close'),
            ('Percent', '@changePercent')
        ]
    )

    TOOLS = [hover, BoxZoomTool(), PanTool(), ZoomInTool(), ZoomOutTool(), WheelZoomTool(), ResetTool()]

    p = bk.figure(
        plot_width=1200,
        plot_height=800,
        title=f'{company} Stock Value History',
        tools=TOOLS,
        toolbar_location='above',
        # x_axis_type='datetime'
    )

    p.xaxis.major_label_orientation = np.pi/4
    p.grid.grid_line_alpha = w

    p.segment(df.seqs[inc], df.high[inc], df.seqs[inc], df.low[inc], color='green')
    p.segment(df.seqs[dec], df.high[dec], df.seqs[dec], df.low[dec], color='red')

    p.rect(x='seqs', y='mid', width=0.3, height='height', fill_color='green', line_color='green', source=sourceInc)
    p.rect(x='seqs', y='mid', width=0.3, height='height', fill_color='red', line_color='red', source=sourceDec)

    p.sizing_mode = "scale_width"

    return components(p)


def make_5y_vwap_chart(company):
    API_URL = 'https://api.iextrading.com/1.0'
    STOCK = company

    try:
        res = req.get(f'{ API_URL }/stock/{ STOCK }/chart/5y')
        data = res.json()
    except JSONDecodeError:
        abort(404)

    df = pd.DataFrame(data)

    w = 0.3

    # TODO: this makes timestamps. bokeh plays nice with using timestamps for the x axis, but my glyphs break.
    df['seqs'] = df['date'].apply((lambda x: pd.Timestamp(x)))
    seqs = np.arange(df.shape[0])
    # df['seqs'] = pd.Series(seqs)

    hover = HoverTool(
        tooltips=[
            ('Date', '@date'),
            ('vwap', '@vwap')
        ]
    )

    TOOLS = [hover, BoxZoomTool(), PanTool(), ZoomInTool(), ZoomOutTool(), WheelZoomTool(), ResetTool()]

    p = bk.figure(
        plot_width=1200,
        plot_height=800,
        title=f'{company} Stock Vwap History',
        tools=TOOLS,
        toolbar_location='above',
        x_axis_type='datetime'
    )

    p.xaxis.major_label_orientation = np.pi/4
    p.grid.grid_line_alpha = w

    p.line(df['seqs'], df['vwap'], line_width=2)

    p.sizing_mode = "scale_width"

    return components(p)
