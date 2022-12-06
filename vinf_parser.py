import re       #regex
import bz2      #bz2 compression reading
import logging
import parse
import dateutil.parser
import json

#define root folder of this file
import os
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

from vinf_date import *
from vinf_utils import *


year_re = r"[0-9]{1,4}"
curly_re = r"{{(.)*?[0-9](.)*?}}" #we are only interested in brackets with digits in them
lll = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\S*\s+"
mid_bc = r"((\s*(BC)|(CE)|(AD)\s*)|\s*)" #handles cases where AD or BC is written before the year
#bracket types
df_bd = r"(?i)((?<=birth( |-|_)date)|(?<=birthdate)|(?<=start date))\s*(?=\|)(.)*?(?=}})"          #YYYY|mm|dd
df_dd = r"(?i)((?<=death( |-|_)date)|(?<=deathdate))\s*(?=\|)(.)*?(?=}})"          #YYYY|mm|dd    
df_bda = r"(?i)((?<=birth( |-|_)date and age)|(?<=bda))\s*(?=\|)(.)*?(?=}})" #YYYY|mm|dd
df_dda = r"(?i)((?<=death( |-|_)date and age)|(?<=dda))\s*(?=\|)(.)*?(?=}})" #YYYY|mm|dd
df_bya = r"(?i)(?<=birth( |-|_)year and age)\s*(?=\|)(.)*?(?=}})" #YYYY|YYYY
df_dya = r"(?i)(?<=death( |-|_)year and age)\s*(?=\|)(.)*?(?=}})" #YYYY|YYYY
df_by = r"(?i)(?<=birth( |-|_)year)\s*(?=\|)(.)*?(?=}})" #YYYY|YYYY
df_dy = r"(?i)(?<=death( |-|_)year)\s*(?=\|)(.)*?(?=}})" #YYYY|YYYY
df_c = r"(?i)((?<=circa\|)|(?<=\bc\.\|)|(?<=\bca\.\|))(.)*(?=}})"
df_old = r"(?<=OldStyleDate\|)\s*[0-9]{1,2}\s*[a-zA-Z]+\s*\|\s*[0-9]{1,4}"
df_bdaa = r"(?i)(?<=birth based on age as of date\|)(.)*(?=}})" #age|YYYY|mm|dd
df_nowrap = r"(?i)(?<=nowrap\|)(.)*(?=}})"
#date formats
df_month_dd_yyyy = r"(?i)" + lll + r"[0-9]{1,2}(,|\s)\s*[0-9]{1,4}((\s*(BC|CE|AD))|\s*?|(?=\S))"  #r"[a-zA-Z]+\s+
df_dd_month_yyyy = r"(?i)" + r"[0-9]{1,2}\s*" + lll + mid_bc + r"[0-9]{1,4}((\s*(BC|CE|AD))|\s*?|(?=\S))"  #[a-zA-Z]+\s*
df_yyyyImmIdd = r"(?i)" + r"[0-9]{1,4}\|[0-9]{1,2}\|[0-9]{1,2}"
df_yyyy = r"(?i)" + r"((?<=\bc\.)|(?<=\bca\.)|\s*?)\s*?[0-9]{1,4}((\s*?(BC|CE|AD))|\s*?|(?=\S))"

