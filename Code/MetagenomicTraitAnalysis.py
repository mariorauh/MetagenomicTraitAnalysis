# Copyright: Mario Rauh
# v0.0.1

import csv, argparse as ap
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def command_line():
    parser = ap.ArgumentParser("Metagenomic Data Analysis")

    parser.add_argument("-i", "--input", help="Path to files containing Megan trait count information", type=str,
                        nargs='+')
    parser.add_argument("-o", "--output", help="Output file's name", type=str)
    parser.add_argument("-t", "--top", help="Include to select top [top] most abundant traits. "
                                            "We recommend a number between 10 and 40. Default: 10", type=int,
                        default=10)

    return vars(parser.parse_args())


def kegg_conv(megan:str):
    try:
        print(f"Try loading {megan} file into program ...")

        with open(megan, mode='r') as infile:
            reader = csv.reader(infile)
            megan_values = {}
            for row in reader:

                if row[0][:2] == 'ko':
                    id_val = row[0][:7]
                    count = int(row[1])
                    megan_values[id_val] = count

        print(f"Successfully loaded {megan}.")
        return megan_values #dict

    except:
        print(f"{megan} not found or not the right format.")
        return None


def import_all(inp:list, top:int):
    '''
    Import all files to the program and save them in a nested dictionary
    :param inp: input files as list
    :return: dict of dicts with top 10 annotations
    '''

    top_ten = {}

    # loop over all files
    for file in inp:

        megan_values = kegg_conv(file)  # megan_values:dict

        #check if megan values are not None (None is return for files that cant be imported
        if megan_values is not None:

            #sort by values. Highest values are at the end.
            megan_values = {k: v for k, v in sorted(megan_values.items(), key=lambda item: item[1])}
            keys = list(megan_values.keys()) # assign all keys of dict to variable keys

            temp = {} # temp variable to save the last 10 elements in.

            for i in range(1,top+1):
                key = keys[-i]  # get last elements by negating the i

                temp[key] = megan_values[key]

            top_ten[file] = temp    # add dict to final dict

    #print(top_ten)
    return top_ten


def check_multiple_apps(top_ten:dict):
    '''
    Create a ste in which to save all traits that occur
    :param top_ten: dict of dicts containing the annotation ids and appearances
    :return: set: all annotation ids
    '''

    final = []
    # iterate over all dict entries and check for each of their annotations if it is already present in final list
    for file in top_ten.keys():
        temp = top_ten[file]
        traits = list(temp.keys())
        for t in traits:
            if t not in final:
                final.append(t)

    return final


def create_csv(files:list,output:str):
    '''
    create a reference csv file in which a number is assigned a file
    :param files: list of files
    :param output: output name
    :return: a csv file containing reference number and associated file name
    '''

    with open(f'{output}.refs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['ID','Filename'])
        for i,file in enumerate(files):
            spamwriter.writerow([i+1,file])


def create_heatmap(top_ten:dict, id_set:list, out:str):
    '''
    create a heatmap.
    column 0: file names
    row 0: annotation ids
    :param top_ten: dict of dicts containing the annotation ids and appearances
    :param id_set: list containing all ids that appear in all dicts in top_ten
    :param out: output file name
    :return: a heatmap
    '''

    files = list(top_ten.keys())
    # create a predefined np matrix with zeros only. n represents in the number of columns, m rows
    n = len(id_set)
    m = len(files)
    mat = np.zeros((m,n),int)
    #print(mat)
    #print(id_set)
    #fill matrix with correct values.
    for i,file in enumerate(files):
        temp = top_ten[file]
        for trait in temp.keys():
            if trait in id_set:
                ind = id_set.index(trait)
                mat[i][ind] = temp[trait]


    #print(mat)

    short_files = []
    # shorten the file names
    for file in files:
        if "/" in file:
            temp = ""
            for i in range(1,len(file)):
                if file[-i] == "/":
                    break
                temp+=file[-i]
            temp=temp[::-1]
            short_files.append(temp)
        else:
            short_files.append(file)

    files = short_files

    create_csv(files, out)

    files_number = []
    for i in range(len(files)):
        files_number.append(i+1)

    # create final heatmap based on above matrix
    fig, ax = plt.subplots()

    im = ax.imshow(mat)
    ax.set_xticks(np.arange(len(id_set)))
    ax.set_yticks(np.arange(len(files)))
    ax.set_xticklabels(id_set)
    ax.set_yticklabels(files_number)
    plt.xticks(rotation=90)
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    # added divider for colorbar. Adapted from stackoverflow.com
    divider = make_axes_locatable(ax)
    cax = divider.new_vertical(size="20%", pad=1, pack_start=True)
    fig.add_axes(cax)
    fig.colorbar(im, cax=cax, orientation="horizontal")
    '''
    # create cell labels
    for i in range(len(files)):
        for j in range(len(id_set)):
            text = ax.text(j, i, mat[i, j], ha="center", va="center", color="w")
    '''
    ax.set_title("Heatmap Megan Annotations")
    fig.tight_layout()
    plt.savefig(f"{out}.kegg.heat.png", dpi=1024)
    plt.close()


def exec():
    print("Metagenomic Data Analysis")
    args = command_line()
    inp, out, top = args["input"], args["output"], abs(args["top"])

    top_ten = import_all(inp, top)
    id_set = check_multiple_apps(top_ten)
    create_heatmap(top_ten, id_set,out)

def main():

    exec()


if __name__ == '__main__':
    main()