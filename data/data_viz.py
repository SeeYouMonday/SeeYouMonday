import matplotlib.pyplot as plt
import csv
import pandas as pd
import itertools
from data.match import parse_terms
from collections import Counter
import numpy as np
import os


def get_terms(file):
    df = pd.read_csv(file, encoding='utf-8')
    terms_column = df['Terms']
    term_list = [term for terms_row in terms_column for term in parse_terms(terms_row)]
    return term_list


def data_viz(file, title, picname):
    terms = get_terms(file)
    terms_counter = Counter(terms)

    most_common = terms_counter.most_common(20)
    keys = [x[0] for x in most_common]
    values = [x[1] for x in most_common]

    y_pos = np.arange(20)
    plt.barh(y_pos, values, align='center', alpha=0.5, color='#43967F')
    plt.yticks(y_pos, keys)
    plt.title(title)
    plt.gca().invert_yaxis()

    figure = plt.gcf()  # get current figure
    figure.set_size_inches(10, 8)

    plt.savefig(os.path.join(os.pardir, 'static', 'viz', '{}.png'.format(picname)), dpi=100)
    # plt.savefig(os.path.join('../static/viz/{}.png'.format(picname)), dpi=100)

    plt.show()


if __name__ == "__main__":
    data_viz('out.csv', 'All Roles', 'out')
    data_viz('computer-systems.csv', 'Computer Systems', 'computer-systems')
    data_viz('data-scientist.csv', 'Data Scientist', 'data-scientist')
    data_viz('software-engineer.csv', 'Software Engineering', 'software-engineer')
