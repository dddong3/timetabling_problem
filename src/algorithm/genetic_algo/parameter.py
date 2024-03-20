class GeneticAlgoParameter:
    def __init__(
        self,
        population_size: int,
        mutation_rate: float,
        crossover_rate: float,
        crossover_strategy: str,
        mutate_strategy: str,
        select_strategy: str,
        max_generation: int,
        loops=1,
        **kwargs
    ):
        """
        @params population_size: int
        @params mutation_rate: float
        @params crossover_rate: float
        @params crossover_strategy: str
        @params mutate_strategy: str
        @params select_strategy: str
        @params max_generation: int
        @params loops: int
        @params kwargs: Any

        Initialize GeneticAlgoParameter.
        """
        self.chromosome_type = "TTP"
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.crossover_strategy = crossover_strategy
        self.mutate_strategy = mutate_strategy
        self.select_strategy = select_strategy
        self.max_generation = max_generation
        self.loops = loops
        [setattr(self, k, v) for k, v in kwargs.items()]


# genetic_algo_parameter: GeneticAlgoParameter = GeneticAlgoParameter()
