from lark import Lark, Transformer, v_args
from lark import UnexpectedCharacters, LexError
from lark.indenter import Indenter
import os


calc_Makefile = """
    ?start: expr* 

    ?expr: includep
          | comment
          | exp_assign_var
          | exp_assign_inc_var

    ?exp_assign_var: string "=" valuevar -> assign_var
    ?exp_assign_inc_var: string "+=" valuevar  -> assign_inc_var

    ?valuevar : WS_INLINE* (astring WS_INLINE*)+ WS*

    ?astring: leaf_string
        | func
        | exp_assign_exp_def_var

    ?leaf_string: string -> return_string
        | atom
             
    ?seq_of_leaf_strings: (leaf_string WS_INLINE*)+ -> return_seq_of_leaf_strings
    ?exp_assign_exp_def_var: "${" string ":=" seq_of_leaf_strings "}"  -> assign_var

    ?atom: "${" string "}"    -> var
    ?func: "$(" func_expr ")"
    ?func_expr: func_name astring "," astring "," astring -> deal_with_func
    
    ?includep: "include" string WS*

    comment : "#" ext_word* WS
     
    func_name: "subst" -> valid_func_name

    string: /[a-zA-Z0-9\-\._\/+]+/ 
    ext_word : /[a-zA-Z0-9:WS_INLINE\t\/\-,: ]+/

    %import common.WORD
    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.WS
    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class ParseMakefileTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        str_children_value=""
        print("assign_name:",str(name))
        print("assign_var:",str(value))
        if hasattr(value,'children'):
            for achildren in value.children:
                if hasattr(achildren,'children'):
                    for a2children in achildren.children:
                        intermediate_children_value = str(a2children)
                        intermediate_children_value=intermediate_children_value.replace('\n','')
                        print("intermediate_children_value:"+intermediate_children_value)
                        str_children_value += intermediate_children_value
                else:
                    if isinstance(achildren,str):
                        achildren=achildren.replace('\n','')
                        print("achildren:"+achildren)
                        str_children_value += achildren
                    
            else:
                if isinstance(achildren,str):
                    achildren=achildren.replace('\n','')
                    print("achildren:"+achildren)
                    str_children_value += achildren
                else:
                    print("Pb do not know what is children_value:"+str(achildren))
                    print(dir(achildren))
        else:
            if isinstance(value,str):
                str_children_value = value
            else:
                print("Pb do not know what is value:"+str(value))
                print(dir(value))
                
        self.vars[str(name.children[0])] = str_children_value
        return str_children_value

    def assign_inc_var(self, name, value):
        if hasattr(value,'children'):
            self.vars[str(name.children[0])] = str(value.children[0])
            return str(value.children[0])
        
    def var(self, name):
        thename=""
        if hasattr(name,'children'):
            thename=str(name.children[0])
            
        if thename=="WRKDIR":
            return os.getcwd()
        if thename=="MASTER_REPOSITORY_GITHUB":
            return "git https://github.com/"
        if thename=="MASTER_SITE_GITHUB":
            return "https://github.com/"
        if thename=="PKGVERSION_NOREV":
            if 'VERSION' in self.vars.keys():
                return self.vars["VERSION"]
            if 'PKGVERSION' in self.vars.keys():
                print("PKGVERSION: "+ self.vars["PKGVERSION"])
                return self.vars["PKGVERSION"]
            return "nothing"
        return self.vars[thename]

    def deal_with_func(self, value_func_name,\
                       value_1st_arg,\
                       value_2nd_arg,\
                       value_3rd_arg):
        str_value_func_name = value_func_name
        if hasattr(value_1st_arg,'children'):
            str_value_1st_arg = str(value_1st_arg.children[0])
        else:
            str_value_1st_arg = value_1st_arg

        if hasattr(value_2nd_arg,'children'):
            str_value_2nd_arg = str(value_2nd_arg.children[0])
        else:
            str_value_2nd_arg = value_2nd_arg
            
        str_value_3rd_arg = value_3rd_arg
        from string import Template
        if str_value_func_name=="subst":
            return str_value_3rd_arg.replace(str_value_1st_arg,\
                                             str_value_2nd_arg)
                                  
    def valid_func_name(self):
        return "subst"

    def return_string(self,value):
        if hasattr(value,'children'):
           print("return_string:"+str(value.children[0]))            
           return str(value.children[0])
        print("return_string:"+str(value)) 
        return value
    
    def retun_atom_string_atom(self,value):
        print("retun_atom_string_atom:"+str(value))
        return value
    
    def return_seq_of_leaf_strings(self,value,value2,value3):
        print("retun_seq_of_leaf_strings value:"+str(value))
        print("retun_seq_of_leaf_strings value2:"+str(value2))
        print("retun_seq_of_leaf_strings value3:"+str(value3))
        return str(value)+str(value2)+str(value3)
    
    def display(self):
        for key,value in self.vars.items():
            print("vars["+str(key)+"]="+str(value))

class PythonIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

kwargs = dict(rel_to=__file__, postlex=PythonIndenter(), start='file_input')

#Makefile_parser = Lark.open("python3.lark", parser='lalr', **kwargs)


def lark_parse_makefile(makecontent,anobj):
    aTransformer = ParseMakefileTree()
    Makefile_parser = Lark(calc_Makefile, parser='lalr',
                           transformer=aTransformer)
    Makefilep = Makefile_parser.parse

    Makefilep(makecontent)
    #aTransformer.display()
    anobj.vars = aTransformer.vars

        
