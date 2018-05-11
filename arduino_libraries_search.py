import click
import datetime
from requests_cache import CachedSession
import pandas as pd
from pandas.io.json import json_normalize
# import semver


@click.command()
@click.option('--max-rows', default=20, help='Number of rows to display.')
@click.option('--cache', default=7, help='Number of days to cache queries.')
@click.option('--search', default='', help='Search keyword')
@click.option('--write-excel/--no-write-excel', default=False)
def main(max_rows, cache, search, write_excel):
    pd.set_option("max_rows", max_rows)
    expire_after = datetime.timedelta(days=cache)
    session = CachedSession(cache_name='cache', backend='sqlite',
                            expire_after=expire_after)
    url = "http://downloads.arduino.cc/libraries/library_index.json"
    r = session.get(url)
    d = r.json()
    libraries = d['libraries']
    df = json_normalize(libraries)
    # df['version'] = df['version'].map(semver.parse_version_info)
    # raises TypeError: unhashable type: 'VersionInfo'
    # see https://github.com/k-bx/python-semver/issues/73
    df = df.sort_values(by=['name', 'version'], ascending=[True, True])
    # df_first = df.groupby('name').first()
    df_last = df.groupby('name').last()
    if search != '':
        ser_have_keyword = \
            df_last['paragraph'].str.contains(search,
                                              case=False).fillna(False)
        df_search = df_last[ser_have_keyword]
        print(df_search)
    if write_excel:
        print("Writing Excel file")
        with pd.ExcelWriter("libraries.xlsx") as writer:
            df.to_excel(writer, sheet_name='All')
            df_last.to_excel(writer, sheet_name='Last')
            # df_first.to_excel(writer, sheet_name='First')
            if search != '':
                df_search.to_excel(writer, sheet_name='Search')


if __name__ == '__main__':
    main()
