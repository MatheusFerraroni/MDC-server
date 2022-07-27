import numpy as np
import json
import os




def main():

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
        # print(f" Processing: {file_name}")

        with open(file_name, 'r') as file:
            story_content = json.load(file)

        # print(f"  Status: {story_content['status']}")

        if story_content['status']=='completed':


            story_default = list(filter(lambda x: x!="", story_content['content'].split("\n")))
            for i in range(len(story_default)):
                try:
                    lbl = story_default[i].split(":")[0]
                    turn = story_content['turns'][i]['text']
                except:
                    continue

                try:
                    contents[lbl].add(turn)
                except:
                    contents[lbl] = set([turn])

    for key in contents.keys():
        contents[key] = list(contents[key])

    creations_per_story = 5
    for _ in range(creations_per_story):
        for file_name in files:

            story_default = story_content['content'].split("\n")

            variation = []
            for i in range(len(story_default)):
                lbl = story_default[i].split(":")[0]
                
                if lbl=="":
                    variation.append("")
                else:
                    variation.append(np.random.choice(contents[lbl]))

            print(variation)





if __name__ == "__main__":
    main()