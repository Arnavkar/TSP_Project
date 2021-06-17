import argparse
from Objects.visualizer import Visualizer

'''
Description:
------------------
Program to run TSP algorithms with animation using matplotlib

Instructions:
-----------------
1.  To get function description and help, run " python main.py -h "
2.  To run file, run " python main.py -i {PATH TO YOUR TEXT FILE} -a {SELECTED ALGORITHM VIA INT VALUE} {OTHER ARGUMENTS}"
3.  To run sample files provided, run " python main.py -i ./TextFiles/{FILENAME}"

'''

parser = argparse.ArgumentParser(description = "TSP Problem visualizer")
parser.add_argument(
    '-a',
    '--algorithm',
    required=True,
    type = int,
    help = '''Select Algorithm To Solve the TSP Problem. Current Algorithms implemented:\n
    0: No Algorithm \n
    1: Nearest Insertion \n
    2: Smallest Increase \n
    3: Genetic Algorithm \n '''
    )

parser.add_argument(
    '-i',
    '--input-file',
    required=True,
    type=str,
    help= "The relevant input file specifying the axis width and height, and all the listed coordinates"
    )

parser.add_argument(
    '-p',
    '--population-size',
    default = 100,
    type=int,
    help= "Population size for of each generation of the  genetic algorithm"
    )
parser.add_argument(
    '-e',
    '--elite-size',
    default = 15,
    type=int,
    help= "Size of the selected elite from each generation to persist into the subsequent generation"
    )
parser.add_argument(
    '-m',
    '--mutation-rate',
    default = 0.01,
    type=float,
    help= "Value denoting chance for mutation"
    )
parser.add_argument(
    '-g',
    '--generations',
    default = 500,
    type=int,
    help= "Total Number of generations for the genetic algorithm"
    )

parser.add_argument(
    '-r',
    '--experiment-runs',
    default = 1,
    type=int,
    help= "Number of experiments to run for the selected algorithm - NOTE: Do not run with genetic algorithm because it might take super long! "
    )

parser.add_argument(
    '-v',
    '--enable-graph',
    default = 1,
    type = int,
    help = "Setting to matplotlib graphical display (enabled by default, set value to 0 to disable)"
)
args = parser.parse_args()

params = {}

params["popsize"] = args.population_size
params["elitesize"] = args.elite_size
params["mutation"] = args.mutation_rate
params["generations"] = args.generations

if args.algorithm < 0 or args.algorithm > 3:
    raise Exception("Invalid mode provided")

if __name__ == "__main__":
    vis = Visualizer(args.input_file,args.algorithm,args.runs,params,args.enable_graph)
    vis.visualize()