class VINF_Parser:
    def __init__(self):
        self.data_directory = './data/'
        #init dateutil parser so that assuming century from ambiguous dates is turned off
        old_init = dateutil.parser._parser._ymd.__init__
        def new_init(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            self.century_specified = True
        dateutil.parser._parser._ymd.__init__ = new_init

    def fill_in_year(self, year_str):
        #isolate the digits into a separate string
        new_str = re.search(year_re, year_str)
        if new_str == None:
            return year_str
        new_str = new_str.group().strip() #save the string and strip just for good measure
        res_str = new_str
        if len(new_str)<4:
            res_str = "01 01 "
            for i in range(4-(len(new_str))):
                res_str += "0"
            res_str += new_str
        return res_str

    def split_xml_into_pages(self, filename):
        with bz2.open(filename, "r") as file:
            lines = file.read().decode()
            pages_arr = lines.split("<page>")
            return pages_arr

    def filter_array_str(self, records_arr ,filter_string):
        result_arr = []
        for record in records_arr:
            if filter_string in record:
                result_arr.append(record)
        return result_arr

    def process_attribute_group(self, grp):
        #gets rid of the | attribute_name =
        attr_name_re = r"\|\s*(.)*?\s*="
        attr_name_search  = re.search(attr_name_re, grp)
        if attr_name_search != None:
            attr_name_end_idx = attr_name_search.span()[1]
            grp_str = grp[attr_name_end_idx:]
        else:
            grp_str = grp

        return grp_str.strip()

    def create_datetimebc(self, year=None, month=None, day=None, bc=False):
        dt = DateBC()
        dt.bc = bc
        if year != None:
            dt.year = year
        if month != None:
            dt.month = month
        if day != None:
            dt.day = day
        return dt

    def process_date(self, date_str):# -> DateBC:
        bracket_types = [
            df_bd,
            df_dd,
            df_bda,
            df_dda,
            df_c,
            df_old,
            df_bdaa,

            df_bya,
            df_dya,

            df_by,
            df_dy,
            df_nowrap
        ]
        format_prio = [
            df_month_dd_yyyy,
            df_dd_month_yyyy,
            df_yyyy,
        ]
        res_date = None
        date_found_in_curly = False
        curly_bracket_coords = []
        #check if any of the brackets contain the date
        for x in re.finditer(curly_re, date_str):
            grp = x.group()
            curly_bracket_coords.append(x.span())
            
            search = None
            #identify the type of curly bracket
            for type_re_idx in range(len(bracket_types)):
                search = re.search(bracket_types[type_re_idx], grp)
                if search != None:
                    s_grp = search.group()
                    #search for YYYY|mm|dd
                    #the first four types have dates in this format
                    if type_re_idx < 4:
                        date_search = re.search(df_yyyyImmIdd, s_grp)
                        if date_search != None:
                            #we found a date inside the bracket
                            #lets parse it
                            date_arr = list(parse.parse("{0}|{1}|{2}", date_search.group()))
                            res_date = DateBC(year=int(date_arr[0]), month=int(date_arr[1]), day=int(date_arr[2]))
                            res_date.year_active = True 
                            res_date.month_active = True
                            res_date.day_active = True
                            if "BC" in date_str:
                                res_date.bc = True
                            date_found_in_curly = True
                            break
                        else:
                            #different formats than YYYY|mm|dd in brackets of type {{birth date and ...}}
                            for fp_idx in range(len(format_prio)):
                                date_search = re.search(format_prio[fp_idx], s_grp)
                                if date_search != None: 
                                    if fp_idx == 0 or fp_idx == 1:
                                        dt = dateutil.parser.parse(date_search.group(), fuzzy=True)
                                        res_date = DateBC(year=dt.year, month=dt.month, day=dt.day)
                                        res_date.year_active = True
                                        res_date.month_active = True
                                        res_date.day_active = True
                                    elif fp_idx == 2:
                                        str_to_parse = self.fill_in_year(date_search.group())
                                        dt = dateutil.parser.parse(str_to_parse, fuzzy=True)
                                        res_date = DateBC(year=dt.year, month=1, day=1)
                                        res_date.year_active = True
                                    if "BC" in date_str:
                                        res_date.bc = True
                                    date_found_in_curly = True
                                    break
                    
                    elif type_re_idx == 4:
                        for fp_idx in range(len(format_prio)):
                            date_search = re.search(format_prio[fp_idx], s_grp)
                            if date_search != None:
                                if fp_idx == 0 or fp_idx == 1:
                                    dt = dateutil.parser.parse(date_search.group(), fuzzy=True)
                                    res_date = DateBC(year=dt.year, month=dt.month, day=dt.day)
                                    res_date.year_active = True
                                    res_date.month_active = True
                                    res_date.day_active = True
                                elif fp_idx == 2:
                                    str_to_parse = self.fill_in_year(date_search.group())
                                    dt = dateutil.parser.parse(str_to_parse, fuzzy=True)
                                    res_date = DateBC(year=dt.year, month=1, day=1)
                                    res_date.year_active = True
                                if "BC" in date_str:
                                    res_date.bc = True
                                date_found_in_curly = True
                                break
                    elif type_re_idx == 5:
                        dt = dateutil.parser.parse(s_grp, fuzzy=True)
                        res_date = DateBC(year=dt.year, month=dt.month, day=dt.day)
                        res_date.year_active = True
                        res_date.month_active = True
                        res_date.day_active = True
                        if "BC" in date_str:
                                res_date.bc = True
                        date_found_in_curly = True
                        break
                    elif type_re_idx == 6: #TODO: RESOLVE NONETYPE ERROR 
                        date_arr = list(parse.parse("{0}|{1}|{2}|{3}", s_grp))
                        res_date = DateBC(year=int(date_arr[1]) - int(date_arr[0]), month=int(date_arr[2]), day=int(date_arr[3]))
                        res_date.year_active = True
                        res_date.month_active = True
                        res_date.day_active = True
                        if "BC" in date_str:
                                res_date.bc = True
                        date_found_in_curly = True
                        break
                    elif type_re_idx == 7 or type_re_idx == 8 or type_re_idx == 9 or type_re_idx == 10 or type_re_idx == 11:
                        date_search = re.search(df_yyyy, s_grp)
                        if date_search != None:
                            str_to_parse = self.fill_in_year(date_search.group())
                            dt = dateutil.parser.parse(str_to_parse, fuzzy=True)
                            res_date = DateBC(year=dt.year, month=1, day=1)
                            res_date.year_active = True
                            if "BC" in date_str:
                                res_date.bc = True
                            date_found_in_curly = True
                            break

        if date_found_in_curly:
            return res_date
        else:
            date_found_outside = False
            new_str = re.sub(r"{{.*?}}", " ", date_str)
                    
            for fp_idx in range(len(format_prio)):
                date_search = re.search(format_prio[fp_idx], new_str)
                if date_search != None:
                    
                    if fp_idx == 0 or fp_idx == 1:
                        dt = dateutil.parser.parse(date_search.group(), fuzzy=True)
                        res_date = DateBC(year=dt.year, month=dt.month, day=dt.day)
                        res_date.year_active = True
                        res_date.month_active = True
                        res_date.day_active = True
                    elif fp_idx == 2:
                        str_to_parse = self.fill_in_year(date_search.group())
                        dt = dateutil.parser.parse(str_to_parse, fuzzy=True)
                        res_date = DateBC(year=dt.year, month=1, day=1)
                        res_date.year_active = True
                    if "BC" in new_str:
                        res_date.bc = True
                    date_found_outside = True
                    break
            if date_found_outside:
                return res_date
            else:
                return None

    def parse_record(self, record):
        tl_re = r"(?<=<title>)(\n|.)*?(?=</title>)"                 #title 
        ct_re = r"(?<={{Infobox)\s+\S+"                             #categories 
        nm_re = r"\|\s*name(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"          #name
        bd_re = r"\|\s*birth_date(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"    #bith date 
        dd_re = r"\|\s*death_date(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"    #death date
        bp_re = r"\|\s*birth_place(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"   #birth place
        dp_re = r"\|\s*death_place(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"   #death place

        tl_srch = re.search(tl_re, record)
        ct_srch = re.search(ct_re, record)
        nm_srch = re.search(nm_re, record)
        bd_srch = re.search(bd_re, record)   
        dd_srch = re.search(dd_re, record)   
        bp_srch = re.search(bp_re, record)   
        dp_srch = re.search(dp_re, record)

        tl_str = ""
        ct_str = ""
        nm_str = ""
        bd_str = ""   
        dd_str = ""   
        bp_str = ""   
        dp_str = ""

        bd_date = None
        bd_is_bc = False

        dd_date = None
        dd_is_bc = False
        
        if tl_srch != None:
            tl_str = self.process_attribute_group(tl_srch.group())
        if ct_srch != None:
            ct_str = self.process_attribute_group(ct_srch.group())
        if nm_srch != None:
            nm_str = self.process_attribute_group(nm_srch.group())
        if bd_srch != None:
            bd_str = self.process_attribute_group(bd_srch.group())
            try:                                                    #TODO: TEMP ADDED TRY EXCEPT TO HANDLE THE BULLSHIT
                bd_date = self.process_date(bd_str)
            except (ValueError, TypeError):
                bd_date = None
            if bd_date != None:
                bd_is_bc = bd_date.bc
        if dd_srch != None:
            dd_str = self.process_attribute_group(dd_srch.group())
            try:
                dd_date = self.process_date(dd_str)
            except (ValueError, TypeError):
                dd_date = None
            if dd_date != None:
                dd_is_bc = dd_date.bc
        if bp_srch != None:
            bp_str = self.process_attribute_group(bp_srch.group())
        if dp_srch != None:
            dp_str = self.process_attribute_group(dp_srch.group())

        record_dict = {
            "title":        tl_str,
            "categories":   ct_str,
            "name":         nm_str,
            "birth_date":   str(bd_date),
            "birth_date_is_bc": ("true" if bd_is_bc else "false"),
            "death_date":   str(dd_date),
            "death_date_is_bc": ("true" if dd_is_bc else "false"),
            "birth_place":  "",#bp_str,
            "death_place":  "",#dp_str,         #TODO TEMPORARILY REMOVED BIRTH AND DEATH PLACE
        }
        return record_dict
        
    def parse_records(self, input_xml, read_xml=True, write_to_json=True):
        pages = []
        people = []
        serialization_file = self.data_directory + "test.pickle"

        if read_xml:
            pages = self.split_xml_into_pages(input_xml)
            people = self.filter_array_str(pages, "birth_date")
        else:
            people = load_serialization(serialization_file)

        logging.info("parsing records ...")
        records = {}
        for p in people:
            record = self.parse_record(p)
            records[record['title']] = record
        logging.info("records parsed with count " + str(len(records)))

        if write_to_json:
            logging.info("writing records to json ...")
            jsonFile = open(self.data_directory + "records.json", "w")
            jsonString = json.dumps(records)
            jsonFile.write(jsonString)
            jsonFile.close()
            logging.info("records written into json")

        return records
    

if __name__ == '__main__':
    #logging settig - INFO
    logging.basicConfig(level=logging.INFO)
    
    vinf_parser = VINF_Parser()
    vinf_parser.parse_records("D:/VINF_datasets/enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2",
                                read_xml=False)
