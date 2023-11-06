#!/usr/bin/env python
# coding: utf-8


#This file contains original code that I wrote for the purpose of this project
#It was written to obtain specific formats/inputs I needed for other functions
#or to create functions that I needed to perform the analyses I was interested in

#Rearranging .value_counts() output based on specific label order
def ordered_counts(df, col, order):
    counts = []
    for item in order:
        counts.append(df[col].value_counts()[item])
    return counts


#Statistical functions

#I'm aware that you can do these tests with scipy.stats
#I'm not entirely sure why I chose to construct them from scratch back then
#I wouldn't do that now, but here they are

#Z-tests of proportion -- one and two sample

def one_sample_z(p0, p, n, critval):
    numerator = p-p0
    variance = p0*(1-p0)
    denom = math.sqrt(variance/n)
    z = round((numerator/denom), 2)
    if z>critval or z<(-1*critval):
        result = 'reject null hypothesis'
    else:
        result = 'fail to reject null hypothesis'
    return z, result

def two_sample_z_with_p(p1, p2, n1, n2, critval):
    p = (p1 + p2)/2
    numerator = p1 - p2
    variance = p*(1-p)
    sizes = (1/n1 + 1/n2)
    denom = math.sqrt(variance * sizes)
    z = round((numerator/denom), 2)
    if z>critval or z<(-1*critval):
        result = 'reject null hypothesis'
    else:
        result = 'fail to reject null hypothesis'
    return z, result


#For chi-square tests -- frequencies
#After frequencies were calculated, chi-square function from scipy.stats was used

def get_exp_freq(cat1lvls, cat2lvls, cat1counts, cat2counts):
    exp_dict = {}
    for i in range(len(cat1lvls)):
        exp_dict[cat1lvls[i]] = []
        for j in range(len(cat2lvls)):
            prob=round((cat1counts[i]*cat2counts[j])/3000, 3)
            exp_dict[cat1lvls[i]].append(prob)
    return exp_dict

def get_obs_freq(cat1lvls, cat2lvls, grouped_data):
    obs_dict = {}
    for i in range(len(cat1lvls)):
        c = cat1lvls[i]
        obs_dict[c] = []
        for j in range(len(cat2lvls)):
            c2 = cat2lvls[j]
            if c2 not in grouped_data[c]:
                obs_dict[c].append(0)
            else:
                obs_dict[c].append(grouped_data[c][c2])
    return obs_dict
#I'm aware that this could also have been done without having to aggregate data using
#groupby prior to executing this function -- also could have been written by passing
#original data frame and relevant columns and executing groupby within the function
#similarly to how I wrote the get_heatmap function below


#Probabilities of each level of an individual variable
#rounded to 3 decimal places

def get_probs(data, levels):
    prob_dict = {}
    for level in levels:
        prob_dict[level] = (round(data[level][0]/(data[level][0]+data[level][1]),3), 
                           round(data[level][1]/(data[level][0]+data[level][1]),3))
    return prob_dict


#Dictionaries of frequencies for heatmaps

def freq_dict(grouped_data, key_labels, value_labels):
    freqs = {}
    for lab in key_labels:
        freqs[lab] = {}
        for lab2 in value_labels:
            if lab == lab2:
                freqs[lab][lab2] = 0
            elif lab2 not in grouped_data[lab]:
                freqs[lab][lab2] = 0
            else:
                freqs[lab][lab2] = grouped_data[lab][lab2]
    return freqs


#Heatmaps in Appendix C were generated using this function

def get_heatmap(data, x_axis, y_axis, x_labels, y_labels, save_fig=False, file_name=None):
    grouped = data.groupby([y_axis])[x_axis].value_counts()
    frequencies = freq_dict(grouped, y_labels, x_labels) #dictionary of frequencies
    frequencies_df = pd.DataFrame.from_dict(frequencies, orient='index') #df from dict
    frequencies_df = frequencies_df.reindex(axis=0, labels=y_labels) #ordering rows from labels
    frequencies_df = frequencies_df.reindex(axis=1, labels=x_labels) #ordering columns from labels
    
    plt.figure(figsize=(20,10))
    ax = sns.heatmap(frequencies_df, annot=False, vmin=0, vmax=(round(grouped.max(), -1))+30, cmap='rocket_r')
    ax.set_xlabel(x_axis, labelpad=20)
    ax.set_ylabel(y_axis,labelpad=20)
    if save_fig:
        plt.savefig(file_name, bbox_inches='tight', format='eps')

