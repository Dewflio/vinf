import lucene
import os
import sys
import datetime
#define the root folder so that python recognises packages
lucene_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(lucene_folder)))
sys.path.append(root_folder)

#from VINF_Parser.src.vinf_parser import VINF_Parser
from vinf_lucene_controller import VINF_Lucene_Controller


def make_choice(available_choices, prompt):
    chosen = False
    while not chosen:
        choice = input(prompt).strip()
        if choice in available_choices:
            chosen = True
            return choice
        else:
            print("Invalid input! Try again.")
        pass

def is_date_less_than(date1, date1_bc, date2, date2_bc):
    #if date1 == None and date2 == None:
    #    return False
    if date1 == None:
        return False
    elif date2 == None:
        return True
    
    year1 = date1.year if not date1_bc else -1 * date1.year
    month1 = date1.month
    day1 = date1.day
    year2 = date2.year if not date2_bc else -1 * date2.year
    month2 = date2.month
    day2 = date2.day

    if year1 < year2:
        return True
    elif year1 == year2:
        if month1 < month2:
            return True
        elif month1 == month2:
            if day1 < day2:
                return True
    return False

def is_overlap(p1_bd, p1_dd, p1_bd_bc, p1_dd_bc, p2_bd, p2_dd, p2_bd_bc, p2_dd_bc):
    answer = False
    if is_date_less_than(p1_bd, p1_bd_bc, p2_bd, p2_bd_bc) and is_date_less_than(p2_bd, p2_bd_bc, p1_dd, p1_dd_bc):
        answer = True
    if is_date_less_than(p2_bd, p2_bd_bc, p1_bd, p1_bd_bc) and is_date_less_than(p1_bd, p1_bd_bc, p2_dd, p2_dd_bc):
        answer = True
    return answer


def could_they_have_met(record1, record2):
    p1_bd = record1["birth_date"]
    p1_dd = record1["death_date"]
    p1_bd_bc = record1["birth_date_is_bc"]
    p1_dd_bc = record1["death_date_is_bc"]

    p2_bd = record2["birth_date"]
    p2_dd = record2["death_date"]
    p2_bd_bc = record2["birth_date_is_bc"]
    p2_dd_bc = record2["death_date_is_bc"]

    answer = is_overlap(p1_bd, p1_dd, p1_bd_bc, p1_dd_bc, p2_bd, p2_dd, p2_bd_bc, p2_dd_bc)
    return answer

def search_and_choose(lucene_controller, prompts, attribute):
    person_selected = False
    person_record = None
    while not person_selected:
        print(prompts[0])
        tokens = input(prompts[1]).strip()
        search_results = lucene_controller.search_index(attribute, tokens, "OR")
        #TODO SORT ARRAY ACCORING TO SCORE
        result_counter = 0
        available_choices = ['0']
        result_records = []
        print("Search results:")
        print("0.\tNone of the results. Let's search again!")
        for result in search_results:
            result_counter += 1
            available_choices.append(str(result_counter))
            record = lucene_controller.get_record_from_doc(result)
            result_records.append(record)
            print(f"{result_counter}.\tsearch score: {result.score}\t{record['title']}")
        
        choice = make_choice(available_choices, prompts[2])
        if choice == '0':
            pass
        else:
            print(f"You chose {result_records[int(choice) - 1]['title']}")
            person_record = result_records[int(choice) - 1]
            person_selected = True

    return person_record

def mode_one(lucene_controller):
    done = False
    mode_one_prompt_info = """\nIn this mode you will select two people based on your search and find out they could have met :)"""
    mode_one_prompt_one = """Search for the first person:"""
    mode_one_prompt_two = """Search for the second person:"""
    mode_one_prompt_choice = """Select which person you want to pick:\t"""
    mode_one_prompt_search = """Enter the words you want to search for:\t"""

    print(mode_one_prompt_info)
    while not done:
        person_one_record = search_and_choose(lucene_controller=lucene_controller,
        prompts=(mode_one_prompt_one, mode_one_prompt_search, mode_one_prompt_choice),
        attribute="title")

        person_two_record = search_and_choose(lucene_controller=lucene_controller,
        prompts=(mode_one_prompt_two, mode_one_prompt_search, mode_one_prompt_choice),
        attribute="title")

        answer = could_they_have_met(person_one_record, person_two_record)

        if answer:
            print(f"\nYes! {person_one_record['title']} and {person_two_record['title']} could have met.")
        else:
            print(f"\nNo! {person_one_record['title']} and {person_two_record['title']} could not have met.")

        p1_bd_bc_str = " BC" if person_one_record['birth_date_is_bc'] else ""
        p1_dd_bc_str = " BC" if person_one_record['death_date_is_bc'] else ""
        p2_bd_bc_str = " BC" if person_two_record['birth_date_is_bc'] else ""
        p2_dd_bc_str = " BC" if person_two_record['death_date_is_bc'] else ""

        p1_dd_str = f" and died {person_one_record['death_date']}" if person_one_record['death_date'] != None else " and is still alive - at least according to our data :)"
        p2_dd_str = f" and died {person_two_record['death_date']}" if person_two_record['death_date'] != None else " and is still alive - at least according to our data :)"

        print(f"\t{person_one_record['title']} was born {person_one_record['birth_date']}" + p1_bd_bc_str + p1_dd_str + p1_dd_bc_str)
        print(f"\t{person_two_record['title']} was born {person_two_record['birth_date']}" + p2_bd_bc_str + p2_dd_str + p2_dd_bc_str)

        choices = ["y", "N"]
        choice = make_choice(choices, "\nDo you want to continue searching in this mode? (y/N)")
        if choice == 'y':
            pass
        else:
            done = True




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
        mode = make_choice(available_modes, mode_choice_prompt)
        if str(mode) in available_modes:
            if mode == '1':
                mode_one(luc)
            else:
                pass
            

        

        




