import lucene
import os
import sys
#define the root folder so that python recognises packages
lucene_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(lucene_folder)))
sys.path.append(root_folder)

#from VINF_Parser.src.vinf_parser import VINF_Parser
from vinf_lucene_controller import VINF_Lucene_Controller


def choose_mode(available_modes, mode_choice_prompt):
    mode_chosen = False
    mode = 0
    while not mode_chosen:
        prompt_input = input(mode_choice_prompt).strip()
        if prompt_input in available_modes:
            mode = int(prompt_input)
            mode_chosen = True
        else:
            print("Incorrect input! Try again.")
    return mode

def make_person_choice(available_choices, prompt):
    chosen = False
    while not chosen:
        choice = input(prompt).strip()
        if choice in available_choices:
            chosen = True
            return choice
        else:
            print("Invalid choice! Try again.")
        pass

def could_they_have_met(record1, record2):
    p1_bd = record1["birth_date"]
    p1_dd = record1["death_date"]

    p2_bd = record2["birth_date"]
    p2_dd = record2["birth_date"]

    return True

def mode_one(lucene_controller):
    done = False
    mode_one_prompt_info = """\nIn this mode you will select two people based on your search and find out they could have met :)"""
    mode_one_prompt_one = """Search for the first person:"""
    mode_one_prompt_two = """Search for the second person:"""
    mode_one_prompt_choice = """Select which person you want to pick:\t"""
    mode_one_prompt_search = """Enter the words you want to search for:\t"""

    print(mode_one_prompt_info)
    while not done:
        person_one_selected = False
        person_one_record = None
        while not person_one_selected:
            print(mode_one_prompt_one)
            tokens = input(mode_one_prompt_search).strip()
            search_results = lucene_controller.search_index("title", tokens, "OR")
            #TODO SORT ARRAY ACCORING TO SCORE
            result_counter = 0
            available_choices = ['0']
            result_records = []
            print("0.\tNone of the results. Lets search again!")
            for result in search_results:
                result_counter += 1
                available_choices.append(str(result_counter))
                record = lucene_controller.get_record_from_doc(result)
                result_records.append(record)
                print(f"{result_counter}.\tsearch score: {result.score}\t{record['title']}")
            
            choice = make_person_choice(available_choices, mode_one_prompt_choice)
            if choice == '0':
                pass
            else:
                print(f"You chose {result_records[int(choice) - 1]['title']}")
                person_one_record = result_records[int(choice) - 1]
                person_one_selected = True

        person_two_selected = False
        person_two_record = None
        while not person_two_selected:
            print(mode_one_prompt_two)
            tokens = input(mode_one_prompt_search).strip()
            search_results = lucene_controller.search_index("title", tokens, "OR")
            #TODO SORT ARRAY ACCORING TO SCORE
            result_counter = 0
            available_choices = ['0']
            result_records = []
            print("0.\tNone of the results. Lets search again!")
            for result in search_results:
                result_counter += 1
                available_choices.append(str(result_counter))
                record = lucene_controller.get_record_from_doc(result)
                result_records.append(record)
                print(f"{result_counter}.\tsearch score: {result.score}\t{record['title']}")
            
            choice = make_person_choice(available_choices, mode_one_prompt_choice)
            if choice == '0':
                pass
            else:
                print(f"You chose {result_records[int(choice) - 1]['title']}")
                person_two_record = result_records[int(choice) - 1]
                person_two_selected = True
        pass



if __name__ == '__main__':

    #relevant directories
    data_directory = lucene_folder + '/data'
    index_directory = data_directory + '/index'
    records_directory = root_folder + '/VINF_Parser/data'

    #controllers - lucene, and parser
    luc = VINF_Lucene_Controller()
    
    #state of the user promptn
    prompt_active = True
    mode_chosen = False
    mode = 0
    available_modes = ['1']

    mode_choice_prompt = """\nChoose the mode of searching:\
                            \n\t1.\tCould they have met? (two people)\
                            \n\t2.\tNot functional yet!\
                            \nEnter your choice (to select enter the number of the choice):"""

    while(prompt_active):
        #choose mode of operation
        mode = choose_mode(available_modes=available_modes, mode_choice_prompt=mode_choice_prompt)
        if str(mode) in available_modes:
            if mode == 1:
                mode_one(luc)
            else:
                pass
            

        

        




