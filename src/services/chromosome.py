import json
import os

from fastapi import BackgroundTasks, HTTPException

from src.algorithm.ttp.app import run

SESSION_LIST = [
    "01",
    "02",
    "03",
    "04",
    "20",
    "05",
    "06",
    "07",
    "08",
    "09",
    "30",
    "40",
    "50",
    "60",
    "70",
]


class ChromosomeSerivce:
    result_path = "data/results/"
    is_running = False
    course_data = None

    def get_chromosome_list(self) -> list[str]:
        """
        @return: List of chromosome files without extension
        """
        files = os.listdir(self.result_path)
        chromosome_list = list(filter(lambda x: x[-4:] == "json", files))
        chromosome_list = [chromosome.split(".")[0] for chromosome in chromosome_list]
        chromosome_list.remove("rules")
        chromosome_list = [chromosome for chromosome in chromosome_list if chromosome.find('record') == -1]

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

        file_chromosome = json.load(open(self.result_path + filename + ".json", "r"))

        for chromosome in file_chromosome:
            if len(chromosome["session"]) == 1:
                chromosome["session"] = "0" + chromosome["session"]
            chromosome["course_key"] = str(chromosome["course_id"]) + str(
                chromosome["class_id"]
            )

        # result_chromosome = []

        # for chromosome in file_chromosome:
        #     session = chromosome["session"]
        #     session_idx = SESSION_LIST.index(session)

        #     for i in range(chromosome["session_length"]):
        #         chromosome["session"] = SESSION_LIST[
        #             (session_idx + i) % len(SESSION_LIST)
        #         ]
        #         result_chromosome.append(chromosome.copy())

        return file_chromosome
    
    def evaluate_chromosome_file(self, filename: str) -> dict:
        filename = f'{filename}_record'
        files = os.listdir(self.result_path)
        chromosome_list = [file.split(".")[0] for file in files if file.find('record') != -1]

        if filename not in chromosome_list:
            return HTTPException(status_code=404, detail="Item not found")
        
        file_chromosome = json.load(open(self.result_path + filename + ".json", "r"))

        return file_chromosome
        
        #TODO : Implement the function to evaluate the chromosome file

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
        os.remove(self.result_path + filename + "_record.json")
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
        try:
            result = run(live=live, popu=popu)
        except Exception as e:
            print(e)
        finally:
            self.is_running = False
        # TODO: Save the result to a file
        return result

    def get_rule(self):
        if os.path.isfile("data/results/rules.json"):
            rule = json.load(open("data/results/rules.json", "r"))
        else:
            rule = []
        return rule
    
    def get_chromosome_detail(self):
        if self.course_data is None:
            self.load_course_data()
        return self.course_data
    
    def load_course_data(self):
        raw_data = json.load(open("data/course/course_washed.json", "r"))
        self.course_data = {}

        for course in raw_data:
            self.course_data[course["course_key"]] = {
                "course_id": course["course_id"],
                "class_id": course["class_id"],
                "course_name": course["course_name"],
                "course_type": course["course_type"],
                "session_length": course["session_length"],
            }