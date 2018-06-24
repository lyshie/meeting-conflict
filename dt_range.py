#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime


def dt_range(string):
    pat = re.compile(r"""
                        (?P<daterange>                      # 20180701-20180731
                            (?P<datebegin> \d{8,8} )        # 20180701
                            \-                              # -
                            (?P<dateend> \d{8,8} )          # 20180731
                            \/
                        ){0,1}

                        (?P<timerange>                      # 2(0900-1200)
                            (?P<weekday> \d )               # 2，星期二
                            \(
                                (?P<timebegin> \d{4,4} )    # 0900
                                \-                          # -
                                (?P<timeend> \d{4,4} )      # 1200
                            \)
                        )
                     """, re.X)
    match = pat.match(string)
    if match:
        for m in match.groups():
            print(m)

        if match.group('datebegin'):
            t = datetime.strptime(match.group('datebegin'), '%Y%m%d')
            print(t)

    print("=" * 60)


def main():
    ds = '20180701-20180731/2(0900-1200)'
    dt_range(ds)
    dt_range("2(0900-1200)")
    dt_range('20180701-20180731/2')

if __name__ == '__main__':
    main()
