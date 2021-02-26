"""
    Run all items, plot to files by default    
"""
import sys
from ingest import ingest_all_data
from heat_map import plot_heat_maps
from mass_histogram import plot_mass_hist
from percentage_destructive import calculate_percent_destructive
from plot_bar import plot_bar
from machine_learning import regression_model


def main(fileset, popup=False):
    data = ingest_all_data(fileset)
    plot_heat_maps(data, popup)
    plot_mass_hist(data, popup)
    plot_bar(data, popup)
    calculate_percent_destructive(data)
    regression_model(data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main( sys.argv[1], True )
    else:
        main('default')
