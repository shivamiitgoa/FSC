import os, sys, re, r2pipe, json

# Returns the paths of all folders which either contains header files
# or its subfolder contains any of the header files
def find_all_headers_folders(folder_path):
    headers_folder_set = set()
    for root, _, files in os.walk(folder_path):
        for x in files:
            if x.endswith(".h") or x.endswith(".hpp"):
                # Add this folder and its parent folders to the result set
                root_folders = root.split('/')
                for i in range(1, len(root_folders) + 1):
                    headers_folder_set.add("/".join(root_folders[:i]))
    return list(headers_folder_set)


# Given the path of source file and the list of all source folders (in which, all the headers used in the
# source file can be found), we compile the source code to object file and save that object
# file by the name of "object_file"
def compile_to_object_file(source_file_path, headers_folder_list):
    # Generate command to compile functions
    cmd = "g++ -c -g -I%s %s -o object_file" % (" -I".join(headers_folder_list), source_file_path)
    # Execute
    os.system(cmd)


# Retrieve the list of all non-static functions which is present in the source file along with its definition
def get_func_list(source_file_path):
    # Getting function names
    function_list_raw = os.popen("ctags -x --c++-kinds=f \"%s\"" % source_file_path).read().split('\n')
    function_list = []
    all_function_with_def_set = set()
    # We are removing static function 
    for f in function_list_raw:
        if ('static' not in f):
            # This is a check for empty lines
            try:
                function_list.append(f.split()[0])
            except:
                pass
        try:
            all_function_with_def_set.add(f.split()[0])
        except:
            pass
    return list(all_function_with_def_set)


# Save decompiled functions
def save_decompiled_functions(object_file_path, func_list_from_src):
    # Retrieve the decompiled assembly for all functions
    r2_pipe = r2pipe.open("object_file", flags=['-2'])
    _ = r2_pipe.cmd("aab")
    _ = r2_pipe.cmd("aac")
    
    decompiled_functions_list = list()
    func_to_decompiled_dict = dict()
    funcs = r2_pipe.cmdj("aflj")
    for func in funcs:
        f = func['offset']
        decompiled_function = r2_pipe.cmd('pdf @%s' % f)
        decompiled_functions_list.append(decompiled_function)
        for f2 in func_list_from_src:
            if ";-- %s" % f2 in decompiled_function:
                func_to_decompiled_dict[f2] = decompiled_function
            
    json.dump(func_to_decompiled_dict, open('decompiled_functions.json', 'w'), indent=4)
    print("Results are saved in decompiled_functions.json")

