import pandas as pd
from pandas.io.json import json_normalize
import re
from requests_cache import CachedSession
import datetime
import tempfile
from zipfile import ZipFile
import semver


EXPIRE_AFTER_DEFAULT = datetime.timedelta(days=7)
MAX_ROWS_DEFAULT = 10
THRESHOLD_DEFAULT = 0.2
SEARCH_IN_DEFAULT = ['name', 'paragraph', 'sentence', 'category']


def init_session(expire_after=EXPIRE_AFTER_DEFAULT, session=None):
    if session is None:
        session = CachedSession(cache_name='cache/cache', backend='sqlite',
                                expire_after=expire_after)
    return session


def init_index(df=None, session=None, ascending=False):
    if df is None:
        return download_index(session, ascending)
    return df


def download_index(session=None, ascending=False):
    if session is None:
        session = init_session(session)
    url = "http://downloads.arduino.cc/libraries/library_index.json"
    r = session.get(url)
    d = r.json()
    libraries = d['libraries']
    df = json_normalize(libraries)
    df['version'] = df['version'].map(semver.parse_version_info)
    # raises TypeError: unhashable type: 'VersionInfo'
    # see https://github.com/k-bx/python-semver/issues/73
    df = df.sort_values(by=['name', 'version'], ascending=[True, ascending])
    return df


def repository_url_from_archive_url(url):
    pattern = re.compile(r"http:\/\/downloads\.arduino\.cc\/libraries\/(.*)/(.*)\/(.*)-(.*).zip")
    match = pattern.match(url)
    allowed_websites = ['github.com']
    if match is None:
        raise NotImplementedError("Can't match")
    website, username, repository, version = match.groups()
    if website == 'github.com':
        repository_url = "https://github.com/%s/%s" % (username, repository)
    else:
        raise NotImplementedError("Website is %r but only website in %r are currently supported" % (website, allowed_websites))
    return repository_url


def add_possible_repository_url(df):
    def _possible_repository_url(url):
        try:
            repository_url = repository_url_from_archive_url(url)
            # repository_url = repository_url.lower()
            return repository_url
        except Exception as e:
            return ""
    df['possible_url_repository'] = df['url'].map(_possible_repository_url)
    df['have_repo_like_archive'] = df['website'].str.lower() == df['possible_url_repository'].str.lower()
    return df


def dice_coefficient(a, b):
    """
    From https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Dice%27s_coefficient
    """
    if not len(a) or not len(b):
        return 0.0
    if a == b:
        return 1.0
    if len(a) == 1 or len(b) == 1:
        return 0.0

    a_bigram_list = [a[i:i + 2] for i in range(len(a) - 1)]
    b_bigram_list = [b[i:i + 2] for i in range(len(b) - 1)]

    a_bigram_list.sort()
    b_bigram_list.sort()

    # assignments to save function calls
    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)
    # initialize match counters
    matches = 0
    i = 0
    j = 0
    while (i < lena and j < lenb):
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1

    score = float(matches) / float(lena + lenb)
    return score


def find_nearest_names(name, threshold=THRESHOLD_DEFAULT, df=None):
    df = init_index(df)
    library_names = df.name.unique()
    df_nearest = pd.DataFrame()
    df_nearest['name'] = library_names
    name_upper = name.upper()
    df_nearest['score'] = df_nearest['name'].str.upper().map(lambda n: dice_coefficient(n, name_upper))
    df_nearest = df_nearest[df_nearest['score'] >= threshold]
    df_nearest = df_nearest.sort_values(by='score', ascending=False)
    df_nearest.index = range(1, len(df_nearest) + 1)
    return df_nearest


def find_nearest_name(name, threshold=THRESHOLD_DEFAULT, df=None):
    df_nearest = find_nearest_names(name, threshold, df)
    if len(df_nearest) == 0:
        raise NotImplementedError("Can't find a nearest name with such a threshold (%f) try reducing or with a better name than %s" % (threshold, name))
    return df_nearest['name'].iloc[0]


def get_versions(name, df=None, ascending=False):
    df = init_index(df)
    df_library = df[df['name'] == name]
    df_library = df_library.sort_values(by='version', ascending=True)
    df_library.index = range(1, len(df_library) + 1)
    df_library = df_library.sort_values(by='version', ascending=ascending)
    return df_library['version']


def get_latest_version(name, df=None):
    return get_versions(name, ascending=True, df=df).iloc[-1]


def init_version(name, version=None, df=None):
    if version is None:
        return get_latest_version(name, df)
    else:
        return version


def get_archive_url(name, version, df):
    df_library = df[df['name'] == name]
    df_library_version = df_library[df_library['version'] == version]
    n = len(df_library_version)
    if n == 0:
        raise Exception("No library matching name '{name}' have been found try `find_nearest_name('{name}') or `find_nearest_names('{name}')`".format(name=name))
    elif n > 1:
        raise Exception("Only one library with a given version should be found - several have been found")
    else:  # n==1
        return df_library_version.url.iloc[0]


def show_licence_from_archive_url(url, session=None):
    session = init_session(session)

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

                    print()
                    print(filename)
                    print()
                    data = zf.open(filename).read().decode()
                    print(data)

    n_licenses = len(license_filenames)

    if n_licenses == 0:
        print("No license have been found")
    elif n_licenses > 1:
        print("Several license files have been found")

    return n_licenses


def show_licence(name, version=None, session=None):
    df = download_index(session)
    version = init_version(name, version=version, df=df)
    url = get_archive_url(name, version, df)
    show_licence_from_archive_url(url, session)


def show_versions(name, session=None):
    df = download_index(session)
    versions = get_versions(name, df=None, ascending=False)
    if len(versions) == 0:
        print(find_nearest_names(name, df=df))
        raise Exception("No library matching name '{name}' have been found try `find_nearest_name('{name}')` or `find_nearest_names('{name}')`".format(name=name))
    return versions


def search(keywords, columns_search=None, session=None, df_last=None):
    if df_last is None:
        df = download_index(session)
        df_last = df.groupby('name').first().reset_index()
    if columns_search is None:
        columns_search = SEARCH_IN_DEFAULT
    keywords = keywords.split(" ")
    ser_have_keyword = pd.Series(False, index=df_last.index)
    for keyword in keywords:
        for col in columns_search:
            ser_have_keyword = ser_have_keyword | df_last[col].str.contains(keyword, case=False).fillna(False)
        # ser_have_keyword = ser_have_keyword & ...
    df_search = df_last[ser_have_keyword]
    n_found = len(df_search)
    print(df_search.set_index('name'))
    print()
    print("Found %d libraries" % n_found)
    return df_search
