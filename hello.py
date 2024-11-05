import argparse 

parse = argparse.ArgumentParser()
parse.add_argument('name')
args = parse.parse_args()
name = args.name
print(args)
print("hello " + name + "!!!!")