import numpy as np
import json
import os
import argparse
import shutil
import random

contador_gerador = 0



def main(turn_default):

    configs_file = "./configs.json"

    print(f"Opening configs at: {configs_file}")
    with open(configs_file, 'r') as file:
        configs = json.load(file)

    
    story_folder = os.path.join(configs['server_folder'], 'processed_stories')
    print(f"Sarching stories in folder: {story_folder}")

    files = [os.path.join(story_folder, f) for f in os.listdir(story_folder)]
    print(f"Total files: {len(files)}")


    contents = {}


    for file_name in files:
        with open(file_name, 'r') as file:
            story_content = json.load(file)


        if story_content['status']=='completed':
            story_default = list(filter(lambda x: x!="", story_content['content'].split("\n")))
            story_default = prepare_story_turns(story_default)

            for i in range(len(story_default)):
                lbl = story_default[i].split(":")[0]
                turn = story_content['turns'][i]['text']

                try:
                    contents[lbl].add(turn)
                except:
                    contents[lbl] = set([turn])


    for key in contents.keys():
        contents[key] = list(contents[key])



    create(turn_default, contents, 0, "")

    print(contador_gerador)




def prepare_story_turns(turns):
    story_default = filter(lambda x: x!="", turns)
    story_default = map(lambda x: x.split(":")[0], story_default)
    story_default = filter(lambda x: x!="Start", story_default)
    story_default = list(story_default)
    return story_default







def create(turnos_default, variations, pos, story_path):
    global contador_gerador
    if pos>=len(turnos_default):
        with open(f"./da_content/{contador_gerador}.txt", 'w') as f:
            f.write(story_path)
        contador_gerador += 1
        return

    caminhos = variations[turnos_default[pos]]

    random.shuffle(caminhos)

    caminhos = caminhos[:2]
    # print(len(caminhos))

    for sample in caminhos:
        create(turnos_default, variations, pos+1, story_path+sample+"\n")













if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Data Augmentation script.')
    parser.add_argument('--input', type=str, required=True, help='Input file to search for strucutre.')

    args = parser.parse_args()
    f_path = args.input

    if not os.path.isfile(f_path):
        raise Exception(f"Not found {f_path}")

    with open(f_path, 'r') as file:
        turns = prepare_story_turns(file.read().split("\n"))


    if os.path.isdir("./da_content/"):
        shutil.rmtree("./da_content/")
    os.mkdir("./da_content/")


    main(turns)



