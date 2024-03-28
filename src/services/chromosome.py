import json
import os

from fastapi import BackgroundTasks, HTTPException

from src.algorithm.ttp.app import run


class ChromosomeSerivce:
    result_path = "data/results/"
    is_running = False

    def get_chromosome_list(self) -> list[str]:
        """
        @return: List of chromosome files without extension
        """
        files = os.listdir(self.result_path)
        chromosome_list = list(filter(lambda x: x[-4:] == "json", files))
        chromosome_list = [chromosome.split(".")[0] for chromosome in chromosome_list]
        return chromosome_list

    def get_chromosome_file(self, filename: str) -> dict:
        """
        @param filename: Name of the file without extension
        @return: Chromosome json file content
        """
        files = os.listdir(self.result_path)
        chromosome_list = [file.split(".")[0] for file in files]

        if filename not in chromosome_list:
            return HTTPException(status_code=404, detail="Item not found")

        result_chromosome = json.load(open(self.result_path + filename + ".json", "r"))

        for chromosome in result_chromosome:
            if len(chromosome["session"]) == 1:
                chromosome["session"] = "0" + chromosome["session"]
            chromosome["course_key"] = str(chromosome["course_id"]) + str(chromosome["class_id"])

        return result_chromosome

    def delete_chromosome_file(self, filename: str) -> list[str]:
        """
        @param filename: Name of the file without extension
        @return: List of chromosome files without extension
        """
        files = os.listdir(self.result_path)
        chromosome_list = [file.split(".")[0] for file in files]

        if filename not in chromosome_list:
            raise HTTPException(status_code=404, detail="Item not found")

        os.remove(self.result_path + filename + ".json")
        return self.get_chromosome_list()

    def post_chromosome(
        self, background_tasks: BackgroundTasks, live: int = 20, popu: int = 20
    ):
        """
        @param live: Number of live
        @param popu: Number of population
        @return: Name of the file without extension
        """

        if self.is_running:
            raise HTTPException(status_code=400, detail="Algorithm is running")

        self.is_running = True

        # TODO: Run the algorithm
        # asyncio.create_task(self.run_algorithm(live, popu))
        background_tasks.add_task(self.run_algorithm, live, popu)

        return HTTPException(status_code=200, detail="Algorithm is running")

    def run_algorithm(self, live: int, popu: int):
        result = None
        result = run(live=live, popu=popu)
        # try:
        # except Exception as e:
        #     print(e)
        # finally:
        self.is_running = False
        # TODO: Save the result to a file
        return result
