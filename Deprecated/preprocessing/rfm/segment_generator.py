import pandas as pd
import yaml


def permute_rfm(r_range: list, f_range: list, m_range: list) -> list:
    """Generate a list of tuples `(r, f, m)`

    Args:
        r_range (list): list or `range` of possible r values
        f_range (list): list or `range` of possible f values
        m_range (list): list or `range` of possible m values

    Returns:
        list: a list of tuples `(r, f, m)`
    """
    permutations = []
    for r in r_range:
        for f in f_range:
            for m in m_range:
                permutations.append((r, f, m))

    permutations = set(permutations)
    permutations = list(permutations)
    return permutations


def check_threshold(r: int,
                    f: int,
                    m: int,
                    r_thres: list,
                    fm_thres: list,
                    f_thres: list = None,
                    m_thres: list = None):
    # Python use round to the nearest even number
    # this will handle the result when
    # round(4.5) -> 4 to round(4.5) -> 5
    fm_score = round((f + m + 0.0001) / 2)

    # additional f, m thres
    addtional_fm = True
    if f_thres is not None:
        addtional_fm &= f in f_thres
    if m_thres is not None:
        addtional_fm &= m in m_thres

    return (fm_score in fm_thres) and (r in r_thres) and addtional_fm


def generate_segment_df(threshold_file: str, n_group: int = 5):
    """Generate a dataframe consists of columns to map rfm scores to segment names

    if a score can be in many segment
    this code will choose the segment that comes first in the config

    Args:
        threshold_file (str): yaml file for segment configuration
        n_group (int, optional): number of groups for `pd.qcut`. Defaults to 5.

    Returns:
        _type_: _description_
    """

    with open(threshold_file) as f:
        segments = yaml.load(f, yaml.Loader)

    # generate all score combination
    scores = permute_rfm(range(1, n_group + 1), range(1, n_group + 1), range(1, n_group + 1))

    # check if score in segments
    segment_score = []

    for score in scores:
        for lv, (segment, v) in enumerate(segments.items()):
            v['f'] = None if 'f' not in v.keys() else v['f']
            v['m'] = None if 'm' not in v.keys() else v['m']

            is_in_segment = check_threshold(score[0], score[1], score[2], v['r'], v['fm'], v['f'],
                                            v['m'])
            if is_in_segment:
                result = (segment, "".join([str(i) for i in list(score)]), lv)
                segment_score.append(result)

    df = pd.DataFrame(segment_score, columns=['segment', 'rfm', 'level'])

    # if a score can be in many segment
    # group to the higher lv. (lower index)
    df = df.sort_values('level').drop_duplicates('rfm').reset_index(drop=True)
    df = df.drop(columns=['level'])

    return df