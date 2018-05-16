import click
import sys
import datetime
import pandas as pd
from utils import MAX_ROWS_DEFAULT, EXPIRE_AFTER_DEFAULT, THRESHOLD_DEFAULT, \
    init_session, download_index, \
    get_versions, get_latest_version, get_archive_url, \
    show_licence_from_archive_url, repository_url_from_archive_url, find_nearest_names
import traceback


@click.command()
@click.option('--max-rows', default=MAX_ROWS_DEFAULT, help='Number of rows to display.')
@click.option('--cache', default=EXPIRE_AFTER_DEFAULT.days, help='Number of days to cache queries.')
@click.argument('name')  # Name of library (ArduinoJson for example)
@click.option('--version', default='latest', help='Version number as semantic version or latest')
@click.option('--threshold', default=THRESHOLD_DEFAULT, help='Threshold value to find nearest library name.')
def main(max_rows, cache, name, version, threshold):
    print("Download %r" % name)
    pd.set_option("max_rows", max_rows)
    expire_after = datetime.timedelta(days=cache)
    session = init_session(expire_after)
    df = download_index(session)
    # df_first = df.groupby('name').last()
    # df_last = df.groupby('name').first()

    if name not in df['name'].values:
        print("%r is not a valid library name" % name)
        print()
        print("Possible library names are:")
        names = find_nearest_names(name, threshold=threshold, df=df)
        print(names[0:10])
        find_nearest_name = names.iloc[0]
        if find_nearest_name.score == 1:
            print()
            new_name = find_nearest_name['name']
            print("Case is important! Autofixing it as %r instead of %r" % (new_name, name))
            name = new_name
            input("")
        else:
            print()
            sys.exit("Please correct library name!")

    df_all_versions = df[df['name'].str.upper() == name.upper()]
    name = df_all_versions.name.unique()[0]
    print(df_all_versions.set_index('version'))

    print("")

    versions = get_versions(name, df)
    print("versions: %s" % versions.map(str).values)

    if version == 'latest':
        version = get_latest_version(name, df)

    print()

    print("version: %s" % str(version))

    url = get_archive_url(name, version, df)

    print()

    print("Downloading from %r" % url)
    assert url[-4:] == '.zip', "URL must finish with .zip"
    print()

    show_licence_from_archive_url(url)

    print()

    print("(possible) repository url")
    print()
    try:
        repository_url = repository_url_from_archive_url(url)
        print(repository_url)
    except Exception as e:
        print("Can't find repository url")
        print()
        traceback.print_exc()


if __name__ == '__main__':
    main()
