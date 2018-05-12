from pandas.io.json import json_normalize


def download_index(session):
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
    return df, df_last
