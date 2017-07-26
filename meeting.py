#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
from datetime import datetime, timedelta
from pprint import pprint, pformat
import re

DT_FORMAT = "%Y-%m-%d %a"

DAYS = {}

MEETINGS = [
    {'activity': 'A', 'datetime': '1(1000-1200)[20170223-20170301]'},
    {'activity': 'A', 'datetime': '4(0800-1000)[20170223-20170301]'},
    {'activity': 'A', 'datetime': '5(1400-1600)'},
    {'activity': 'B', 'datetime': '5(1400-1600)'},
]


def schedule_meeting(meeting, days):
    pattern = re.compile(r"""
                            (\d+)                    # match 1~7                 (1 => Monday, 7 => Sunday)
                            \((\d+\-\d+)\)           # match (1000-1200)         => 1000-1200
                            (?:\[(\d+)\-(\d+)\])*    # match [20170101-20171231] => 20170101, 20171231
                            """, re.X)
    m = re.search(pattern, meeting['datetime'])

    if m:
        pprint(meeting)

        '''
        w  => 1 ~ 7          星期
        t  => 1000-1200      時間範圍
        d1 => 20170101       日期開始，可有可無 None
        d2 => 20171231       日期結束，可有可無 None
        '''
        w, t, d1, d2 = m.groups()

        '''限定日期範圍'''
        if d1 and d2:
            d1 = datetime.strptime(d1, "%Y%m%d")
            d2 = datetime.strptime(d2, "%Y%m%d")

            delta = d2 - d1

            for i in range(delta.days + 1):
                d = d1 + timedelta(days=i)

                '''星期符合，排入活動'''
                if d.isoweekday() == int(w):
                    days[d.strftime(DT_FORMAT)].append(
                        {'activity': meeting['activity'], 'time': t})
        else:
            for d in days.keys():
                d = datetime.strptime(d, DT_FORMAT)

                '''星期符合，排入活動'''
                if d.isoweekday() == int(w):
                    days[d.strftime(DT_FORMAT)].append(
                        {'activity': meeting['activity'], 'time': t})


def main():
    locale.setlocale(locale.LC_TIME, 'zh_TW.UTF-8')

    d1 = datetime.strptime("20170223", "%Y%m%d")
    d2 = datetime.strptime("20170309", "%Y%m%d")

    delta = d2 - d1

    '''設定日期'''
    for i in range(delta.days + 1):
        d = d1 + timedelta(days=i)
        DAYS[d.strftime(DT_FORMAT)] = []

    '''安排活動'''
    for m in MEETINGS:
        schedule_meeting(m, DAYS)

    '''顯示完整活動'''
    for k in sorted(DAYS.keys()):
        print("%s => %s" % (k, pformat(DAYS[k])))

if __name__ == '__main__':
    main()
