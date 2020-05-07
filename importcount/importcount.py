import os
import fnmatch


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def output_write(framework, text):
    with open("importcount/" + framework + "_importcount_output.csv", "a") as f:
        f.write(text + "\n")
        f.close()


def remove_next_line(sample):
    return sample.replace('\n', '')


def create_output(framework, imports, java_files_path, relative, sample):
    return framework + "," + sample + "," + str(len(imports)) + "," + str(len(java_files_path)) + "," + str(relative)


def calculate_relative(imports, java_files_path):
    if len(java_files_path) == 0:
        relative = 0
    else:
        relative = len(imports) / len(java_files_path)
    return relative


def get_imports_android(java_files_path):
    imports = set()
    for file in java_files_path:
        with open(file) as java_file:
            for line in java_file:
                line = remove_next_line(line)
                line = line.split(" ")
                if line[0] == "import":
                    lib = line[1].replace(";", "")
                    if lib.split(".")[0] == "android":
                        imports.add(lib)
    return imports


def get_imports_spring(java_files_path):
    imports = set()
    for file in java_files_path:
        with open(file) as java_file:
            for line in java_file:
                line = remove_next_line(line)
                line = line.split(" ")
                if line[0] == "import":
                    lib = line[1].replace(";", "")
                    if lib.split(".")[0] == "org" and lib.split(".")[1] == "springframework" and lib.split(".")[2] == "boot":
                        imports.add(lib)
    return imports


def get_imports(framework, java_files_path):
    if framework == "android":
        return get_imports_android(java_files_path)
    elif framework == "spring":
        return get_imports_spring(java_files_path)


def importcount(framework, projects):
    output_write(framework, 'framework,path,imports,javaFiles,imports/java_files')
    with open(projects) as samples:
        for sample in samples:
            sample = remove_next_line(sample)
            java_files_path = find("*.java", "repositories/" + sample)
            imports = get_imports(framework, java_files_path)
            relative = calculate_relative(imports, java_files_path)
            output_write(framework, create_output(framework, imports, java_files_path, relative, sample))