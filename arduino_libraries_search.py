import click
import datetime
import pandas as pd
from utils import MAX_ROWS_DEFAULT, EXPIRE_AFTER_DEFAULT, SEARCH_IN_DEFAULT, init_session, download_index, add_possible_repository_url, search


@click.command()
@click.option('--max-rows', default=MAX_ROWS_DEFAULT, help='Number of rows to display.')
@click.option('--cache', default=EXPIRE_AFTER_DEFAULT.days, help='Number of days to cache queries.')
@click.option('--keywords', default='', help='Search keywords (separated with space)')
@click.option('--search_in', default=",".join(SEARCH_IN_DEFAULT), help='Search keyword in the following colums (separated with a coma)')
@click.option('--write-excel/--no-write-excel', default=False)
def main(max_rows, cache, keywords, search_in, write_excel):
    pd.set_option("max_rows", max_rows)
    expire_after = datetime.timedelta(days=cache)
    session = init_session(expire_after)
    df = download_index(session)
    # df = add_possible_repository_url(df)
    # print(df)
    # print("Have repo like archive: %d" % df['have_repo_like_archive'].sum())
    # print("Don't have repo like archive: %d" % (len(df) - df['have_repo_like_archive'].sum()))
    # return
    # df_first = df.groupby('name').last().reset_index()
    df_last = df.groupby('name').first().reset_index()
    df_last['number_of_version'] = df.groupby('name')['version'].count()
    df_last = add_possible_repository_url(df_last)
    print(df_last[['name', 'url', 'website', 'possible_url_repository', 'have_repo_like_archive']].set_index('name'))
    print("Have repo like archive: %d" % df_last['have_repo_like_archive'].sum())

    if keywords != '':
        columns_search = search_in.split(',')
        df_search = search(keywords, columns_search, session=session, df_last=df_last)
    if write_excel:
        print("Writing Excel file")
        with pd.ExcelWriter("libraries.xlsx") as writer:
            df_last.to_excel(writer, sheet_name='Last')
            # df_first.to_excel(writer, sheet_name='First')
            df.to_excel(writer, sheet_name='All')
            if keywords != '':
                df_search.to_excel(writer, sheet_name='Search')


if __name__ == '__main__':
    main()
