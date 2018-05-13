import click
import datetime
from requests_cache import CachedSession
import pandas as pd
# import semver
from utils import download_index
import tempfile
from zipfile import ZipFile


@click.command()
@click.option('--max-rows', default=20, help='Number of rows to display.')
@click.option('--cache', default=7, help='Number of days to cache queries.')
@click.option('--name', default='', help='Name of library (ArduinoJSON for example)')
def main(max_rows, cache, name):
    pd.set_option("max_rows", max_rows)
    expire_after = datetime.timedelta(days=cache)
    session = CachedSession(cache_name='cache', backend='sqlite',
                            expire_after=expire_after)
    df, df_last = download_index(session)

    df_all_versions = df[df['name'] == name]
    df_all_versions = df_all_versions.set_index('version')
    print(df_all_versions)

    print("")

    latest_version = df_last[df_last.index == name].iloc[0]
    print(latest_version)

    url = latest_version.url

    print()

    print("Downloading from %r" % url)
    assert url[-4:] == '.zip', "URL must finish with .zip"

    r = session.get(url)
    raw = r.content

    with tempfile.TemporaryFile() as tmpf:
        tmpf.write(raw)

        with ZipFile(tmpf, 'r') as zf:
            license_filenames = []
            for filename in zf.namelist():
                filename_upper = filename.upper()
                if 'LICENSE' in filename_upper or 'LICENCE' in filename_upper:
                    license_filenames.append(filename)
            assert len(license_filenames) == 1, \
                "Several license files have been found"
            license_filename = license_filenames[0]

            print()
            print(license_filename)
            data = zf.open(license_filename).read().decode()
            print(data)


if __name__ == '__main__':
    main()
