import time
import tqdm
from genetic_algo import GeniticAlgoithm
from multiprocessing import Process, Manager


def run_ga(all_ga: list[int]) -> None:
    FILE_NAME = 'test_gene_washed.json'
    # FILE_NAME = 'little_gene.json'
    ga = GeniticAlgoithm(FILE_NAME, 'class.json', live=1000, popu=100)
    all_ga.append(ga)

def main() -> None:

    loops = 10

    with Manager() as manager:
        all_ga = manager.list()
        threads = [Process(target=run_ga, args=(all_ga,)) for _ in range(loops)]
        [_.start() for _ in threads]
        [_.join() for _ in tqdm.tqdm(threads)]
        all_ga = list(all_ga)

    all_fitness = [_.best_fitness for _ in all_ga]
    all_fitness, all_ga = zip(*sorted(zip(all_fitness, all_ga), reverse=True))
    print(all_fitness[:10])
    all_ga[0].output_chromosome()

if __name__ == '__main__':
    main()